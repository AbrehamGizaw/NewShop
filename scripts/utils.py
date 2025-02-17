import os
import json
from django.core.exceptions import ImproperlyConfigured
import glob
import json, logging, os
import shutil
import subprocess
from datetime import datetime

# basic log types matched with log file names
LOG_FILES_BY_TAGNAME = {
    'error': 'error_logs.log',
    'email': 'email_logs.log',
}


def extract_last_names(names_list, split_by):
    return [name.split('.')[-1] if split_by in name else name.split()[-1] for name in names_list]



def load_json_config(path):
    try:
        with open(path) as file:
            loaded_dict = json.load(file)
            INFO(f"The Loaded Data is: {loaded_dict}")
            return loaded_dict
    except FileNotFoundError as e:
        ERROR(f"Config file '{path}' not found. \n\r{e}")
        raise e
    except json.JSONDecodeError as e:
        ERROR(f"Failed to load JSON from file '{path}'. Check if the file contains valid JSON. \n\t {e}")
        raise e
    except Exception as e:
        ERROR(f"An error occurred while loading JSON from file '{path}': {e}")
        raise e



def INFO(message):
    LOGGER.info(f"- {message}")
    print(f"{message}")


def WARNING(message):
    LOGGER.warning(f"- {message}")
    print(f"{message}")


def ERROR(message):
    LOGGER.error(f"- {message}")
    print(f"{message}")


def DEBUG(message):
    LOGGER.debug(f"- {message}")
    print(f"{message}")

def set_logger(name: str, path: str, is_test=False):
    global LOGGER
    LOGGER = logging.getLogger(name)
    try:
        formatter = logging.Formatter(
            '[%(asctime)s:%(levelname)s] || {%(pathname)s Line:%(lineno)d} -- %(message)s'
        )
        filename = os.path.join(path, f'{name}_{datetime.now():%Y%m%d_%H%M%S}.log')
        file_handler = logging.FileHandler(
            filename=filename
        )
        print(f"Log File: {filename}")
        if is_test:
            file_handler.setLevel(logging.DEBUG)
            LOGGER.setLevel(logging.DEBUG)
        else:
            file_handler.setLevel(logging.INFO)
            LOGGER.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        LOGGER.addHandler(file_handler)
        return filename
    except Exception as e:
        print("An error occurred while setting up the logger:", e)
        raise e


def recursive_op_files(source, destination, source_pattern, override=False, skip_dir=True, operation='copy'):
    files_count = 0
    try:
        assert source is not None, 'Please specify source path, Current source is None.'
        assert destination is not None, 'Please specify destination path, Current source is None.'

        if not os.path.exists(destination):
            INFO(f'Creating Dir: {destination}')
            os.mkdir(destination)

        items = glob.glob(os.path.join(source, source_pattern))

        for item in items:

            try:
                if os.path.isdir(item) and not skip_dir:
                    path = os.path.join(destination, os.path.basename(item))
                    # INFO(f'START {operation} FROM {item} TO {path}.')
                    files_count += recursive_op_files(
                        source=item, destination=path,
                        source_pattern=source_pattern, override=override
                    )
                else:
                    file = os.path.join(destination, os.path.basename(item))
                    INFO(f'START {operation} FROM {item} TO {file}.')
                    if not os.path.exists(file) or override:
                        if operation == 'copy':
                            shutil.copyfile(item, file)
                        elif operation == 'move':
                            shutil.move(item, file)
                        else:
                            raise ValueError(f"Invalid operation: {operation}")
                        files_count += 1
                    else:
                        raise FileExistsError(f'The file {file} already exists int the destination path {destination}.')
            except FileNotFoundError as e_file:
                ERROR(f"File not found error: {e_file}")
                print(f"File not found error: {e_file}")
            except PermissionError as e_permission:
                ERROR(f"Permission error: {e_permission}")
                print(f"Permission error: {e_permission}")
            except Exception as e_inner:
                ERROR(f"An error occurred: {e_inner}")
                print(f"An error occurred: {e_inner}")
    except AssertionError as e_assert:
        ERROR(f"Assertion error: {e_assert}")
        print(f"Assertion error: {e_assert}")
    except Exception as e_outer:
        ERROR(f"An error occurred: {e_outer}")
        print(f"An error occurred: {e_outer}")
    return files_count


def convert_to_json(items):
    x = json.dumps(items)


def load_env_config(key, config, env):
    try:
        return config[env][key]
    except KeyError:
        error_msg = "ImproperlyConfigured: Set {0} environment variable".format(key)

    raise ImproperlyConfigured(error_msg)


def load_config(file_path):
    """ Takes config file path as an argument and returns config content as json! """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file {file_path} does not exist.")

    if not file_path.endswith('.json'):
        raise ValueError("Config file must be a JSON file.")

    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Config file is not a valid JSON file.")

    return config
