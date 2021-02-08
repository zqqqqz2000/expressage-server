DIALCT = "mysql"

DRIVER = "pymysql"

USERNAME = "root"

PASSWORD = ""

HOST = "127.0.0.1"

PORT = "3306"

DATABASE = "expressage"

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
    DIALCT,
    DRIVER,
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
    DATABASE
)

SECRET_KEY = "123456789"
