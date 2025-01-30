import argparse
import configparser
from ora360.const import CONF_FILE_CANDIDATES


def add_cfg_file_to_candidates(cfg_file):
    if not cfg_file:
        pass
    else:
        CONF_FILE_CANDIDATES.append(cfg_file)


class DB:
    """Database configuration
    """
    host = ''
    port = ''
    service_name = ''
    user = ''
    password = ''


class RPT:
    """Report configuration
    """
    depth = 7


class AppConf:
    def __init__(self, arg=None):
        self.arg = Arg()
        self.arg = arg
        self.db = DB()
        self.rpt = RPT()
        self.run_cfg = configparser.ConfigParser()

    def init_db_cfg(self):
        self.db.host = self.run_cfg.get('db', 'host')
        self.db.port = self.run_cfg.get('db', 'port')
        self.db.service_name = self.run_cfg.get('db', 'service_name')
        self.db.user = self.run_cfg.get('db', 'user')
        self.db.password = self.run_cfg.get('db', 'password')

    def init_rpt_cfg(self):
        self.rpt.depth = self.arg.depth

    def parse(self, conf_file):
        add_cfg_file_to_candidates(self.arg.cfg_file)
        self.run_cfg.read(conf_file)

        self.init_db_cfg()
        self.init_rpt_cfg()


class Arg:
    def __init__(self):
        # Создаем парсер аргументов
        parser = argparse.ArgumentParser(description="Parameters for Ora360", exit_on_error=False)

        # Добавляем аргументы
        parser.add_argument("cfg_file", type=str, help="Parameter file", )
        parser.add_argument("-d", "--depth", type=int, help="Report depth in days", default=7)
        # parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity")

        # Парсим аргументы
        try:
            args = parser.parse_args()
            self.cfg_file = args.cfg_file
            self.depth = args.depth
        except argparse.ArgumentError:
            self.cfg_file = None
            self.depth = 7


aconf = AppConf()

# if __name__ == "__main__":
#     arg = Arg()
#     print(arg.cfg_file)
#     conf = AppConf(arg)
#     conf.parse(CONF_FILE_CANDIDATES)
#     print(CONF_FILE_CANDIDATES)
#     print(conf.db)
