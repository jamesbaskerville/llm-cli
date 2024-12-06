# LLShell

A LLM-powered CLI to help you do things in the shell.

## Installation

```bash
# optional venv creation
python -m venv venv
source venv/bin/activate
```

```bash
# install dependencies, build, and install
pip install -r requirements.txt
./build.sh
./local-install.sh
```

## Usage

```bash
llshell
```

I used this to spin up a FastAPI server for me -- only issue is that LLShell
didn't background it, so it stopped responding to my input.