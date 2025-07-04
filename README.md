# Django REST & Nuxt-3 JWT Authentication with Swagger UI (OpenAPI)

## Run Backend (Django)
- Go to the ```backend/``` directotry
    ```bash
    cd backend/
    ```
- Create ```.env``` file and add the following structure
    ```
    DEBUG=True
    SECRET_KEY=your_django_secret_key_here
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,backend,0.0.0.0
    MYSQL_DATABASE=django_db
    MYSQL_USER=django_user
    MYSQL_ROOT_USER=root
    MYSQL_PASSWORD=secure_password
    MYSQL_HOST=db
    MYSQL_PORT=3306
    MYSQL_ROOT_PASSWORD=secure_password
    ```
- Build the docker image
    ```bash
    docker-compose build --no-cache
    ```
- Start the docker container with log in the terminal
    ```bash
    docker-compose up
    ```
    Or,
- Start the docker container without log in the terminal
    ```bash
    docker-compose up -d
    ```
- If you want to stop the container. Just use the following command
    ```bash
    docker-compose down
    ```
### Server Start at
- MySQL: http://localhost:3306
- Django: http://localhost:8000


## Swagger UI (OpenAPI)
#### For the OpenAPI docs, you can find those as follows:
- Schema: http://localhost:8000/api/schema/
- Docs: http://localhost:8000/api/docs/
- Redocs: http://localhost:8000/api/redocs/

    You may also find the all API with Classes in here: http://localhost:8000/api/all-endpoints/

## Run Frontend (Nuxt 3)
- Go to the ```frontend/``` directotry
    ```bash
    cd frontend/
    ```
- Create ```.env``` file and add the following structure
    ```
    SECRET_KEY=my-secret-key
    NUXT_PUBLIC_API_BASE=http://localhost:8000/api/
    ```
- Build the docker image
    ```bash
    docker-compose build --no-cache
    ```
- Start the docker container with log in the terminal
    ```bash
    docker-compose up
    ```
    Or,
- Start the docker container without log in the terminal
    ```bash
    docker-compose up -d
    ```
- If you want to stop the container. Just use the following command
    ```bash
    docker-compose down
    ```
### Nuxt Server Start at
- http://localhost:3000