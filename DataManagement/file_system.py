import os
from pathlib import Path
import shutil
import pandas as pd
import json
import numpy as np
import io
import datetime


def clear_folder_content(folder_path: Path, including_folder: bool = False):
    if not os.path.exists(folder_path):
        return
    print("Deleting folder: ", folder_path)
    for file_path in folder_path.iterdir():
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    if including_folder:
        ensure_dir(folder_path)
        os.rmdir(folder_path)
    print("Folder deleted: ", folder_path)


def ensure_dir(folder_path: Path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def save_to_file(to_save, file_path: Path, additional_info=None):
    ensure_dir(file_path.parent)
    if type(to_save) == pd.DataFrame:
        file_path = file_path if file_path.name.endswith(".csv") else f"{file_path}.csv"
        to_save.to_csv(file_path)
    elif type(to_save) == dict:
        file_path = file_path if file_path.name.endswith(".txt") else f"{file_path}.txt"
        with open(file_path, 'w') as file:
            file.write(json.dumps(to_save, cls=NpEncoder))
    elif type(to_save) == np.ndarray and additional_info["type"] == "image":
        file_path = file_path.as_posix() if file_path.name.endswith(".png") else f"{file_path}.png"
        cv2.imwrite(file_path, to_save)
    else:
        raise NotImplementedError(f"Saving of this type: {type(to_save)} isn't implemented yet. File: {file_path} .")


def load_file(file_path: Path, additional_info: dict = None):
    info = {"type": "json"}
    if additional_info is not None:
        info.update(additional_info)
    if file_path.suffix == ".csv":
        return pd.read_csv(file_path, index_col=0)
    elif file_path.suffix == ".txt" and info["type"] == "json":
        with open(file_path) as f:
            return json.load(f)
    elif file_path.suffix == ".txt" and info["type"] == "lines":
        f = io.open(file_path, "r", encoding="utf-8")
        return f.readlines()
    elif file_path.suffix == ".wav":
        data, sample_rate = librosa.load(file_path, sr=None)
        return sample_rate, data
    else:
        raise NotImplementedError(f"Reading files of this object type isn't implemented yet. File: {file_path} .")


def get_date_time() -> str:
    """
    :return: Used to be part of a file name with current date and time
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
