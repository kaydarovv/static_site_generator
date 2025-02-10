import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def copy_recursively(source: str, destination: str) -> None:
    if not os.listdir(source):
        logger.info(f"Checking if directory {source} is empty...")
        return
    for item in os.listdir(source):
        full_path_item = os.path.join(source, item)
        if os.path.isfile(full_path_item):
            file = full_path_item
            shutil.copy(file, destination)
            logger.info(f"Copying file - {file} from {source} to {destination}")

        if os.path.isdir(full_path_item):
            folder = os.path.join(destination, item)
            os.mkdir(folder)
            logger.info(f"Made directory - {folder}")
            copy_recursively(full_path_item, folder)

def source_to_destination(source: str, destination: str) -> None:
    if not os.path.exists(destination):
        raise Exception("destination folder path in invalid or doesn't exist")
    logger.info(f"Cleaning {destination} that contains: {os.listdir(destination)}")
    shutil.rmtree(destination)
    os.mkdir(destination)
    logger.info(f"Cleaning of {destination} finished: {os.listdir(destination)}")

    if not os.path.exists(source):
        raise Exception("source folder path is invalid or doesn't exist")
    logger.info(f"Starting copying from {source} to {destination}")
    copy_recursively(source, destination)