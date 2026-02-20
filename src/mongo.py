import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Optional, Dict, List, Any, Union
from datetime import datetime
import logging


class MongoManager:

    def __init__(self, connection_string: str, database_name: str):
        """
        Инициализация подключения к MongoDB

        Args:
            connection_string: Строка подключения к MongoDB
            database_name: Имя базы данных
            timeout_ms: Таймаут подключения в миллисекундах
            max_pool_size: Максимальный размер пула соединений
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: Optional[MongoClient] = None
        self.db = None
        self.timeout_ms = 5000
        self.max_pool_size = 100
        self.logger = logging.getLogger(__name__)


    def connect(self) -> bool:
        """
        Установка соединения с MongoDB

        Returns:
            bool: True если соединение успешно установлено
        """
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=self.timeout_ms,
                maxPoolSize=self.max_pool_size
            )
            # Проверка соединения
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            self.logger.info(f"Успешно подключено к MongoDB: {self.database_name}")
            return True

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            self.logger.error(f"Ошибка подключения к MongoDB: {e}")
            return False

    def disconnect(self):
        """Закрытие соединения с MongoDB"""
        if self.client:
            self.client.close()
            self.logger.info("Соединение с MongoDB закрыто")

    def __enter__(self):
        """Контекстный менеджер для подключения"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения"""
        self.disconnect()

    def create_collection_if_not_exists(self, collection_name: str) -> bool:
        """
        Создание коллекции, если она не существует

        Args:
            collection_name: Имя коллекции

        Returns:
            bool: True если коллекция создана или уже существует
        """
        try:
            if collection_name in self.db.list_collection_names():
                self.logger.info(f"Коллекция {collection_name} уже существует")
                return True

            self.db.create_collection(collection_name)
            self.logger.info(f"Коллекция {collection_name} создана")
            return True

        except Exception as e:
            self.logger.error(f"Ошибка при создании коллекции {collection_name}: {e}")
            return False


    def drop_collection(self, collection_name: str, confirm: bool = False) -> bool:
        """
        Удаление коллекции

        Args:
            collection_name: Имя удаляемой коллекции
            confirm: Подтверждение удаления (для защиты от случайного удаления)

        Returns:
            bool: True если коллекция успешно удалена
        """
        if not confirm:
            self.logger.warning(f"Удаление коллекции {collection_name} не подтверждено. "
                                f"Установите confirm=True для подтверждения")
            return False

        try:
            # Проверяем существование коллекции
            if collection_name not in self.db.list_collection_names():
                self.logger.warning(f"Коллекция {collection_name} не существует")
                return False

            # Удаляем коллекцию
            self.db[collection_name].drop()
            self.logger.info(f"Коллекция {collection_name} успешно удалена")
            return True

        except Exception as e:
            self.logger.error(f"Ошибка при удалении коллекции {collection_name}: {e}")
            return False


    def insert_one(self, collection: str, document: Dict[str, Any]) -> Optional[str]:
        """
        Вставка одного документа

        Args:
            collection: Имя коллекции
            document: Документ для вставки

        Returns:
            Optional[str]: ID вставленного документа или None
        """
        try:
            # Добавляем временные метки
            document['created_at'] = datetime.now()
            document['updated_at'] = datetime.now()

            result = self.db[collection].insert_one(document)
            self.logger.info(f"Документ вставлен в {collection} с ID: {result.inserted_id}")
            return str(result.inserted_id)

        except Exception as e:
            self.logger.error(f"Ошибка при вставке документа: {e}")
            return None

    def find_one(self, collection: str, endpoint_id: int) -> Optional[Dict[str, Any]]:
        try:
            query = {"endpoint_id": endpoint_id}
            result = self.db[collection].find_one(query)

            if result and '_id' in result:
                result['_id'] = str(result['_id'])

            if result:
                self.logger.info(f"Найдена эндпоинт '{endpoint_id}' в коллекции {collection}")
            else:
                self.logger.info(f"Группа '{endpoint_id}' не найдена в коллекции {collection}")

            return result

        except Exception as e:
            self.logger.error(f"Ошибка при поиске эндпоинта '{endpoint_id}': {e}")
            return None

    def update_one(self, collection: str, query: Dict[str, Any],
                   update: Dict[str, Any], upsert: bool = False) -> bool:
        """
        Обновление одного документа

        Args:
            collection: Имя коллекции
            query: Запрос для поиска
            update: Данные для обновления
            upsert: Создать документ если не найден

        Returns:
            bool: True если обновление успешно
        """
        try:
            # Добавляем время обновления
            if '$set' in update:
                update['$set']['updated_at'] = datetime.now()
            else:
                update['$set'] = {'updated_at': datetime.now()}

            result = self.db[collection].update_one(query, update, upsert=upsert)

            if result.matched_count > 0:
                self.logger.info(f"Обновлен документ в {collection}")
                return True
            elif upsert and result.upserted_id:
                self.logger.info(f"Создан новый документ в {collection} с ID: {result.upserted_id}")
                return True
            else:
                self.logger.warning(f"Документ для обновления не найден в {collection}")
                return False

        except Exception as e:
            self.logger.error(f"Ошибка при обновлении документа: {e}")
            return False

    def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        """
        Удаление одного документа

        Args:
            collection: Имя коллекции
            query: Запрос для поиска

        Returns:
            bool: True если удаление успешно
        """
        try:
            result = self.db[collection].delete_one(query)
            if result.deleted_count > 0:
                self.logger.info(f"Удален документ из {collection}")
                return True
            else:
                self.logger.warning(f"Документ для удаления не найден в {collection}")
                return False

        except Exception as e:
            self.logger.error(f"Ошибка при удалении документа: {e}")
            return False
