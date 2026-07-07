# Login / Cart / Logout Automation Framework

Selenium + pytest automation framework for [Sauce Demo](https://www.saucedemo.com) covering login, add to cart, logout, and full end-to-end flow.

## Features

- **Page Object Model** — locators and actions live in `pages/`
- **Data-driven tests** — credentials and products from Excel
- **Cross-browser** — Chrome and Firefox
- **Parallel execution** — pytest-xdist (`-n auto`)
- **Reporting** — HTML report, file logs, pass/fail screenshots
- **Negative tests** — wrong password and locked-out user

## Project Structure

```
Login_Cart_Logout_Framework/
├── Configurations/config.ini    # App URL, Excel path, default user
├── Data/test_data.xlsx          # Users and products test data
├── pages/                       # Page Object classes
├── tests/                       # Pytest test files
├── utilities/                   # Config reader, Excel, logger, helpers
├── run.bat                      # Windows test runner (menu)
├── pytest.ini                   # Pytest settings
└── requirements.txt             # Python dependencies
```

## Setup

### 1. Prerequisites

- Python 3.10+
- Google Chrome or Mozilla Firefox installed

### 2. Install dependencies

```powershell
cd Login_Cart_Logout_Framework
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Test data

`Data/test_data.xlsx` contains:

| Sheet    | Columns                          |
|----------|----------------------------------|
| Users    | Username, Password               |
| Products | Product Name, Price, Add To Cart ID |

Default user: `standard_user` / `secret_sauce`

## Run Tests

### Windows — double-click

```
run.bat
```

Menu options:

| # | Mode |
|---|------|
| 1 | Sequential — Chrome |
| 2 | Sequential — Firefox |
| 3 | Parallel — Chrome |
| 4 | Parallel — Firefox |
| 5 | Parallel — Chrome + Firefox |

### Command line

```powershell
# All tests on Chrome
pytest -s -v tests/ --browser chrome

# Parallel on both browsers
pytest -n auto tests/ --browser both
```

## Output

| Output | Location |
|--------|----------|
| HTML report | `Reports/report.html` |
| Logs | `Logs/Automation_Logs.log` |
| Screenshots | `Screenshots/` |

## Test Files

| File | Purpose |
|------|---------|
| `test_login.py` | Verify inventory page after login |
| `test_login_negative.py` | Wrong password, locked-out user |
| `test_add_to_cart.py` | Add products from Excel (parametrized) |
| `test_logout.py` | Logout returns to login page |
| `test_full_flow.py` | Login → cart → logout in one test |
