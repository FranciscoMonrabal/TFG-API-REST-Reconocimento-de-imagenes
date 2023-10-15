from tensorflow import keras
from keras import layers, models
import matplotlib.pyplot as plt


def main():

    # Parameter definition
    dataset_dir = r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset"
    img_height, img_width = 45, 45
    batch_size = 256
    epochs = 10
    num_classes = 20

    # Dataset import
    train_df, val_df = keras.preprocessing.image_dataset_from_directory(
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

    # Normalization for lighter input values
    normalization_layer = layers.Rescaling(1./255)
    train_df = train_df.map(lambda x, y: (normalization_layer(x), y))
    val_df = val_df.map(lambda x, y: (normalization_layer(x), y))

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
        layers.Dense(num_classes),
        layers.Softmax()
    ])

    # Compile
    model.compile(optimizer=keras.optimizers.Adam(0.0002),
                  loss=keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])
    model.summary()

    # Train
    history = model.fit(
        train_df,
        validation_data=val_df,
        epochs=epochs
    )

    model.save(
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\models\symbol_recognition_3")

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


if __name__ == "__main__":
    main()

