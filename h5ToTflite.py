import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model(r'C:\Users\iamar\Wakeword-neural-network\wakeword models\wakeword-model.h5', compile = False)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TF Lite model.
with tf.io.gfile.GFile(r'C:\Users\iamar\Wakeword-neural-network\wakeword models\new-model.tflite', 'wb') as f:
  f.write(tflite_model)