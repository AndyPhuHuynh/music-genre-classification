import os
import random
import librosa
import numpy as np

from src.dataset import Dataset
from src.paths import GTZAN_DIR
from src.features.labels import get_label

SAMPLE_RATE = 22050
N_MFCC = 13

def extract_features(dataset_path: str = GTZAN_DIR) -> Dataset:
    """
    Extracts MFCC features and genre labels from the GTZAN dataset
    :param dataset_path: path to the GTZAN dataset which directly contains subdirectories of all the genres
    :return: A dataset containing MFCC features and genre labels
    """
    X = []
    y = []

    genres = os.listdir(dataset_path)
    for genre in genres:
        genre_dir = os.path.join(dataset_path, genre)
        if not os.path.isdir(genre_dir):
            continue

        print(f"Extracting MFCC for {genre}")
        for filename in os.listdir(genre_dir):
            file_path = os.path.join(genre_dir, filename)
            try:
                # Extract the waveform and sample rate
                signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
                # Extract mfcc data for the sample in intervals of short frames
                mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=N_MFCC)
                # Average each feature over all the time frames
                mfcc_mean = np.mean(mfcc.T, axis=0)
                X.append(mfcc_mean)
                y.append(get_label(genre))
            except Exception as e:
                print(f"Unable to process file '{file_path}': {e}")
    X = np.array(X)
    y = np.array(y)
    print(f"Extracted {len(X)} samples with {X.shape[1]} features each")
    return Dataset(X, y)


def split_dataset(dataset: Dataset) -> tuple[Dataset, Dataset, Dataset]:
    """
    Splits dataset into training, validation, and test sets
    :param dataset: The dataset to split
    :return: (Dataset, Dataset, Dataset): training, validation, and test sets
    """
    data_len = len(dataset)
    shuffled_indices = [i for i in range(data_len)]
    random.shuffle(shuffled_indices)

    training_end_index: int = int(data_len * 0.6)
    validation_end_index: int = training_end_index + int(data_len * 0.2)

    train_indices      = shuffled_indices[:training_end_index]
    validation_indices = shuffled_indices[training_end_index:validation_end_index]
    test_indices       = shuffled_indices[validation_end_index:]

    X_train, y_train = dataset.X[train_indices],      dataset.y[train_indices]
    X_val,   y_val   = dataset.X[validation_indices], dataset.y[validation_indices]
    X_test,  y_test  = dataset.X[test_indices],       dataset.y[test_indices]

    return Dataset(X_train, y_train), Dataset(X_val, y_val), Dataset(X_test, y_test)



