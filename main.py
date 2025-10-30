from src.dataset import Dataset
from src.setup.init_dataset import ensure_gtzan_downloaded
from src.features.extract_mfcc import extract_features, split_dataset

ensure_gtzan_downloaded()
data: Dataset = extract_features()
train, validation, test = split_dataset(data)

print(f"Length of train set: {len(train)}")
print(f"Length of validation set: {len(validation)}")
print(f"Length of test set: {len(test)}")

