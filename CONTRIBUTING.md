# Contributing

## Project structure



## Getting Started

1. Building the development image

From the project root:

  docker build . -f docker/Dockerfile -t fok_platform

2. [Configure credentials]

3. Start the service within the container. (probably something like this:)

  docker run fok_platform /src/manage.py startapp
  
4. ???

5. Open a browser to http://localhost:8080/ (maybe ?) to view the application.
