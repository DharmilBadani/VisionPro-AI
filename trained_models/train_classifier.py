import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

def train_custom_model(dataset_dir, epochs=5, batch_size=32, img_size=(224, 224)):
    """
    Fine-tunes MobileNetV2 on a custom dataset folder structured as:
    dataset_dir/
        class_1/
            img1.jpg
            img2.jpg
        class_2/
            img3.jpg
            img4.jpg
    """
    print(f"Loading custom dataset from: {dataset_dir}")
    
    # 1. Setup Image Data Generators with basic data augmentation
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    train_generator = datagen.flow_from_directory(
        dataset_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )
    
    val_generator = datagen.flow_from_directory(
        dataset_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )
    
    num_classes = train_generator.num_classes
    class_indices = train_generator.class_indices
    print(f"Classes found: {list(class_indices.keys())}")
    
    # 2. Build MobileNetV2 base model with frozen weights
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=img_size + (3,))
    base_model.trainable = False
    
    # 3. Append custom dense classification head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    # 4. Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # 5. Train model
    print("Starting training...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs
    )
    
    # 6. Save model weights
    output_path = os.path.join("trained_models", "mobilenetv2_custom.h5")
    os.makedirs("trained_models", exist_ok=True)
    model.save(output_path)
    print(f"Model saved successfully to: {output_path}")
    
    return history

if __name__ == "__main__":
    # Create a mock training folder if not exists to demonstrate usage
    mock_dataset_dir = "trained_models/dummy_dataset"
    os.makedirs(os.path.join(mock_dataset_dir, "circle"), exist_ok=True)
    os.makedirs(os.path.join(mock_dataset_dir, "square"), exist_ok=True)
    
    print("\n[INFO] To train the model on your custom dataset:")
    print("1. Organize your images into subfolders inside a dataset directory.")
    print("2. Call: train_custom_model('path/to/dataset')")
