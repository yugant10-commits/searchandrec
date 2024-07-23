# searchandrec
Can be used to rank search and give recommendation

## Setup virtual env and install dependencies

1. Install poetry
```
pip install poetry
```

2. Change config to create virtual env in the project directory
```
poetry config virtualenvs.in-project true                                                                             
```

3. Create env and install dependencies
```
poetry install
```

4. Activating Env
```
poetry shell
```

## Run the server 
```
cd app
uvicorn main:app --reload    
```