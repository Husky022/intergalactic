# модуль для сохранения кода, не относящегося напрямую к контроллерам
from datetime import datetime
from os.path import splitext


def get_timestamp_path(isinstance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
