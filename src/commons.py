import json
from datetime import datetime, timezone
from os.path import exists
from os import environ, makedirs
from threading import current_thread
from typing import Optional

import spacy

from .env import env
from .enums import Paths

nlp = spacy.load('en_core_web_sm')


def read(path, mode='r', encoding='utf-8'):
    if exists(path):

        kwargs = dict(
            file=path,
            mode=mode,
            encoding=encoding
        )

        if mode.endswith('b'):
            del kwargs['encoding']

        with open(**kwargs) as f:
            return f.read()


def makedirs_from_path(path: str):
    if not exists(path):
        dir_path = '/'.join(path.split('/')[:-1])
        if not exists(dir_path):
            makedirs(dir_path)


def write(path, contents, mode='w', encoding='utf-8'):
    makedirs_from_path(path)

    kwargs = dict(
        file=path,
        mode=mode,
        encoding=encoding
    )

    if mode.endswith('b'):
        del kwargs['encoding']

    with open(**kwargs) as f:
        f.write(contents)


def try_load_json(o):
    try:
        return json.loads(o)
    except Exception:
        return {}


def now():
    return datetime.now(timezone.utc)


def _log(message, level: str = 'info'):
    _env = 'ENV: ' + str(env()).upper().ljust(10)
    level = level.upper().ljust(10)
    timestamp = now().isoformat().ljust(36)
    thread_name = 'THREAD: ' + current_thread().name.ljust(25)

    message = timestamp + _env + thread_name + level + message
    print(message)
    message += '\n'
    write(str(Paths.LOGGING), message, mode='a')


def info(message):
    _log(message, 'info')


def error(message: str, exception: Optional[Exception] = None):
    if exception:
        message = message.strip().removesuffix('.') + f'. Exception: {type(exception).__name__} - {str(exception)}'
    _log(message, 'error')


def success(message):
    _log(message, 'success')


# TODO - Need to use json to manage subprocesses with os.getpid() when pipelines need to run concurrently


def set_env_to_prod():
    environ['ML_STUDIES_ENV'] = 'prod'
    info('Working environment set to prod.')


def set_env_to_dev():
    environ['ML_STUDIES_ENV'] = 'dev'
    info('Working environment set to dev.')


def set_current_pipeline_var(value: str):
    key = 'CURRENT_PIPELINE'
    info(f'Setting {key} env variable to: {value}')
    environ[key] = value


def set_current_worker_var(value: str):
    key = 'CURRENT_WORKER'
    info(f'Setting {key} env variable to: {value}')
    environ[key] = value
