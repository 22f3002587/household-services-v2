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