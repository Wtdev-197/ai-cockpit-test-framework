# Environment Deployment Guide

## 1. Prerequisites

- Windows PowerShell, macOS, or Linux shell
- Python 3.10 or newer; Python 3.11 is recommended
- Git
- Network access to install Python packages

Check versions:

```powershell
python --version
git --version
```

## 2. Get the Source Code

```powershell
git clone <repository-url>
cd ai-cockpit-test-framework
```

Replace `<repository-url>` with the repository URL supplied by the team.

## 3. Create and Activate a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, call the interpreter directly:

```powershell
venv\Scripts\python.exe -m pip install --upgrade pip
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify the tools:

```powershell
python -m pytest --version
python -m robot --version
```

## 5. Configure Runtime Mode

No `.env` file is required for the default Mock mode. The defaults are:

```text
RUN_MODE=mock
LLM_PROVIDER=mock
```

For local experiments, create `.env` in the repository root. Never commit API keys or other secrets.

## 6. Run Tests

```powershell
python -m pytest -v
python -m robot --outputdir results tests/acceptance/
```

See [testing.md](testing.md) for every supported command and test inventory.

## 7. Test Artifacts

- pytest output is shown in the terminal.
- pytest file logs are configured for `logs/pytest.log` by `pytest.ini`.
- Robot Framework writes `output.xml`, `log.html`, and `report.html` to `results/` with `--outputdir results`.

## 8. Troubleshooting

### `No module named pytest`

The command is using a Python interpreter without project dependencies. Activate `venv`, or call it explicitly:

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m pytest -v
```

### `No module named src.cockpit`

Run commands from the repository root and ensure the package directory is named `src/cockpit`, not `src/cockpit-ivi`.
