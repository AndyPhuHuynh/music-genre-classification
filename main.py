import os
import numpy as np

os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

from src.features.extract_mfcc import extract_features, split_dataset
from src.features.labels import get_genre_from_label
from src.setup.init_dataset import ensure_gtzan_downloaded

ensure_gtzan_downloaded()
scaler, data = extract_features()
train, validation, test = split_dataset(data)

num_features = train.X.shape[1]
num_classes = 10
y_train_cat = to_categorical(train.y, num_classes)
y_validation_cat = to_categorical(validation.y, num_classes)

model = Sequential([
    Dense(128, activation='relu', input_shape=(num_features,)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(train.X, y_train_cat, validation_data=(validation.X, y_validation_cat), epochs=30, batch_size=32)

ratios: dict[int, float] = {}

for i in range(10):
    total: int = 0
    correct: int = 0
    for j in range(len(test)):
        if test.y[j] == i:
            total += 1
            prediction = model.predict(test.X[j].reshape(1, -1))
            predicted_class = np.argmax(prediction)
            if predicted_class == i:
                correct += 1
    ratios[i] = 1.0 * correct / total


y_test_cat = to_categorical(test.y, num_classes)
test_loss, test_acc = model.evaluate(test.X, y_test_cat, verbose=2)

print(f"Test accuracy: {test_acc * 100:.2f}%")
print(f"Test loss: {test_loss:.4f}")

for label, ratio in ratios.items():
    print(f"For genre {get_genre_from_label(label)}: Correct percentage: {ratio}")


