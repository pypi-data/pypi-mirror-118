import os
import pickle
import shutil


def default_if_none(value, default):
    return (value
            if (value is not None)
            else default)


def serialise(obj, path):
    """
    Serialises a pickleable object to a file.

    :param obj: the object to serialise.
    :param path: a str - the path to the file.
    """
    with open(path, "wb") as file:
        pickle.dump(obj, file)


def deserialise_from(path):
    """
    Deserialises a pickleable object from a file.

    :param path: a str - the path of the file.
    :returns: the deserialised Python object.
    """
    with open(path, "rb") as file:
        return pickle.load(file)


def remove_dir_if_exists(directory):
    if (os.path.isdir(directory)):
        shutil.rmtree(directory)


def make_or_clear_dir(path):
    if (os.path.isdir(path)):
        shutil.rmtree(path)

    os.mkdir(path)


def verify_dir_exists(d):
    if (not os.path.isdir(d)):
        raise FileNotFoundError(f"'{d}' does not exist!")


def make_dirs(paths):
    for p in paths:
        os.mkdir(p)


def image_name_to_id(name):
    end = name.rfind(".")
    return int(name[:end].lstrip("0"))


def short_name_for(path):
    start = path.rfind(os.sep)
    return path[start + 1:]


def batches_count_for(total_items, batch_size):
    quotient, remainder = divmod(total_items, batch_size)
    return quotient + int(remainder != 0)
