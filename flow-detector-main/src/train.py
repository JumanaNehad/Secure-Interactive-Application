import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
#from tensorflow import keras
from tensorflow import keras
#from tensorflow.keras import layers
from keras.layers import Dense

# Load the dataset from CSV file
df = pd.read_csv('C:/Users/Nihad/Desktop/project/flow-detector-main/src/filterred.csv')

# Drop unnecessary columns
df = df.drop(columns=['id', 'proto', 'service', 'state', 'attack_cat'])

# Convert categorical features to numerical values

# Scale the numerical features
scaler = StandardScaler()
df.iloc[:, :-1] = scaler.fit_transform(df.iloc[:, :-1])

# Split the dataset into training and testing sets
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model architecture
model = keras.Sequential([
    Dense(64, activation='relu', input_shape=[X_train.shape[1]]),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the testing set
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print('\nTest accuracy:', test_acc)

# save the trained model
model.save('ddos_detector_model')
