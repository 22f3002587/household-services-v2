class Config:
    SQLALCHEMY_DATABASE_URI="sqlite:///database.sqlite3"
    DEBUG = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'mysecretsaltwithsalt'
    SECRET_KEY= "shouldbekeptveryhidden"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION = True
    SECURITY_TOKEN_AUTHENTICATION_HEADER='Authorization'
    SECURITY_TOKEN_AUTHENTICATION_METHODS = ["Token"]


    CACHE_DEFAULT_TIMEOUT = 300
    DEBUG = True
    CACHING_TYPE = "RedisCache"
    CACHE_REDIS_PORT = 6379


    CELERY = {
        "broker_url": "redis://localhost:6379/0",
        "result_backend": "redis://localhost:6379/1",
        "timezone": "Asia/Kolkata",
        "task_ignore_result": True
    }