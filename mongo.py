import re
from typing import Dict, Any

from fastapi import FastAPI
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Нужны таблицы в базе User, User_groups, Groups, Groups_Methods, Methods, User_Methods
# Для каждой группы создавать свою БД


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello world!"}


# Регулярка ^(\/\w[\w_-]*)+(\/)?$
pattern = r'^(\/\w[\w_-]*)+(\/)?$'


@app.post("/set_endpoint")
def set_endpoint(login: str, endpoint: str, data: Dict[str, Any]):
    if not re.fullmatch(pattern, endpoint):
        return {"message": "Не валидный endPoint", "error": True}

    client = MongoClient("localhost", port=27017)
    db = client["mock_test"]
    collection_name = login

    if collection_name not in db.list_collection_names():
        print(f"Коллекция {collection_name} не найдена.")

        # Создаем новую коллекцию
        new_collection = db.create_collection(collection_name)
        print(f"Создана новая коллекция: {new_collection.name}")
    else:
        print(f"Коллекция {collection_name} уже существует.")
    if endpoint[-1] != '/':
        endpoint += '/'

    data = {"endpoint": "/" + login + endpoint, "data": data}
    db[login].insert_many([data])


@app.post("/{full_path:path}")
async def get_data(full_path: str):
    login = full_path.split("/")[0]

    client = MongoClient("localhost", port=27017)
    db = client["mock_test"]
    collection_name = login
    # Переписать проверку...
    if collection_name not in db.list_collection_names():
        return {"message": "Такого endpoint не существует", "error": True}
    print(full_path)
    if full_path[-1] != '/':
        full_path = full_path+'/'

    print(full_path)

    data = db[login].find({
        "endpoint": "/"+full_path
    })

    if data:
        result = data.next()["data"]
        return result
    else:
        return {"message": "Такого endpoint не существует", "error": True}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)