import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(64)
    # auto-submit
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    MAIL_SUBJECT_PREFIX = "API-Feedback"
    MAIL_SENDER = "API admin <luochong@gufengxiaoyuehan.xyz>"
    API_ADMIN = os.environ.get("API_ADMIN") or "luochong@gufengxiaoyuehan.xyz"

    MONGOALCHEMY_DATABASE = "geoinfos"
    MONGOALCHEMY_SERVER = "104.128.235.71"
    MONGOALCHEMY_USER = "logan"
    MONGOALCHEMY_PASSWORD = os.environ.get("MONGOALCHEMY_PASSWORD")
    MONGOALCHEMY_SERVER_AUTH = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    MAIL_SERVER = "smtp.gufengxiaoyuehan.xyz"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or "luochong@gufengxiaoyuehan.xyz"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or "sqlite:///" + os.path.join(basedir,"data-dev.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "data-test.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "data.sqlite")
    MAIL_SERVER = "smtp.gufengxiaoyuehan.xyz"
    MAIL_PORT = 25

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}