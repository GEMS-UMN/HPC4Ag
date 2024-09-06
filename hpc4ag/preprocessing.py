import pickle
import numpy as np
from sklearn.model_selection import train_test_split

from .utils import download_file, load_pickle, save_pickle

NoDataValue = -9999

def split_train_test(object_ids, test_size=0.2):
    """
    Split the given object IDs into train and test sets.

    Parameters:
        object_ids (list of int): list of IDs of the objects to be split.
        test_size (float, optional): Proportion of the dataset to include in the test split (0.0 to 1.0). Defaults to 0.2.

    Returns:
        list of int, list of int: Lists of the IDs of objects for the train and test set.
    """    
    train_ids, test_ids = train_test_split(object_ids, test_size=test_size, random_state=42)
    return train_ids, test_ids

def band_idx_lookup(band_name, data):
    """
    Allows to select a specific band (channel) from the stack of Sentinel arrays.

    Parameters:
        band_name (str): band name, for example, B04, B08, etc.
        data (array): array stack.

    Returns:
        array: array stack of the band (channel) selected.
    """    
    return data['grid_info'][0]['bands'].index(band_name)

def get_analysis_array(filepath, start_end_dates=None):
    """
    Computes vegetation indices for crop type predictions (NDVI and CIre).

    Parameters:
        filepath (str): The path to the pickle file with Sentinel data sample representing one field.
        start_end_dates (list of str, optional): List of start and end date for analysis,
            formatted as ["yyyy-mm-dd", "yyyy-mm-dd"]. Defaults to None (in that case all dates will be considered).

    Returns:
        array: stack of arrays with NDVI and CIre values for selected (or all) dates.
    """    
    # Load data from the pickled file
    sr_data = load_pickle(filepath)
    # Extract relevant information from the loaded data
    grid = sr_data['samples'][0]['grids'][0]
    mask = grid['mask']
    stack = grid['stack']
    dates = grid['dates']
    if start_end_dates != None:
        dates_selected = [
            dates.index(date) for date in dates if date >= start_end_dates[0] and date <= start_end_dates[1]
        ]
        stack = stack[dates_selected[0]:dates_selected[-1]+1,:,:,:]
    # Extract specific bands from the stack
    b4 = stack[:, band_idx_lookup("B04", sr_data), :, :]
    b5 = stack[:, band_idx_lookup("B05", sr_data), :, :]
    b7 = stack[:, band_idx_lookup("B07", sr_data), :, :]
    b8 = stack[:, band_idx_lookup("B08", sr_data), :, :]
    days2data = stack[:, band_idx_lookup("Days2data", sr_data), :, :]
    # Calculate indices of interest
    ndvi = (b8 - b4)/np.maximum((b8 + b4), 1e-10)
    ndvi[(ndvi<-1)|(ndvi>1)] = NoDataValue
    cire = b7/np.maximum(b5, 1e-10) - 1
    cire[(cire<-1)|(cire>15)] = NoDataValue
    # Stack your array
    analysis_array = np.stack((ndvi, cire), axis=1)
    # Use mask to zero out irrelevant values in the stacked array
    analysis_array[:, :, mask == 0] = NoDataValue
    return analysis_array

def divide_image(array, x_dim=3, y_dim=3):
    """
    Divides larger array into smaller patches.

    Parameters:
        array (array): The input array.
        x_dim (int, optional): X dimension of resulting patches. Defaults to 3.
        y_dim (int, optional): Y dimension of resulting patches. Defaults to 3.

    Returns:
        array: array of resulting patches
    """
    array = array.copy()
    # Get dimensions of the input array
    num_date, channels, height, width = array.shape
    # Define patch dimensions
    patch_height, patch_width = x_dim, y_dim
    # Initialize lists to store patches and their positions
    patches = []
    patch_positions = []
    i = 0
    while i <= height - patch_height:
        j = 0
        while j <= width - patch_width:
            # Initialize patch before extraction
            patch = array[:, :, i:i+patch_height, j:j+patch_width]
            # Check if all elements in the patch are non-zero (not equal to 0)
            if np.all(patch != NoDataValue):
                patches.append(patch.copy())
                patch_positions.append((i, j))
                array[:, :, i:i+patch_height, j:j+patch_width] = NoDataValue  # Mark these positions as used
            j += patch_width if np.all(patch != NoDataValue) else 1
        i += patch_height if np.all(patch != NoDataValue) else 1
    # Convert the list to numpy arrays before returning
    return np.array(patches)

def create_patches(fids, filepath, outfilepath, x_dim=3, y_dim=3,
                   start_end_dates=["2022-05-11", "2022-10-09"]):
    """
    Combines preparatory steps to generate patches (computes vegetation indices, 
    divides arrays into patches, and saves resulting data to a new pickle)

    Parameters:
        fids (list of int): list of IDs to process.
        filepath (str): The path to the pickle file.
        outfilepath (str): The path to the file where the object will be saved.
        x_dim (int, optional): X dimension of resulting patches. Defaults to 3.
        y_dim (int, optional). Y dimension of resulting patches. Defaults to 3.
        start_end_dates (list of str, optional): List containing start and end dates for analysis. Defaults to ["2022-05-11", "2022-10-09"].

    Returns:
        None
    """
    file_dict = {}
    for fid in fids:
        analysis_array = get_analysis_array(
            filepath=download_file(bucket_path='csb/', filename=filepath.format(fid)), 
            start_end_dates=start_end_dates)
        patches = divide_image(analysis_array, x_dim, y_dim)
        file_dict[fid] = patches
    save_pickle(file_dict, outfilepath)
