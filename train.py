from tensorflow import keras
from keras import layers, models
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import numpy as np


def main():

    # Parameter definition
    dataset_dir = r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\datasets\dataset_v2"
    img_height, img_width = 45, 45
    batch_size = 256
    epochs = 5
    num_classes = 20

    # Dataset import
    train_ds, test_ds = keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        labels='inferred',
        label_mode='int',
        validation_split=0.2,
        seed=1,
        subset='both',
        batch_size=batch_size,
        image_size=(img_height, img_width),
        color_mode='grayscale'
    )

    val_ds = train_ds.skip(int(len(train_ds)*0.8))
    train_ds = train_ds.take(int(len(train_ds)*0.8))

    # Model definition
    model = models.Sequential([
        layers.Rescaling(1. / 255, input_shape=(img_height, img_width, 1)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    # Compile
    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])
    model.summary()

    # Train
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    model.save(
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\models\symbol_recognition_12")

    # Summary analysis
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

    model_output = model.predict(test_ds)
    pred_test = np.argmax(model_output, axis=1)
    true_test = np.concatenate([y for x, y in test_ds], axis=0)
    print(pred_test)
    print(true_test)

    print(classification_report(true_test, pred_test, labels=test_ds.class_names))


if __name__ == "__main__":
    main()

