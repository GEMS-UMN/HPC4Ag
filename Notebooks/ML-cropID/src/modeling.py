import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Reshape, Flatten, LSTM, Dense, Dropout, SimpleRNN
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import MinMaxScaler

def generate_X_and_y(data, one_hot_encoded_labels):
    """
    Pairs data patches with labels based on field IDs to create X array and corresponding y array.

    Parameters:
        data (dict): dictionary with field IDs and corresponding patches.
        one_hot_encoded_labels (pandas.DataFrame): Data frame with one hot encoded representation of different categories for each field ID.

    Returns:
        array, array: Array with patches, array with labels
    """ 
    X = []
    y = []
    for fid in data.keys():
        for patchid in range(0, data[fid].shape[0]):
            X.append(data[fid][patchid])
            y.append(one_hot_encoded_labels.loc[fid])
    X = np.array(X)
    y = np.array(y)
    return X, y

def assign_class_weight(y):
    """
    Computes class weight to balance out under- and over-represented classes in the training set.

    Parameters:
        y (array): Array of one hot encoded train labels.

    Returns:
        dict: Dictionary with structure {class : weight}
    """ 
    class_series = np.argmax(y, axis=1)
    # Compute class weights with sklearn method
    class_labels = np.unique(class_series)
    class_weights = compute_class_weight(class_weight="balanced", classes=class_labels, y=class_series)
    return dict(zip(class_labels, class_weights))


def apply_scaler_train(X_train):
    """
    Fits scaler to each feature of train and transforms train data.

    Parameters:
        X_train (array): Array of train data with original values.

    Returns:
        array, dict of objects: Scaled train data, dictionary of scaler objects (one for each channel)
    """ 
    scaled_feature_arrays = []
    scalers = {}
    for feature in [0,1]:
        scalers[feature] = MinMaxScaler()
        X_train_feature = X_train[:,:,feature,:,:].reshape(-1,1)
        X_train_feature_scaled = scalers[feature].fit_transform(X_train_feature)
        X_train_feature_scaled = X_train_feature_scaled.reshape(X_train[:,:,feature,:,:].shape)
        scaled_feature_arrays.append(X_train_feature_scaled)
    X_train_scaled = np.stack(scaled_feature_arrays, axis=2)
    return X_train_scaled, scalers

def apply_scaler_test(X_test, scalers):
    """
    Transforms test data with previously created scalers.

    Parameters:
        X_test (array): Array of test data with original values.
        scalers (dict of objects): Dictionary of scaler objects (one for each channel)

    Returns:
        array: Scaled test data.
    """ 
    scaled_feature_arrays = []
    for feature in [0,1]:
        X_test_feature = X_test[:,:,feature,:,:].reshape(-1,1)
        X_test_feature_scaled = scalers[feature].transform(X_test_feature)
        X_test_feature_scaled = X_test_feature_scaled.reshape(X_test[:,:,feature,:,:].shape)
        scaled_feature_arrays.append(X_test_feature_scaled)
    X_test_scaled = np.stack(scaled_feature_arrays, axis=2)
    return X_test_scaled

def compile_model(shape=(31, 2, 3, 3), kind="SimpleRNN"):
    """
    Defines and compiles a neural network model.

    Parameters:
        shape (tuple, optional): Tuple describing input array shape as (time, band, row, column). Defaults to (31, 2, 3, 3).
        kind (str, optional): Sequential model type. Defaults to SimpleRNN.

    Returns:
        keras.Model: Compiled neural network model.
    """ 
    # Define a model
    model = Sequential()
    model.add(Reshape((shape[0], shape[1]*shape[2]*shape[3]), input_shape=shape))
    if kind == "SimpleRNN":
        model.add(SimpleRNN(units=4, activation="softmax"))  
    elif kind == "LSTM":
        model.add(LSTM(units=64, kernel_regularizer=regularizers.l2(0.01)))
        model.add(Dense(128, activation="relu", kernel_regularizer=regularizers.l2(0.01)))
        model.add(Dropout(0.5))
        model.add(Dense(4, activation="softmax"))  
    # Compile the model
    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])
    return model