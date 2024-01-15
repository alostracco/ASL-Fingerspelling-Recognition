import os
import json
import logging
from django.conf import settings
from keras.layers import GlobalAveragePooling2D, Dense, BatchNormalization, Dropout
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2

#IMAGE_RES = 226


class ASLModel:
    lookup_file = settings.LOOKUP_FILE
    weights_file = settings.WEIGHTS_FILE

    def __init__(self):
        lookup_path = os.path.join(settings.BASE_DIR, self.lookup_file)
        weights_path = os.path.join(settings.BASE_DIR, self.weights_file)

        self.IMAGE_RES = 226

        #logging.info(f"Loading lookup file from: {lookup_path}")
        self.lookup = self.load_lookup(lookup_path)
        self.num_classes = len(self.lookup.keys())
        self.model = self.load_model(weights_path)

    def load_lookup(self, file_name):
        with open(file_name, "r") as json_file:
            lookup = json.load(json_file)
        return {str(value): key.upper() for key, value in lookup.items()}

    def load_model(self, weights_file):
        base_model = InceptionV3(
            weights="imagenet", include_top=False, input_shape=(self.IMAGE_RES, self.IMAGE_RES, 3)
        )

        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation="relu", kernel_regularizer=l2(0.01))(x)
        x = BatchNormalization()(x)
        x = Dropout(0.5)(x)
        x = Dense(1024, activation="relu", kernel_regularizer=l2(0.01))(x)
        x = BatchNormalization()(x)
        x = Dropout(0.5)(x)
        x = Dense(1024, activation="relu", kernel_regularizer=l2(0.01))(x)
        x = BatchNormalization()(x)
        x = Dropout(0.5)(x)
        predictions = Dense(self.num_classes, activation="softmax")(x)

        model = Model(inputs=base_model.input, outputs=predictions)
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )

        model.load_weights(weights_file)
        return model
