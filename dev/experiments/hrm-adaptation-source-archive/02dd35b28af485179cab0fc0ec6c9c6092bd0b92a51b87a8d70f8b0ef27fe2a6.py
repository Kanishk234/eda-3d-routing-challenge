"""Load pinned pretrained HRM on CPU without its CUDA dataset evaluator.

This synthetic inference probe establishes feasibility, not routing quality.
Third-party source and weights remain in ignored artifacts with their license.
"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path


def load_cpu(model_dir, threads=2):
    import torch
    import yaml
    assert 1 <= threads <= 16
    manifest = json.loads((model_dir / 'manifest.json').read_text())
    for f in manifest['files']:
        path = model_dir / (('source/' if 'git_blob' in f else '') + f['path'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == f['sha256']
    sys.path.insert(0, str((model_dir / 'source').resolve()))
    from models.recursive_reasoning.hrm import HierarchicalReasoningModel_ACTV1
    torch.set_num_threads(threads)
    torch.manual_seed(0)
    state = torch.load(model_dir / 'pytorch_model.bin', map_location='cpu', weights_only=True)
    prefix = '_orig_mod.model.'
    assert all(k.startswith(prefix) for k in state)
    state = {k[len(prefix):]: v for k, v in state.items()}
    arch = yaml.safe_load((model_dir / 'all_config.yaml').read_text())['arch']
    config = {k: v for k, v in arch.items() if k not in ('name', 'loss')}
    config.update(batch_size=1, seq_len=1024, vocab_size=7,
                  num_puzzle_identifiers=state['inner.puzzle_emb.weights'].shape[0])
    model = HierarchicalReasoningModel_ACTV1(config)
    model.load_state_dict(state, strict=True)
    model.eval()
    return model, config, manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model-dir', type=Path, default=Path('dev/artifacts/hrm-pretrained'))
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--threads', type=int, default=2)
    a = p.parse_args()
    import torch
    assert not a.out.exists()
    model, config, manifest = load_cpu(a.model_dir, a.threads)
    # 16 rows x 4 layers x 16 columns; a pair of endpoints per color.
    grid = torch.ones((16, 4, 16), dtype=torch.long)
    for net in range(4):
        grid[2 + net * 3, net, 2] = 3 + net
        grid[2 + net * 3, net, 13] = 3 + net
    batch = {'inputs': grid.reshape(1, 1024), 'puzzle_identifiers': torch.zeros(1, dtype=torch.long)}
    carry = model.initial_carry(batch)
    begin = time.perf_counter()
    with torch.inference_mode():
        for step in range(config['halt_max_steps']):
            carry, output = model(carry, batch)
        assert bool(carry.halted.all())
        assert torch.isfinite(output['logits']).all()
    pred = output['logits'].argmax(-1)
    result = dict(complete=True, scope='Synthetic CPU feasibility only; no official-case score or legality claim',
                  model_manifest_sha256=hashlib.sha256((a.model_dir / 'manifest.json').read_bytes()).hexdigest(),
                  source_revision=manifest['revision'], torch_version=torch.__version__,
                  threads=a.threads, dtype=config['forward_dtype'], steps=step + 1,
                  inference_wall_s=time.perf_counter() - begin,
                  physical_parameter_count=sum(x.numel() for x in model.parameters()),
                  logits_shape=list(output['logits'].shape), finite_logits=True,
                  input_sha256=hashlib.sha256(grid.numpy().tobytes()).hexdigest(),
                  predictions=pred[0].tolist())
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2) + '\n')
    print({k: v for k, v in result.items() if k != 'predictions'})


if __name__ == '__main__':
    main()
