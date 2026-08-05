<h1>Managing Multiple Versions of Python on Linux</h1>

- [Managing Multiple Versions of Python on Linux with pyenv](#managing-multiple-versions-of-python-on-linux-with-pyenv)
- [📦 Installing pyenv](#installing-pyenv)
- [⚙️ Using pyenv](#using-pyenv)
- [🐍 Running Python Programs](#running-python-programs)
- [📂 Virtual Environments with pyenv](#virtual-environments-with-pyenv)
  - [Option 1: pyenv-virtualenv](#option-1-pyenv-virtualenv)
  - [Option 2: Built-in venv](#option-2-built-in-venv)
- [✅ Best Practices](#best-practices)


## Managing Multiple Versions of Python on Linux with pyenv

This guide summarizes best practices for installing and using **pyenv** on Linux (e.g., Ubuntu) to manage multiple Python versions safely and effectively. It covers installation, usage, running Python programs, and setting up virtual environments (`venv`).

---

## 📦 Installing pyenv

1. **Install prerequisites** (needed to build Python from source):
```bash
   sudo apt update
   sudo apt install -y build-essential libssl-dev zlib1g-dev \
       libbz2-dev libreadline-dev libsqlite3-dev curl \
       libncursesw5-dev xz-utils tk-dev libxml2-dev \
       libxmlsec1-dev libffi-dev liblzma-dev
```

2. **Install pyenv**:

```bash
   curl https://pyenv.run | bash
```

3. **Configure your shell** (`~/.bashrc` or `~/.zshrc`):
4. 
   ```bash
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv virtualenv-init -)"
   ```

4. **Reload your shell**:
5. 
   ```bash
   exec $SHELL
   ```

---

## ⚙️ Using pyenv

- **List available versions**:
- 
  ```bash
  pyenv install --list
  ```

- **Install a specific version**:
- 
  ```bash
  pyenv install 3.12.1
  pyenv install 3.9.18
  ```
  > 🔑 Note: You must specify the full version (major.minor.patch).  
  > `pyenv install 3.14` will not automatically install the latest patch release.

- **Set global version** (default for all shells):
- 
  ```bash
  pyenv global 3.12.1
  ```

- **Set local version** (per project, stored in `.python-version`):
- 
  ```bash
  pyenv local 3.9.18
  ```

- **Set shell version** (temporary, for current session):
- 
  ```bash
  pyenv shell 3.10.13
  ```

---

## 🐍 Running Python Programs

- After activating a version, `python` and `pip` point to that interpreter:

  ```bash
  python --version   # Shows active Python version
  pip --version      # Shows pip tied to that Python
  ```

- Best practice: run pip via Python to avoid ambiguity:

  ```bash
  python -m pip install requests
  ```

- To run a script with a specific version:

  ```bash
  pyenv shell 3.12.1
  python myscript.py
  ```

---

## 📂 Virtual Environments with pyenv

You can use either **pyenv-virtualenv** or the built-in `venv` module.

### Option 1: pyenv-virtualenv

1. Install plugin (already included if you used `pyenv.run`).
2. Create a virtual environment:

   ```bash
   pyenv virtualenv 3.12.1 myproject-env
   ```
3. Activate it:
   4
   ```bash
   pyenv activate myproject-env
   ```
4. Deactivate:

   ```bash
   pyenv deactivate
   ```

### Option 2: Built-in venv

1. Ensure the desired Python version is active:

   ```bash
   pyenv shell 3.12.1
   ```
2. Create a venv directory:

   ```bash
   python -m venv venv
   ```
3. Activate it:

   ```bash
   source venv/bin/activate
   ```
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ✅ Best Practices

- **Never replace Ubuntu’s system Python** — it’s required for package management.
- **Use pyenv for development** — safe, flexible, and supports multiple versions.
- **Always use virtual environments** — isolate dependencies per project.
- **Document dependencies** with `requirements.txt` or `pyproject.toml`.
- **Check active interpreter** with `python --version` before installing packages.

---


By Brian Bird, drafted by Windows Copilot (GPT-5), 12/16/2025

