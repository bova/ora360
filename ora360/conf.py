import configparser
from ora360.const import CONF_FILE_CANDIDATES


class DB:
    """Database configuration
    """
    host = ''
    port = ''
    service_name = ''
    user = ''
    password = ''


class AppConf:
    def __init__(self):
        self.db = DB()
        self.run_cfg = configparser.ConfigParser()

    def init_db_cfg(self):
        self.db.host = self.run_cfg.get('db', 'host')
        self.db.port = self.run_cfg.get('db', 'port')
        self.db.service_name = self.run_cfg.get('db', 'service_name')
        self.db.user = self.run_cfg.get('db', 'user')
        self.db.password = self.run_cfg.get('db', 'password')

    def parse(self, conf_file):
        self.run_cfg.read(conf_file)

        self.init_db_cfg()

if __name__ == "__main__":
    conf = AppConf()
    conf.parse(CONF_FILE_CANDIDATES)
    print(conf.db)
