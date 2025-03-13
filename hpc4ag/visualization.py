import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib.colors import ListedColormap
from datetime import datetime
import seaborn as sns
from datetime import datetime

from .preprocessing import get_analysis_array
from .utils import download_file, load_pickle

crop_colors = ["#FFD400", "#267000", "#A800E3", "#D9B56B"]
crop_types = ["Corn", "Soybeans", "Sugarbeets", "Spring Wheat"]
crop_colors_dict = dict(zip(crop_types, crop_colors))
NoDataValue = -9999

def map_training_labels(gdf, column_name):
    """
    Plots a map of training fields.

    Parameters:
        gdf (geopandas.GeoDataFrame): A GeoDataFrame containing geometries and label information.
        column_name (str): The name of the column in `gdf` containing the labels.

    Returns:
        None
    """
    #print (crop_types)
    crop_types = sorted(list(gdf[column_name].unique()))
    #cmap = ListedColormap([crop_colors[crop_types.index(crop)] for crop in crop_types])
    cmap = ListedColormap([crop_colors_dict[crop] for crop in crop_types])
    fig, ax = plt.subplots(figsize=(8,4), tight_layout=True)
    gdf.plot(column=column_name, legend=True, cmap=cmap, legend_kwds={"bbox_to_anchor":(1.4, 1)}, ax=ax)
    plt.title("Data labels and boundaries", weight="bold")
    plt.show()
    

def plot_sample_distribution (gdf, column_name):
    """
    Plots a distribution of training fields as a bar plot.

    Parameters:
        gdf (geopandas.GeoDataFrame): A GeoDataFrame containing geometries and label information.
        column_name (str): The name of the column in `gdf` containing the labels.

    Returns:
        None
    """
    category_counts = gdf[column_name].value_counts()
    
    # Plotting the histogram with custom colors
    plt.figure(figsize=(6, 2.5), tight_layout=True)
    bars =  category_counts.plot(
        kind="bar",
        color=[crop_colors_dict.get(cat, "grey") for cat in category_counts.index])
    plt.title("Data distribution", weight="bold")
    plt.xlabel("Crop Type")
    plt.xticks(rotation=0)
    sns.despine()
    # Adding numeric values on top of each bar
    for bar in bars.patches:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{int(bar.get_height())}', 
             ha='center', va='bottom') 
    plt.show()


def map_timeseries_oneband(array, band_index, dates):
    """
    Plots the sample grid of a single band of stacked array at each time step.

    Parameters:
        array (array-like): Input array to display.
        band_index (int): Index of band of interest to plot.
        dates (list of str): List of strings for each time step.

    Returns:
        None
    """
    fig = plt.figure(figsize=(25, 25))
    positions = list(range(0, array.shape[0]))
    dates = [datetime.strptime(dateString, "%Y-%m-%d").date() for dateString in dates]
    for position, date in zip(positions, dates):
        plt.subplot(8, 8, position + 1)
        plt.imshow(array[position,band_index,:,:], cmap="pink_r")
        plt.title(f'{date}', style="italic")
        plt.colorbar()
        plt.axis("off")
    plt.tight_layout()
    plt.show()

    
def plot_indices_temporal(selected_fields, filepath):
    """
    Plots the NDVI and CIre of selected fields as subplots.

    Parameters:
        selected_fields (dict): Dictionary with structure {'crop' : fid}.
        filepath (str): The path to the pickle file with Sentinel data sample representing one field.

    Returns:
        None
    """
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 5), tight_layout=True)

    for crop, fid in selected_fields.items():
        pickle_path=download_file(bucket_path='csb/', filename=filepath.format(fid))
        grid = load_pickle(filepath=pickle_path)["samples"][0]["grids"][0]
        dates = [datetime.strptime(dateString, "%Y-%m-%d").date() for dateString in grid['dates']]
        # get indices
        stack = get_analysis_array(filepath=pickle_path)
        stack[stack==NoDataValue]=np.nan
        ndvi = stack[:, 0, :, :]
        ndvi_med = [np.nanmedian(ndvi[timestep]) for timestep in range(0, ndvi.shape[0])]
        cire = stack[:, 1, :, :]
        cire_med = [np.nanmedian(cire[timestep]) for timestep in range(0, cire.shape[0])]
    
        axs[0].plot(dates, ndvi_med, label=crop, color=crop_colors_dict[crop], marker="o")
        axs[1].plot(dates, cire_med, label=crop, color=crop_colors_dict[crop], marker="o")

    axs[0].legend(ncol=4, loc="upper left")
    axs[0].set_title("Normalized Difference Vegetation Index (NDVI)", weight="bold")
    axs[1].set_title("Red-edge Chlorophyll Index (CIre)", weight="bold")

    plt.show()
    
def plot_confusion_matrix(y_true, y_pred, display_labels):
    """
    Plots the confusion matrix and the normalized confusion matrix as subplots.

    Parameters:
        y_true (array-like): Ground truth (correct) values.
        y_pred (array-like): Estimated values as returned by a classifier.
        display_labels (array-like): Common names used for plotting.

    Returns:
        None
    """
    fig, axs = plt.subplots(1,2, figsize=(10,4), tight_layout=True)
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=display_labels)
    disp.plot(cmap="RdPu", ax=axs[0])
    axs[0].set_title("Confusion Matrix", weight="bold")
    cm_normalized = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm_normalized, display_labels=display_labels)
    disp.plot(cmap="RdPu", ax=axs[1])
    axs[1].set_title("Normalized Confusion Matrix", weight="bold")
    for ax in [0,1]:
        plt.setp(axs[ax].get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    plt.show()

def plot_learning_history(history):
     """
    Plots the training and validation accuracy and loss at each epoch.

    Parameters:
        history: Model fitting history after training.

    Returns:
        None
    """
    #plot the training and validation IoU and loss at each epoch
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(loss) + 1)
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    fig, axs = plt.subplots(1, 2, figsize=(10,3), tight_layout=True)
    axs[0].plot(epochs, loss, label='Training loss')
    axs[0].plot(epochs, val_loss, label='Validation loss')
    axs[0].set_title('Training and validation loss', weight="bold")
    axs[0].set_xlabel('Epochs')
    axs[0].set_ylabel('Loss')
    axs[0].legend()
    axs[1].plot(epochs, acc, label='Training accuracy')
    axs[1].plot(epochs, val_acc, label='Validation accuracy')
    axs[1].set_title('Training and validation accuracy', weight="bold")
    axs[1].set_xlabel('Epochs')
    axs[1].set_ylabel('Accuracy')
    axs[1].legend()
    plt.show()
