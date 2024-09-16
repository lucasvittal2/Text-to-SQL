from database.mongo import MongoDBHandler


class Config:
    _instance = None
    _mongodb = MongoDBHandler()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def getConfig(cls) -> dict:
        config = cls._mongodb.getCollectionData("config")[0]
        return config