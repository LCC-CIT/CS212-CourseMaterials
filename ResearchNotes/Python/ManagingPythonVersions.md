<h1>Managing Multiple Versions of Python on Windows</h1>

- [Traditional Approach](#traditional-approach)
  - [Install & Versions](#install-versions)
  - [PATH Hygiene](#path-hygiene)
  - [Virtual Environments (per project)](#virtual-environments-per-project)
  - [Selecting Python in Tools](#selecting-python-in-tools)
  - [Pip Safety](#pip-safety)
  - [Dependency Management](#dependency-management)
    - [requirements.txt vs. pyproject.toml](#requirementstxt-vs-pyprojecttoml)
      - [Creating a pyproject.toml file](#creating-a-pyprojecttoml-file)
      - [Use pip with pyproject.toml](#use-pip-with-pyprojecttoml)
      - [Installing a project with pip and pyproject.toml](#installing-a-project-with-pip-and-pyprojecttoml)
  - [Optional Managers](#optional-managers)
  - [Maintenance](#maintenance)
- [New Python Install Manager](#new-python-install-manager)
  - [Using the New Python Install Manager](#using-the-new-python-install-manager)
  - [Install a Python runtime version](#install-a-python-runtime-version)
    - [List installed runtime versions of Python](#list-installed-runtime-versions-of-python)
    - [Run a program with a particular version of Python](#run-a-program-with-a-particular-version-of-python)
    - [Create a venv for a particular version of Python](#create-a-venv-for-a-particular-version-of-python)
    - [Activate an venv](#activate-an-venv)
    - [Install a package for a particular version of Python](#install-a-package-for-a-particular-version-of-python)

## Traditional Approach



### Install & Versions

- Use `py` launcher: the Windows `py` launcher lets you target versions reliably (`py -3.12`, `py -3.13`), avoiding PATH conflicts.
- Prefer python.org installers: install 64-bit builds from python.org; avoid the Microsoft Store version for dev work.
- Keep multiple majors: install stable LTS-like versions (e.g., 3.12) alongside latest (e.g., 3.13) for projects needing older wheels.

### PATH Hygiene

- Minimal PATH: let the `py` launcher be the only Python entry on PATH; don’t add multiple `...\PythonXX\` or `...\Scripts\` paths.
- Verify with `py -V` and `py -0p`: shows all installed interpreters and their paths.

### Virtual Environments (per project)

- One venv per project: never install packages globally; isolate with venv.
- Create with targeted interpreter:
  - `py -3.13 -m venv .venv` or `py -3.12 -m venv .venv`
- Activate and install:
  - `.\.venv\Scripts\Activate.ps1`
  - `python -m pip install --upgrade pip`
  - `python -m pip install -r requirements.txt`
- In VS Code, select the interpreter for the workspace: Command Palette → Python: Select Interpreter → pick `.venv\Scripts\python.exe`.

### Selecting Python in Tools

- CLI: `py -3.12 -m pip ...`, `py -3.13 script.py`
- Shebangs: `#!/usr/bin/env python3` generally fine; on Windows, prefer explicit `py -3.12` when scripting.
- VS Code: set `python.defaultInterpreterPath` per workspace or use `.vscode/settings.json` to point to `.venv`.

### Pip Safety

- Always call pip via the interpreter: `python -m pip ...` inside the active venv to avoid cross-installing into the wrong version.
- Upgrade pip inside each venv after creation.

### Dependency Management

- Pin dependencies: use [requirements.txt](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) with versions that are known to work for each Python.
- Rebuild venv when changing Python major/minor: delete `.venv`, recreate with the target version, and reinstall.
- Watch platform wheels: packages like `windows-curses` may lag for newest Python (e.g., 3.13). For your [main.py](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html), if `windows-curses` fails on 3.13, run on 3.12 for now or guard with a friendly message.

#### requirements.txt vs. pyproject.toml

- Pyproject.toml: Modern, standards-based manifest (PEP 621) used by build tools like `pip`, `uv`, `poetry`, `hatch`. Declares dependencies in one file, similar to `package.json`.
- [Requirements.txt:](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) Simple list of runtime dependencies for apps; installed via `pip install -r requirements.txt`. Common for non-library projects.
- Setup.cfg/setup.py: Older packaging formats for libraries; still supported but largely superseded by `pyproject.toml`.

Recommended for your project

- If this is an application (not published as a library): use [requirements.txt](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html).
- If you want a manifest similar to `package.json`: use `pyproject.toml` with a tool like `uv` or `poetry`.

Quick starts

- [Requirements.txt](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) workflow:
  - Install deps: `pip install requests windows-curses google-genai`
  - Freeze versions: `pip freeze > requirements.txt`
  - Reinstall later: `pip install -r requirements.txt`
- Pyproject.toml with uv (fast, simple):
  - Install uv: `pip install uv`
  - Init project: `uv init`
  - Add deps: `uv add requests windows-curses google-genai`
  - Run: `uv run python main.py`
- Pyproject.toml with poetry:
  - Install poetry: `pip install poetry`
  - Init: `poetry init` (follow prompts)
  - Add deps: `poetry add requests windows-curses google-genai`
  - Run: `poetry run python main.py`

##### Creating a pyproject.toml file

Several Python packaging tools can scaffold a pyproject.toml for you. Pick one:

1. Poetry

- Install (optional): pipx install poetry
- Create in existing folder (interactive): poetry init
- Or scaffold a new project (includes pyproject.toml): poetry new myproject

1. PDM

- Install (optional): pipx install pdm
- Initialize in current folder: pdm init

1. Hatch

- Install (optional): pipx install hatch
- Initialize in current folder: hatch init
- Or scaffold a new project: hatch new myproject

1. Flit

- Install (optional): pipx install flit
- Interactive init: flit init

1. Rye

- Install (optional): pipx install rye
- Initialize in current folder: rye init

1. uv

- Install (optional): pipx install uv
- Scaffold a new project: uv init myproject

Notes

- There’s no built-in pip command to generate pyproject.toml; you use one of the tools above.
- On Windows, use py -m pipx install <tool> if pipx is installed via Python.

##### Use pip with pyproject.toml

How pip interacts with `pyproject.toml`, when it works, and a minimal example with commands.

- What works: If your `pyproject.toml` declares dependencies under `[project] dependencies` (PEP 621), `pip` can install them via `pip install .` (or `pip install -e .` for editable). Pip will build and install the project, pulling those deps.
- What pip does not do: Pip doesn’t “read” `pyproject.toml` just to install dependencies for running your app without installing the project. For that workflow, keep using [requirements.txt](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html).

Minimal `pyproject.toml` for this app:

- Create `pyproject.toml` in the repo root with:

Commands:

Guidance:

- Use `pip install -e .` if you want imports to reflect local code changes without reinstalling.
- If you prefer not to “install” your app, stick with [requirements.txt](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html): `pip install -r requirements.txt`.
- Tools like `uv`, `poetry`, and `hatch` use `pyproject.toml` directly to manage deps and are more “package.json-like” for app projects.

##### Installing a project with pip and pyproject.toml

What “install” means for a Python app, how `pip install .` behaves with `pyproject.toml`, and when to use editable mode.

- Install (Python context): Copies your project into the environment’s `site-packages`, records its metadata, and installs declared dependencies so it can be imported or run like any other installed package.
- Dependencies: Pip reads `[project] dependencies` from `pyproject.toml` (or `install_requires` in legacy formats) and installs those packages into your venv.
- Entry points: If your project defines console scripts in `pyproject.toml` (under `[project.scripts]`), `pip install` creates runnable commands in `venv313\Scripts\` so you can launch your app without `python main.py`.
- Non-editable vs editable:
  - Non-editable: `pip install .` copies a built artifact; changes to your source don’t affect the installed package until you reinstall.
  - Editable: `pip install -e .` links the install to your source directory; changes are immediately reflected when importing/running.

Common commands:

When you’re building an app you run via `python main.py`, you don’t have to “install” it—using [requirements.txt](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) and running the script directly is fine. “Installing” is useful when you want:

- A single command to run it (via console scripts).
- Dependencies managed via a manifest (`pyproject.toml`).
- Your app/library importable from anywhere in that environment.

### Optional Managers

- `pyenv-win` (Windows port): can help install/manage multiple versions, but the built-in `py` launcher is typically sufficient on Windows.
- Conda/Mamba (if used): keep environments separate from `venv`; don’t mix package managers within the same env.

### Maintenance

- List installed versions: `py -0p`
- Remove outdated versions: uninstall via Apps → Installed apps; rebuild affected venvs.
- Keep venvs project-local: store at `.venv` in the project root; don’t share venvs across projects.

## New Python Install Manager

The Python install manager helps you to install, manage, and launch  Python on Windows. After install, the "py" command is your tool of choice - try "py help"  to see what it can do! (Not working? You may need to uninstall the old  "Python launcher", and check "Manage app execution aliases" to ensure  the command is enabled.) Complete documentation is available at  http://docs.python.org/3/using/windows

**Release date:** Dec. 5, 2025 (Version 25.2)

The Python install manager for Windows is our tool for  installing and managing runtimes. The traditional executable installer  will stop being released with Python 3.16



### Using the New Python Install Manager

### Install a Python runtime version

```python
py install 3.12
```

#### List installed runtime versions of Python

```python
py list
```

#### Run a program with a particular version of Python

```python
python main.py -V:3.13
```

#### Create a venv for a particular version of Python

```python
py -V:3.13 -m venv .venv313
```

#### Activate an venv

```py
.\.venv313\Scripts\activate
```

#### Install a package for a particular version of Python

```python
py -3.13 -m pip install windows-curses
```

`-m` Means run a module as a script. In this case we're using this command to run pip with Python 3.13.

By Brian Bird, with drafts from GitHub Copilot, 12/15/2025

