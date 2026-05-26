Для введения в эксплуатацию:

1) Склонировать: репозитории в отдельную папку

```sh
git clone https://github.com/SergDC101/front_mock_service.git
git clone https://github.com/SergDC101/hse_mock_service.git
```

2) Создать файл docker-compose.yml

```yml
services:
  db_dev:
    container_name: db_dev
    image: postgres:14
    restart: always
    ports:
      - 5433:5432
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      DB_NAME: postgres
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    networks:
      - postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  pgadmin:
    container_name: pgadmin
    restart: always
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: noemail@noemail.com
      PGADMIN_DEFAULT_PASSWORD: root
    ports:
      - "5050:80"
    networks:
      - postgres
   

  mongo_db:
    container_name: mongo_db
    image: mongo:latest
    restart: always
    ports:
      - "27017:27017"
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - postgres

  app:
    build:
      context: ./hse_mock_service/.
    restart: unless-stopped
    container_name: mock_service
    command: [ "/mock_service/docker/app.sh" ]
    ports:
      - "8086:8086"
    environment:
      - DB_HOST=db_dev
      - DB_PORT=5432
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASS=postgres
      - MONGO_HOST=mongo_db
      - MONGO_PORT=27017
      - MONGO_BASE=mock_test
      - SECRET_AUTH=KJNKJEFBHJWEF"OBFKjnsdkjdfb;fk2378234
    depends_on:
      db_dev:
        condition: service_healthy
      mongo_db:
        condition: service_healthy
    networks:
      - postgres
  
  frontend:
    build:
      context: ./front_mock_service/.
      dockerfile: Dockerfile
    container_name: front_mock_service
    ports:
      - "3000:80"
    depends_on:
      - app
    restart: always
    networks:
      - postgres

networks:
  postgres:
    driver: bridge

```

3) Запустить команду 

```sh
docker compose up -d --build
```