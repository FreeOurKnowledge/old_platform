# Contributing

## Project structure



## Getting Started

1. Build the development image. From the project root:

  sudo docker build . -f ./docker/Dockerfile -t fok_platform
  
  sudo docker-compose -f ./docker/docker-compose.yml up --build -d

2. Check the build is running properly

  sudo docker ps

3. [Configure credentials]??

4. Open a browser to http://localhost:8080/ to view the application (if using Chromebook, go to http://penguin.termina.linux.test:8080/)
