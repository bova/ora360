import os
from pathlib import Path


CONF_FILE_CANDIDATES = ['/etc/ora360/ora360.ini',
                        'c:\\ora360\\ora360.ini',
                        os.path.join(Path.home(), 'PycharmProjects', 'ora360', 'ora360.ini')]