# mongo_manager.py
from pymongo import MongoClient
from typing import Dict, Any, Optional, List


class MongoManager:
    def __init__(self, host="localhost", port=27017, db_name="mock_test"):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        print(f"Подключено к MongoDB: {host}:{port}, БД: {db_name}")

    # Работа с коллекциями (таблицами)
    def collection_exists(self, collection_name: str) -> bool:
        """Проверяет существует ли коллекция"""
        return collection_name in self.db.list_collection_names()

    def create_collection(self, collection_name: str):
        """Создает новую коллекцию"""
        if not self.collection_exists(collection_name):
            self.db.create_collection(collection_name)
            print(f"Создана коллекция: {collection_name}")
            return True
        return False

    def delete_collection(self, collection_name: str):
        """Удаляет коллекцию"""
        if self.collection_exists(collection_name):
            self.db[collection_name].drop()
            print(f"Удалена коллекция: {collection_name}")
            return True
        return False

    def get_all_collections(self) -> List[str]:
        """Возвращает список всех коллекций"""
        return self.db.list_collection_names()

    # Работа с записями (документами)
    def insert_one(self, collection_name: str, data: Dict[str, Any]) -> str:
        """Добавляет одну запись"""
        result = self.db[collection_name].insert_one(data)
        return str(result.inserted_id)

    def insert_many(self, collection_name: str, data: List[Dict[str, Any]]) -> List[str]:
        """Добавляет несколько записей"""
        result = self.db[collection_name].insert_many(data)
        return [str(id) for id in result.inserted_ids]

    def find_one(self, collection_name: str, filter: Dict[str, Any]) -> Optional[Dict]:
        """Находит одну запись по фильтру"""
        return self.db[collection_name].find_one(filter)

    def find_many(self, collection_name: str, filter: Dict[str, Any]) -> List[Dict]:
        """Находит несколько записей по фильтру"""
        return list(self.db[collection_name].find(filter))

    def find_by_endpoint(self, collection_name: str, endpoint: str) -> Optional[Dict]:
        """Специальный метод для поиска по endpoint (как в вашем коде)"""
        result = self.db[collection_name].find_one({"endpoint": endpoint})
        if result and "_id" in result:
            result["_id"] = str(result["_id"])  # Преобразуем ObjectId в строку
        return result

    def update_one(self, collection_name: str, filter: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Обновляет одну запись"""
        result = self.db[collection_name].update_one(filter, {"$set": data})
        return result.modified_count > 0

    def delete_one(self, collection_name: str, filter: Dict[str, Any]) -> bool:
        """Удаляет одну запись"""
        result = self.db[collection_name].delete_one(filter)
        return result.deleted_count > 0

    def delete_many(self, collection_name: str, filter: Dict[str, Any]) -> int:
        """Удаляет несколько записей по фильтру"""
        result = self.db[collection_name].delete_many(filter)
        return result.deleted_count

    def delete_by_endpoint(self, collection_name: str, endpoint: str) -> bool:
        """Удаляет запись по endpoint"""
        result = self.db[collection_name].delete_one({"endpoint": endpoint})
        return result.deleted_count > 0

    def count_records(self, collection_name: str, filter: Dict[str, Any] = None) -> int:
        """Считает количество записей"""
        filter = filter or {}
        return self.db[collection_name].count_documents(filter)

    def clear_collection(self, collection_name: str):
        """Очищает коллекцию (удаляет все записи)"""
        self.db[collection_name].delete_many({})
        print(f"Коллекция {collection_name} очищена")

    def close(self):
        """Закрывает соединение"""
        self.client.close()
        print("Соединение с MongoDB закрыто")