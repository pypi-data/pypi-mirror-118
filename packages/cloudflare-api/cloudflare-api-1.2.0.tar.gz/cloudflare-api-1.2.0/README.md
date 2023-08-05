# cloudflare-api

[![Python Package](https://github.com/nikhiljohn10/cloudflare-api/actions/workflows/python-publish.yml/badge.svg)](https://github.com/nikhiljohn10/cloudflare-api/actions/workflows/python-publish.yml) ![PyPI - Status](https://img.shields.io/pypi/status/cloudflare-api) [![PyPI](https://img.shields.io/pypi/v/cloudflare-api)](https://pypi.org/project/cloudflare-api) [![CodeFactor](https://www.codefactor.io/repository/github/nikhiljohn10/cloudflare-api/badge)](https://www.codefactor.io/repository/github/nikhiljohn10/cloudflare-api) [![GitHub license](https://img.shields.io/github/license/nikhiljohn10/cloudflare-api)](https://github.com/nikhiljohn10/cloudflare-api/blob/main/LICENSE)

Python client for Cloudflare API v4

## Usage

### Python Package

```bash
pip install cloudflare-api
```

Sample code can be found inside [/test.py](https://github.com/nikhiljohn10/cloudflare-api/blob/main/test.py) 

### Source Code

```bash
git clone https://github.com/nikhiljohn10/cloudflare-api
cd cloudflare-api
```

Create a `secret.py` in the root directory with following content:
```python
API_TOKEN = ""
ACCOUNT_ID = ""
```
The above variable need to be assigned with your own api token and account id from Cloudflare dashboard.

Then run the following command in terminal:
```bash
make test
```

## Example

For this example, `poetry` is used for easy setup.
```bash
python3 -m pip install poetry
poetry new cloudflare-app
cd cloudflare-app
poetry add cloudflare-api
```

Copy the code below in to a new file `./cloudflare-app/__main__.py`. Then replace `API_TOKEN` & `ACCOUNT_ID` values with values obtained from Cloudflare dashboard.
```python
#!/usr/bin/env python3

from CloudflareAPI import Cloudflare, jsonPrint

API_TOKEN = ""
ACCOUNT_ID = ""

def main():
  cf = Cloudflare(token=API_TOKEN, account_id=ACCOUNT_ID)
  print(cf.worker.list())
  print(cf.store.list())
```

Now we can run our program using following command:
```
poetry run python cloudflare-app
```

## Available endpoints

### Account

- `list` - List all accounts where given token have access
- `get_id` - Return account id if only one account exists. Otherwise display all accounts availabe and exit.
- `details` - Display details of an account
- `rename` - Rename an existing account

### Worker

- `list` - List all existing workers
- `upload` - Upload a new worker with binding if given
- `download` - Download an existing worker
- `deploy` - Deploy an existing worker using the subdomain
- `undeploy` - Undeploy an existing worker
- `delete` - Delete an existing worker

  ### Subdomain

  - `create` - Create a new subdomain if none exists
  - `get` - Get the current subdomain from cloudflare account

### Store(Workers KV)

- `list` - List all existing Namespaces
- `id` - Find the namespace id of the namespace
- `create` - Create a new namespace
- `rename` - Rename an existing namespace
- `delete` - Delete an existing namespace
