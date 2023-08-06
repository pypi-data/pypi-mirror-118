import os
from pathlib import Path
from typing import Tuple

import environ
import logging


def get_paths(file: str) -> Tuple[str, str, str]:
    """
    get the interesting paths w.r.t a django project

    :return: tuple.
        - first is SETTING_DIR (absolute path of the settings.py of the project)
        - second is BASE_DIR: directory where the django PROJECT_DIR is located (both in apps and in project directory)
        - third PROJECT_DIR: directory where settings.py is located
    """
    SETTING_DIR = Path(file).resolve()
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(file).resolve().parent.parent
    PROJECT_DIR = Path(file).resolve().parent
    return SETTING_DIR, BASE_DIR, PROJECT_DIR


def read_env_file(env_file_environment_variable: str = None, default_env_file: str = None, **env_file_default_values) -> environ.Env:
    """
    Read the .env file configuration. You should use it in the settings.py of django.
    We fetch the .env file to load by looking at the environment variabole "env_file_environment_variable". If such an
    environment variable is not found, we will load the file "default_env_file" in the CWD.

    :param env_file_environment_variable: the environment variable to consider
    :param default_env_file: the .env file to load from the CWD to load if no variable named "env_file_environment_variable"
        can be found
    :param env_file_default_values: parameters that are passed as-is in the env file.
    :return: environ.Env
    """
    # ###################################################################################
    # django-environ setup
    # ###################################################################################
    # see https://django-environ.readthedocs.io/en/latest/#settings-py

    env = environ.Env(**env_file_default_values)
    if env_file_environment_variable is None:
        env_file_environment_variable = "ENV_FILE"
    if default_env_file is None:
        default_env_file = "production.env"

    if env_file_environment_variable in os.environ.keys():
        env_file = os.environ.get(env_file_environment_variable)
    else:
        logging.info(f"\"{env_file_environment_variable}\" environment variable not detected. Using the env file \"{default_env_file}\" in the CWD...")
        env_file = default_env_file
    env_file = os.path.abspath(os.path.normcase(env_file))

    logging.info(f"Reading the content of the env file \"{env_file}\"")
    environ.Env.read_env(env_file=env_file)
    return env
