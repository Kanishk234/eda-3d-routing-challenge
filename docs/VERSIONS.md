# Versions — October 1, 2026

Location: native WSL Ubuntu /home/younix/eda-3d-routing-challenge, Windows UNC \\wsl.localhost\Ubuntu\home\younix\eda-3d-routing-challenge. Host LAPTOP-C8RSJ5BT, Ubuntu 24.04.4 LTS, x86_64 kernel 6.6.87.2-microsoft-standard-WSL2. Evidence timestamps UTC; user date/timezone October 1, America/Chicago.

- Official upstream main 499ad7e2a415a97e9ce9b3396b0477e75ebd13e6, confirmed git ls-remote/API. Local HEAD d887a05b844f9aeda0f656ca4644c58969d41ec5; initial clean Git state; origin https://github.com/Kanishk234/eda-3d-routing-challenge.git.
- Intel Core Ultra 9 285H, 16 WSL online/affinity CPUs; VM topology is not a physical-laptop core assertion.
- WSL total RAM 16,435,576,832 bytes (~15.3 GiB), initial available 13,582,548,992 bytes (~12.7 GiB); swap 4,294,967,296 bytes, initially unused. Host Windows RAM and separate quotas unknown; cgroup v2 limit files unavailable.
- CPython 3.12.3, project .venv created; pip 24.0, empty pip freeze. Core stdlib only. No system-Python installs or optional matplotlib.
- GCC/g++ 13.3.0 Ubuntu 13.3.0-6ubuntu2~24.04.1, GNU Make 4.3; GNU time/timeout available. CMake absent/unneeded.
- Compiler command: g++ -O3 -std=c++17 -Wall -Wextra -Wpedantic dev/toolchain_probe.cpp -o dev/artifacts/toolchain_probe. Run output: C++17 ready; int64 bits=64. No router implemented.
- No GPU used, queried or provisioned. CPU-first per user.

Setup/build/run commands in dev/README.md. One worker initially; tests 180 seconds; smoke/CI 60 seconds per subprocess. No long benchmark or costs.

Sandbox exec/Node failed before launch; patch helper rejected UNC reparse point. Approved PowerShell writes/native WSL execution worked. Windows Git dubious-ownership refusal avoided via native WSL Git without global safe.directory changes.
