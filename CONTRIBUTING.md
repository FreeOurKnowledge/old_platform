# Contributing

## Project structure

```
platform
├── free_our_knowledge
│   ├── __init__.py
│   ├── settings
│   ├── resources
│   ├── urls.py
│   └── wsgi.py
├── docker
│   └── Dockerfile
│   └── docker-compose.yml
│   └── entrypoint.sh
├── manage.py
└── requirements.txt
```

## Getting Started


### Development installation

1. CLone the repository locally:

```
git clone git@github.com:FreeOurKnowledge/platform.git
```

2. Create a new virtual environment and activate it:

```
python3 -m venv fok_env
source fok_env/bin/activate
```

3. Install all of the dependencies:

```
pip install -r requirements.txt
```

4. Generate the database tables:

```
python manage.py migrate --noinput
```

4. Start the project:

```python
  python manage.py runserver
```

If everything works the platform should be available on http://127.0.0.1:8000/.

### Docker installation

1. Build the development image. From the project root:

  sudo docker build . -f ./docker/Dockerfile -t fok_platform
  
  sudo docker-compose -f ./docker/docker-compose.yml up --build -d

2. Check the build is running properly

  sudo docker ps

3. [Configure credentials]??

4. Open a browser to http://localhost:8080/ to view the application (if using Chromebook, go to http://penguin.termina.linux.test:8080/)


