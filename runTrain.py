from tempLoad import load_data
from modelCreator import create_model
from modelUtils import compile_model, evaluate_model, save_model

print ("Training data")
training_data, training_labels = load_data(r'C:\Users\iamar\wakeword-data\training')
print ("Validation data")
validation_data, validation_labels = load_data(r'C:\Users\iamar\wakeword-data\validate')

model = create_model()

compile_model(model, 50, training_data, training_labels, validation_data, validation_labels)
accuracy = evaluate_model(model, validation_data, validation_labels)

file_name = save_model(model, accuracy)
print('Hot word detector training has completed. File stored ', file_name)