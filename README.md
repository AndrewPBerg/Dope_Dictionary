# Installation

## Python Dependencies
This project uses pythons built-in `venv` to manage dependencies. Once the `venv` is activated, one can also just use `pip install -r requirements.txt`. 


### Python Built-in `venv`
> Make sure to be in the `django_project` directory when running venv commands
```bash
cd django_project
```

> MacOS/Linux
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

> Windows
```bash
python -m venv myenv
.\myenv\Scripts\activate
pip install -r requirements.txt
```

## GoogleGemini API
1. Set up a [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key) account and generate an API key. 
2. create a `.env` file in the `django_project/project_230/dictionary` directory 
3. Set the `GOOGLE_API_KEY` environment variable to their API key.

> note the `GOOGLE_API_KEY` must be in the `.env` file to use the app. and the API key should also be in "string" format.

Example `.env` file:
```python
# .env
GOOGLE_API_KEY="your_api_key_here"
```

## Maven Dependencies
- used for the Java microservice 
> Make sure to be in the `HashTableService` directory when running maven commands
> Make sure maven is installed

```bash
mvn --version
```
> if not installed, install maven from [here](https://maven.apache.org/download.cgi)

### Start Maven Service
```bash
cd HashTableService
```
```bash
mvn clean compile
```
> NOTE: make sure that the current java version is supported by the maven `pom.xml` file in the 
```xml
<properties>
    <java.version>example_version</java.version>
</properties>
```
> To check the current java version, run 
```bash 
java -version
```


> Start the maven service
```bash
mvn spring-boot:run
```

# Quick Start

## Quick Commands

> Activate the python `venv`
```bash
cd django_project
.\myenv\Scripts\activate
```

> Start the django server
```bash
cd project_230
python manage.py runserver
```


> In a different Terminal, Start the maven service
```bash
cd HashTableService
mvn spring-boot:run
```