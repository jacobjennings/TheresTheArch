# Agent Guide — TheresTheArch

Guidance for AI agents (and humans) working in this repository.

## What this is

A toolkit for generating Minecraft [Litematica](https://github.com/maruohon/litematica)
schematics, focused on a mathematically accurate Gateway Arch. Two parts:

- `litematica-python/` — an independent, from-scratch Python library for reading
  and writing the `.litematic` format. Depends only on the `NBT` package.
- `theresthearch/` — the Gateway Arch generator built on that library:
  - `arch_generator.py` — core generation logic + Python API (`ArchGenerator`,
    `create_simple_arch`)
  - `arch_cli.py` — interactive command-line interface (no GUI deps)
  - `arch_gui.py` — Tkinter GUI

The `litematica/` directory is an **optional** git submodule pointing at the
upstream mod for reference only (LGPL-3.0). It is not needed to build, test, or
run anything — clone without `--recursive`.

## Setup

```bash
./setup.sh                 # creates venv and installs NBT
source venv/bin/activate
# or simply: pip install NBT
```

Python 3.7+ (CI exercises 3.9 and 3.12). The GUI additionally needs `tkinter`.

## Run

```bash
python theresthearch/arch_cli.py     # interactive CLI (recommended)
python theresthearch/arch_gui.py     # GUI (requires tkinter)
```

## Test

```bash
python litematica-python/test_basic.py
```

CI also runs a smoke generation. Run both the test suite and a small
`ArchGenerator(scale=0.1).generate()` after changing generation or format code.

## Conventions & gotchas

- **Imports rely on `sys.path` insertion.** `theresthearch/*.py` add
  `../litematica-python` to `sys.path` at runtime to import `litematica`. Keep
  that working; don't assume the packages are pip-installed.
- **PyInstaller builds** (see `.github/workflows/release.yml`) must pass
  `--paths theresthearch --paths litematica-python` or the bundled binary fails
  to import `arch_generator` / `litematica`.
- **Generated output** (`*.litematic`) is git-ignored — don't commit schematics.
- Keep docs honest: avoid invented performance/RAM/timing numbers (point at the
  live preview instead).

## Workflow preference

When the git user is **Jacob Jennings** (`jacob.r.jennings@gmail.com`, GitHub
`jacobjennings`), develop **directly on `main`** — do not create feature
branches for routine changes; commit and push to `main`. For any other user,
follow the normal default of branching off `main` and opening a pull request.
