# Dope_Dictionary

#NEW
Web-App TODOs:
- Andrew (file path)
  - Documentation
  - LLM Services
- Jason (file path)
  - HashTableService copy/src/main/java/service/DictionaryService.java
  - here you will see where to put your code :)
 
    Your Pal,
      Quinn :)


TODO:
- Description
- Installation
- Usage

# Installation
## Python Dependencies
This project uses pythons built-in `venv` to manage dependencies. Once the `venv` is activated, one can also just use `pip install -r requirements.txt`. 

This project uses pythons built-in `venv` to manage dependencies. Once the `venv` is activated, one can also just use `pip install -r requirements.txt`. 



### Python Built-in Venv
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

> NOTE: make sure to be in the `django_project` directory when running venv commands

### Pip (local site-packages)
```bash
pip install -r requirements.txt
```

## GoogleGemini API
1. Set up a [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key) account and generate an API key. 
2. Then one must create a `.env` file in the `django_project/project_230/dictionary` directory 
2. Then one must create a `.env` file in the `django_project/project_230/dictionary` directory 
3. Set the `GOOGLE_API_KEY` environment variable to their API key.
> note the `GOOGLE_API_KEY` must be in the `.env` file to use the app. and the API key should also be in "string" format.

Example `.env` file:
```python
GOOGLE_API_KEY="your_api_key_here"
```

## Maven Dependencies
- used for java microservice 
- make sure maven installed

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
    <java.version>21</java.version>
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

## Possibly Other Dependencies



# Known Issues
