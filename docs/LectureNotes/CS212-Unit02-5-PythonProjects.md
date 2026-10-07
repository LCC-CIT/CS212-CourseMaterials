---
title: .venv and Python Projects
description: How to use virtual environments (.venv), pip, and uv to manage Python projects and their packages.
keywords: Python, venv, pip, uv, pyproject.toml, MacOS, Windows
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Python Projects</h1>

<h2>Contents</h2>

[TOC]

## Why Projects Need Their Own Environment

Python's real power comes from its huge collection of third-party *packages*, such as NumPy, TensorFlow, and Z3. Packages are installed with a *package manager*. Python's official package manager is `pip`, which downloads packages from the <a href="https://pypi.org/" target="_blank">Python Package Index (PyPI)</a>.

If you installed every package you used into your one system-wide copy of Python, you would eventually run into problems:

- **Version conflicts**&mdash;Project A needs version 1 of a library and Project B needs version 2. Only one can be installed at a time.
- **A messy, unreproducible setup**&mdash;After a few months you wouldn't remember which packages each project actually needs, and a teammate (or your instructor) wouldn't know what to use to run your app.
- **Risk to your system**&mdash;Some operating systems (and Homebrew on macOS) use their copy of Python for their own tools. Changing its packages can break them. Newer versions of Python refuse to let `pip` modify these system installations, and display an `externally-managed-environment` error.

The solution is to give **each project its own isolated environment** with its own packages (and possibly its own version of Python). This is called a *virtual environment*.

## Managing Virtual Environments with `venv` and `pip`

Python includes the `venv` module for creating virtual environments, and `pip` for installing packages into them. These are the official, built-in tools, and they work the same way on every computer that has Python. 

> Note that `venv` is a module (a file of Python code that provides ready-made functions and tools, which Python can import or run), not a standalone program. The `-m` option means "run this module as a script," so the command always starts with `python -m` (or `py -m`).

### What is a .venv Folder?

A virtual environment is just a folder that contains:

- A copy of (or link to) a Python interpreter.
- A private `site-packages` folder where packages installed into the environment are stored.
- Scripts to activate the environment.
- A small configuration file, `pyvenv.cfg`, that records which Python the environment was built from.

By convention the folder is named **`.venv`** and is created inside the project folder. (The leading dot makes it a "hidden" folder on macOS and Linux, and many tools, including VS Code look for this name automatically.)

A typical project looks like this:

```
my_project/
├── .venv/              <- the virtual environment (don't edit, don't commit)
│   ├── pyvenv.cfg
│   ├── Scripts/        <- Windows: python.exe, pip.exe, activate scripts
│   ├── bin/            <- MacOS: python, pip, activate scripts
│   └── Lib/ or lib/    <- installed packages live here
├── main.py
└── requirements.txt
```

When the environment has been *activated* (see below), typing `python` or `pip` runs or uses what is inside `.venv`, so anything you install goes will go into that folder and only affect that project. Deleting the `.venv` folder removes the environment completely, and you can always make a new one.

### Create a Virtual Environment

Open a terminal, use `cd` to move to your project folder, and create the environment.

#### Windows

```powershell
py -m venv .venv
```

(If `py` isn't available, use `python -m venv .venv`.)

#### MacOS

```bash
python3 -m venv .venv
```

The `-m venv` option tells Python to run its `venv` module, and `.venv` is the name of the folder to create. The environment uses the same version of Python that ran the command.

### Activate the Environment

Creating the environment doesn't *use* it. You must activate it in each new terminal window.

#### Windows

In PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

In Command Prompt (CMD):

```
.venv\Scripts\activate.bat
```

If PowerShell says that running scripts is disabled on this system, allow locally created scripts for your user account (you only need to do this once):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

#### MacOS

```bash
source .venv/bin/activate
```

When activation succeeds, the name of the environment appears at the start of your prompt:

```
(.venv) PS C:\PythonProjects\my_project>
```

You can confirm that you are using the environment's Python by asking where it is:

```powershell
# Windows PowerShell
Get-Command python
```

```bash
# MacOS
which python
```

The path should point inside your project's `.venv` folder. Inside an activated environment, `python` works on macOS too&mdash;you don't need to type `python3`.

### Install Packages with pip

With the environment active, use `pip` to install packages. Since `pip` is itself a Python module, the most reliable way to call it is through Python:

```bash
python -m pip install z3-solver
```

Some other useful pip commands:

```bash
python -m pip install numpy pandas          # install several packages
python -m pip install numpy==2.1.0          # install a specific version
python -m pip install --upgrade numpy       # upgrade a package
python -m pip uninstall numpy               # remove a package
python -m pip list                          # show what's installed
python -m pip show numpy                    # details about one package
```

Packages installed this way are stored in `.venv` and are visible only when it's active.

### Document Your Dependencies with `requirements.txt`

To record exactly which packages (and versions) your project uses, save them to a text file:

```bash
python -m pip freeze > requirements.txt
```

Anyone else (or you, on another computer) can then recreate the same environment:

```bash
python -m venv .venv
# activate it, then:
python -m pip install -r requirements.txt
```

This is how most course projects and many open-source projects share their dependencies.

### Deactivate the Environment

When you're finished working, return to your normal shell:

```
deactivate
```

### Use the Environment in VS Code

VS Code needs to know which Python to use to run and debug your code.

1. Open your project folder in VS Code (**File > Open Folder**).
2. Press `Ctrl+Shift+P` (`Cmd+Shift+P` on macOS) and run **Python: Select Interpreter**.
3. Choose the one marked **Recommended** or labeled `.venv`.

VS Code often detects a `.venv` folder on its own and offers to use it. Once selected, new integrated terminals are activated automatically, and the green "Run" button and the debugger (`F5`) use the environment's Python.

### Version Control and .venv

Never commit the `.venv` folder to Git. It is large, it contains files specific to your operating system and your computer, and it can be re-created from `requirements.txt` at any time. Add this line to your project's `.gitignore` file:

```
.venv/
```

Also, don't copy or move a `.venv` folder to another location or computer. It contains absolute paths and won't work. Create a new one instead.

### Troubleshooting

| Problem                                                      | Likely cause and fix                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `ModuleNotFoundError: No module named 'z3'`                  | The package isn't installed in the Python you're running. Activate `.venv` (or select it in VS Code) and run `python -m pip install z3-solver`. |
| `externally-managed-environment` error from pip              | You are using the system Python, not a virtual environment. Create and activate a `.venv` first. |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Run the `Set-ExecutionPolicy` command shown above, once.     |
| Nothing happens, or the wrong Python version is used         | Check the path with `Get-Command python` or `which python`. Delete `.venv` and re-create it with the right version of Python. |
| Packages vanished after moving the project                   | `.venv` can't be moved. Delete it and re-create it, then run `pip install -r requirements.txt`. |

## Managing Virtual Environments (and more) with `uv`

### What is `uv`?

<a href="https://docs.astral.sh/uv/" target="_blank">**uv**</a> is a modern, very fast Python package and project manager from a company called Astral. It's written in Rust, and it's designed to replace a whole collection of separate tools with a single command:

| Task                              | Traditional tool(s)              | uv equivalent                        |
| --------------------------------- | -------------------------------- | ------------------------------------ |
| Install and switch Python versions | `pyenv` and installers from python.org | `uv python install`                  |
| Create virtual environments       | `python -m venv`                 | `uv venv` (or automatic)             |
| Install packages                  | `pip`                            | `uv add`, `uv pip install`           |
| Record exact dependency versions  | `pip freeze`, pip-tools          | `uv.lock` (automatic)                |
| Run tools and scripts             | `pipx`, manual activation        | `uvx`, `uv run`                      |
| Project metadata and dependencies | Poetry, setuptools, PDM          | `pyproject.toml` managed by `uv`     |

In short, uv does everything in the previous section&mdash;and more&mdash;but you rarely have to think about activating environments or running `pip`. It still creates a `.venv` folder so everything you learned above still applies.

### Advantages and Disadvantages

**Advantages**

- **Speed**&mdash;Installing packages is typically 10 to 100 times faster than `pip`, thanks to Rust and aggressive caching. 
- **No duplicated storage**&mdash;Packages are stored once in a shared cache and linked into each environment, which saves disk space.
- **One tool**&mdash;Python versions, environments, dependencies, and running scripts all use the same commands on Windows and macOS.
- **Reproducibility**&mdash;The `uv.lock` file records the exact version of every package (including packages that your packages depend on) so everyone on a team gets the same environment.
- **Manages Python itself**&mdash;uv can download and install the version of Python a project needs, so there's no need to hunt for installers. 
- **No activation needed**&mdash;`uv run` automatically uses the project's environment, creating or updating it if necessary.
- **Compatible with pip**&mdash;It can read and export `requirements.txt` files, and `uv pip install` works like `pip install`.
- **Open source** and actively developed.

**Disadvantages**

- **Another tool to install**&mdash;Unlike `venv` and `pip`, uv doesn't come with Python.
- **Newer and fast-moving**&mdash;It is still a young project (its version numbers still start with 0), so commands and behaviors occasionally change, and online tutorials may be out of date.
- **Less universal**&mdash;`uv.lock` is a uv-specific file that other tools don't understand. Some tutorials, CI systems, and hosting services still assume `pip` and `requirements.txt`.
- **Two ways to do things**&mdash;`uv add` (project-based) and `uv pip install` (pip-style) behave differently, which can be confusing to beginners. Mixing them in one project is discouraged.
- **A company controls it**&mdash;The tool is open source, but it's developed by a commercial company, unlike `pip` and `venv` which are part of the Python project itself.

### Install uv

#### Windows

Run this in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or, if you prefer using WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

#### MacOS

Using Homebrew (which you installed in the previous lecture notes):

```bash
brew install uv
```

Or use the standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify the Installation**

Close and re-open your terminal, then run:

```
uv --version
```

To update uv later, run `uv self update` (if you installed it with the standalone installer), or use your package manager (`brew upgrade uv` or `winget upgrade astral-sh.uv`).

### Create a Project

Create a new project in a new folder:

```
uv init my_project
cd my_project
```

Or, to turn an existing, empty folder into a project, `cd` into it and run:

```
uv init
```

uv creates these files:

```
my_project/
├── .gitignore          <- already lists .venv/
├── .python-version     <- the Python version this project uses
├── main.py             <- a starter "Hello World" program
├── pyproject.toml      <- project settings and dependencies
└── README.md
```

(`uv init` also sets up a Git repository, unless you're already in one.) The `.venv` folder and `uv.lock` file are created the first time you add a package or run your code.

### Add and Remove Packages

Instead of `pip install`, use `uv add`:

```
uv add z3-solver
uv add numpy pandas
uv add "numpy>=2.0"
```

Each command does three things: it installs the package into `.venv` (creating it if needed), records it in the `dependencies` list in `pyproject.toml`, and updates `uv.lock` with the exact versions that were installed.

To remove a package:

```
uv remove pandas
```

Some packages are only needed while developing (such as testing or formatting tools). Add them to a separate *dependency group*:

```
uv add --dev pytest
```

To see everything that is installed:

```
uv tree
```

### Run Your Code

Use `uv run` instead of activating the environment and running `python`:

```
uv run main.py
```

Before running, uv makes sure that the environment exists and that it matches `pyproject.toml` and `uv.lock`, fixing it if it doesn't. You can run any command inside the environment the same way:

```
uv run python
uv run pytest
```

If you do want to activate `.venv` the traditional way (for example, to use a tool that expects it), you still can, using the same commands described earlier (`.venv\Scripts\Activate.ps1` on Windows or `source .venv/bin/activate` on macOS).

### Manage Python Versions

uv can find or download different versions of Python:

```
uv python list                # show available and installed versions
uv python install 3.12        # download and install Python 3.12
uv python pin 3.12            # use 3.12 for this project (writes .python-version)
uv init --python 3.12 my_proj # start a new project with a specific version
```

These Python installations are managed by uv and are separate from any Python you installed from python.org or with Homebrew.

### Work on an Existing Project

When you download or clone a project that already has a `pyproject.toml` and `uv.lock` (for example, from GitHub), set it up with a single command:

```
uv sync
```

uv creates `.venv`, installs the right version of Python if necessary, and installs the exact versions of all the packages that are recorded in `uv.lock`. You can then use `uv run` as usual.

If a project only has a `requirements.txt` file, you can still use uv in a pip-compatible way:

```
uv venv
uv pip install -r requirements.txt
```

### Command Cheat Sheet

| Command                  | What it does                                                 |
| ------------------------ | ------------------------------------------------------------ |
| `uv init [name]`         | Create a new project                                         |
| `uv add <package>`       | Install a package and add it to `pyproject.toml`             |
| `uv remove <package>`    | Uninstall a package and remove it from `pyproject.toml`      |
| `uv sync`                | Make `.venv` match `pyproject.toml` and `uv.lock`            |
| `uv lock`                | Update `uv.lock` without installing anything                 |
| `uv run <command>`       | Run a command or script in the project's environment         |
| `uv tree`                | Show the dependency tree                                     |
| `uv python install <ver>` | Download a version of Python                                |
| `uv python pin <ver>`    | Set the Python version for the project                       |
| `uvx <tool>`             | Run a command-line tool in a temporary environment (without installing it permanently) |
| `uv pip install <package>` | pip-compatible interface (for projects that don't use `pyproject.toml`) |

### Understanding pyproject.toml

#### What is TOML?

**TOML** (*Tom's Obvious, Minimal Language*) is a plain-text format for configuration files. It was designed to be easy for people to read and write. If you've seen JSON or INI files, TOML will look familiar. Files in this format end with the `.toml` extension. Python uses it for `pyproject.toml`, and many other tools do as well (for example, Rust's `Cargo.toml`).

The basic building blocks are:

```toml
# This is a comment

# Key = value pairs
name = "my-project"        # a string (always in quotes)
version = "0.1.0"
max_retries = 3            # an integer
pi = 3.14                  # a float
verbose = true             # a boolean (lowercase)

# Arrays (lists) use square brackets
authors = ["Ada", "Grace"]

# A table is a named group of key/value pairs, introduced by a [header]
[database]
host = "localhost"
port = 5432

# Tables can be nested using dots in the header
[database.credentials]
user = "student"
```

Compared with JSON, TOML allows comments, doesn't require quotes around keys, and doesn't need commas and braces everywhere. The table above corresponds to this JSON:

```json
{
  "name": "my-project",
  "version": "0.1.0",
  "max_retries": 3,
  "pi": 3.14,
  "verbose": true,
  "authors": ["Ada", "Grace"],
  "database": {
    "host": "localhost",
    "port": 5432,
    "credentials": { "user": "student" }
  }
}
```

Python 3.11 and later can read TOML files with the built-in `tomllib` module.

#### Anatomy of pyproject.toml

`pyproject.toml` is the standard file for describing a Python project (defined by <a href="https://peps.python.org/pep-0621/" target="_blank">PEP 621</a>). After running `uv init` and `uv add z3-solver` and `uv add --dev pytest`, it will look something like this:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "z3-solver>=4.13.0",
]

[dependency-groups]
dev = [
    "pytest>=8.3.0",
]
```

The sections are:

- **`[project]`**&mdash;Basic information about your project.
  - `name`, `version`, `description`&mdash;Descriptive metadata.
  - `requires-python`&mdash;Which versions of Python the project works with.
  - `dependencies`&mdash;The packages your project needs, each with an optional *version specifier*: `"numpy"` (any version), `"numpy>=2.0"` (2.0 or newer), `"numpy==2.1.0"` (exactly that version), or `"numpy>=2.0,<3"` (a range).
- **`[dependency-groups]`**&mdash;Extra sets of dependencies, such as `dev` for development-only tools.
- **`[tool.*]`**&mdash;Settings for individual tools. Each tool uses its own table name, for example `[tool.pytest.ini_options]` or `[tool.ruff]`. You can add these sections yourself.
- **`[build-system]`**&mdash;Describes how to package the project. It's only needed if you plan to build and publish a package, and `uv init` doesn't add it for a simple application.

You can edit this file by hand. After doing so, run `uv sync` (or `uv run`) to update the environment to match.

#### The uv.lock File

`pyproject.toml` lists the packages you *asked for*, usually with flexible version ranges. **`uv.lock`** records the exact version of *every* package that was installed, including the packages that your packages depend on, along with checksums for each. It is also a TOML file, but it's generated by uv, so **don't edit it by hand**.

| File             | You edit it? | Commit to Git? | Purpose                                       |
| ---------------- | ------------ | -------------- | --------------------------------------------- |
| `pyproject.toml` | Yes (or let `uv add` do it) | Yes | What the project needs                        |
| `uv.lock`        | No           | Yes            | Exactly what was installed, so others get the same thing |
| `.python-version` | Rarely      | Yes            | Which Python version to use                   |
| `.venv/`         | No           | **No**         | The installed environment (can be re-created) |

### Using uv with VS Code

uv creates a `.venv` folder in your project, so VS Code finds it the same way as in the previous section: open the project folder, run **Python: Select Interpreter**, and choose the `.venv` interpreter. After that, the debugger and `F5` work normally.

## Exercise

1. Create a folder called `venv_practice`. Using only `venv` and `pip`, create and activate a `.venv`, install the `z3-solver` package, and write a short program that imports `z3` and prints `z3.get_version_string()`. Run it, then run `python -m pip freeze > requirements.txt` and look at the file. Deactivate the environment.
2. Install uv. Create a new project with `uv init uv_practice`. Add `z3-solver` with `uv add`, change `main.py` to print the Z3 version, and run it with `uv run main.py`.
3. Open `pyproject.toml` and find your dependency. Compare the version recorded there with the exact version in `uv.lock`.
4. Delete the `.venv` folder in `uv_practice`, then run `uv sync`. What happens?
5. Run `uv add --dev pytest` and look at how `pyproject.toml` changed.

## Reference

- <a href="https://docs.python.org/3/tutorial/venv.html" target="_blank">Virtual Environments and Packages</a>&mdash;Python Tutorial
- <a href="https://docs.python.org/3/library/venv.html" target="_blank">venv — Creation of virtual environments</a>&mdash;Python documentation
- <a href="https://pip.pypa.io/en/stable/" target="_blank">pip documentation</a>&mdash;Python Packaging Authority
- <a href="https://docs.astral.sh/uv/" target="_blank">uv documentation</a>&mdash;Astral
  - <a href="https://docs.astral.sh/uv/getting-started/installation/" target="_blank">Installing uv</a>
  - <a href="https://docs.astral.sh/uv/guides/projects/" target="_blank">Working on projects</a>
- <a href="https://toml.io/en/" target="_blank">TOML: Tom's Obvious Minimal Language</a>&mdash;toml.io
- <a href="https://packaging.python.org/en/latest/guides/writing-pyproject-toml/" target="_blank">Writing your pyproject.toml</a>&mdash;Python Packaging User Guide
- <a href="https://code.visualstudio.com/docs/python/environments" target="_blank">Python environments in VS Code</a>&mdash;Visual Studio Code web site



*Note: Parts of this document were drafted with assistance from Claude Sonnet 5.5 10/7/2026*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
