"""Repair-first refinement that reserves most fixed work for physical polish."""
import json,sys
from pathlib import Path
import evolution_pilot as pilot
from measure import digest,save

def mutation(source,kind):
 if kind=='control':return source
 percent={'slice10':10,'slice25':25}[kind]
 mode='engine.price_units=kernel=="fanout_fine"?16:1;'
 call='repair(seed+static_cast<unsigned long long>(pass),1,4,true,false,wide?std::max(12,group_limit-1):4);'
 anchor='    void explore(unsigned long long seed,int passes,bool wide=false) {'
 assert source.count(mode)==1 and source.count(call)==2 and source.count(anchor)==1
 helper='''    void budgeted_repair(unsigned long long seed,int passes,I penalty,bool negotiated,bool selection,int blockers) {
        auto full=work_limit;
        if(!full || expansions>=full) {repair(seed,passes,penalty,negotiated,selection,blockers);return;}
        work_limit=expansions+std::max<std::uint64_t>(1,(full-expansions)*PERCENT/100);
        try {repair(seed,passes,penalty,negotiated,selection,blockers);}
        catch(...) {work_limit=full;throw;}
        work_limit=full;
        // Work interruption rolled back the current transaction. Resume only
        // when no real stop/time/global-work condition has occurred.
        if(work_exhausted && !stopped && std::chrono::steady_clock::now()<deadline && expansions<full) {
            work_exhausted=false;timed_out=false;
        }
    }
'''.replace('PERCENT',str(percent))
 return source.replace(mode,mode+'engine.repair_first=true;').replace(call,'budgeted_'+call).replace(anchor,helper+anchor)

def main():
 source=Path(__file__);expected=digest(source);pilot.mutation=mutation;pilot.main();out=Path(sys.argv[sys.argv.index('--out')+1]);report=json.loads((out/'progress.json').read_text());assert digest(source)==expected;(out/source.name).write_bytes(source.read_bytes());report['additional_source_sha256']={str(source.resolve()):expected};report['scope']+=' Bounded repair consumes at most10/25percent remaining expansion budget per pass,then physical polish. Local work-stop resets only after transaction rollback and absent global/time/stop exhaustion.';save(out/'progress.json',report)
if __name__=='__main__':main()
