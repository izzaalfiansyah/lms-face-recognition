import os


def get_temp_dir():
    path = "assets/temp/"

    if not os.path.exists(path):
        os.makedirs(path)

    return path
