# LingTab Backend

A backend service for LingTab, an app which plays two roles:

-   Keeping track of what Ian owes me
-   Understanding how Flutter interfaces with a web-based API

This backend is written with the following technologies:

-   Django REST Framework
-   Tailwind
-   Docker

To run the app, simply run:

```
docker compose up --build
```

To run a dev environment, simply run:

```
docker compose -f "docker-compose.dev.yml" up --build
```

The env file should have necessary information about the environment. example.env gives an example of what variables are necessary to build the project.

If debug is set to true in the .env file, tailwind will be in development mode. To run tailwind, enter the web container and start it using the following commands:

```
docker exec -it lingtab-backend /bin/bash
```

```
python manage.py tailwind start
```
