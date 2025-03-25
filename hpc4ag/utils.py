import os
import pickle
import requests
import tempfile

tmpdir = tempfile.mkdtemp()

def download_file(bucket_url="https://s3.msi.umn.edu/hpc4ag", bucket_path="", filename=""):
    fileurl = '/'.join([bucket_url.strip('/'), bucket_path.strip('/'), filename.strip('/')])
    gemslearningfile = os.path.join('/opt/hpc4ag/data', filename)
    if (os.path.isfile(gemslearningfile)):
        # We've already made this available in the shared area
        return gemslearningfile
    tmpfile = os.path.join(tmpdir, filename)
    if (os.path.isfile(tmpfile)):
        # Assume the file was already fetched once where the code accesses 
        # the file more than once
        return tmpfile
    with requests.get(fileurl, stream=True) as r:
        r.raise_for_status()
        with open(tmpfile, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return tmpfile


def get_tmpdest(filename):
    return os.path.join(tmpdir, filename)


def save_pickle(obj, filepath):
    """
    Saves the given object to a file using pickle serialization.

    Parameters:
        obj (object): The object to be serialized and saved to the file.
        filepath (str): The path to the file where the object will be saved.

    Returns:
        None
    """
    pickle.dump(obj, open(filepath, "wb"))

def load_pickle(filepath):
    """
    Loads an object from a file using pickle deserialization.

    Parameters:
        filepath (str): The path to the file from which the object will be loaded.

    Returns:
        object: The object loaded from the file.
    """
    return pickle.load(open(filepath, "rb"))