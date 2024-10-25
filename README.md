# Dope_Dictionary
TODO:
- Description
- Installation
- Usage

# Installation
## Python Dependencies
This project uses `poetry` to manage dependencies. One can also just use `pip install -r requirements.txt`. 
If you are using poetry, run `poetry install` to install the dependencies.

### Poetry
> to install poetry, run `pipx install poetry` or see [poetry installation](https://python-poetry.org/docs/#installation) for specifics.
```bash
poetry install
```
> use poetry to run python scripts

```bash
poetry run python example.py
```


### Python Built-in Venv
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```
> here one can run python scripts once inside the venv with
```bash
source myenv/bin/activate
python example.py
```

### Pip (local site-packages)
```bash
pip install -r requirements.txt
```

> here one can run python scripts normally with 
```bash
python example.py
```

## GoogleGemini API
1. Set up a [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key) account and generate an API key. 
2. Then one must create a `.env` file in the root directory 
3. Set the `GOOGLE_API_KEY` environment variable to their API key.
> note the `GOOGLE_API_KEY` must be in the `.env` file to use the app. and the API key should also be in "string" format.

## Gradle Dependencies
This is a Jason or Quinn area of expertise.
## Possibly Other Dependencies

# Usage

To run the app, one can use the following command:


...
