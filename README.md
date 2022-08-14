## Features

Extracts person names from [Notion]-sites constructed using [Super].

> **Warning**\
> [Wraptas], etc. are not supported.

## Getting started

### 1. Install Python

Use [pyenv] for Python version management.

```shell
pyenv install
```

### 2. Install dependencies

Use [venv] for virtual environments.

```shell
python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

deactivate
```

### 3. Setup .env

```shell
cat <<EOF > .env
TARGET_URL={Notion-site URL}
EOF
```

### 4. Run

```shell
source venv/bin/activate

python main.py

deactivate
```

<!-- Links -->
[Notion]: https://www.notion.so
[Super]: https://super.so
[Wraptas]: https://wraptas.com
[pyenv]: https://github.com/pyenv/pyenv
[venv]: https://docs.python.org/3/library/venv.html
