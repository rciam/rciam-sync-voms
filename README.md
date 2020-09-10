# rciam-sync-voms

A Python-based tool for synchronising VO/group membership and role information from VOMS servers.

## Instalation

Install from git and configure

```bash
git clone https://github.com/rciam/rciam-sync-voms.git
cd rciam-sync-voms
cp config.py.example config.py
vi config.py
```

Create a Python virtualenv, install dependencies, and run the script

```bash
virtualenv -p python3 .venv
source .venv/bin/activate
(.venv) pip3 install -r requirements.txt
(.venv) python3 main.py
🍺
```

## License

Licensed under the Apache 2.0 license, for details see `LICENSE`.
