import argparse
from ora360.const import CONF_FILE_CANDIDATES


class Arg:
    def __init__(self):
        # Создаем парсер аргументов
        parser = argparse.ArgumentParser(description="Parameters for Ora360", exit_on_error=False)

        # Добавляем аргументы
        parser.add_argument("cfg_file", type=str, help="Parameter file", )
        # parser.add_argument("-a", "--age", type=int, help="Your age")
        # parser.add_argument("-v", "--verbose", action="store_true", help="Increase verbosity")

        # Парсим аргументы
        try:
            args = parser.parse_args()
            self.cfg_file = args.cfg_file
        except argparse.ArgumentError:
            self.cfg_file = None


if __name__ == '__main__':
    arg = Arg()
    print(arg.cfg_file)
    CONF_FILE_CANDIDATES.insert(0, arg.cfg_file)
    print(CONF_FILE_CANDIDATES)
