# MMMMMMMM               MMMMMMMMIIIIIIIIIUUUUUUUU     UUUUUUU
# M:::::::M             M:::::::MI::::::::IU::::::U     U::::::U
# M::::::::M           M::::::::MI::::::::IU::::::U     U::::::U
# M:::::::::M         M:::::::::MII::::::IIUU:::::U     U:::::UU
# M::::::::::M       M::::::::::M  I::::I   U:::::U     U:::::U 
# M:::::::::::M     M:::::::::::M  I::::I   U:::::D     D:::::U 
# M:::::::M::::M   M::::M:::::::M  I::::I   U:::::D     D:::::U 
# M::::::M M::::M M::::M M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M  M::::M::::M  M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M   M:::::::M   M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M    M:::::M    M::::::M  I::::I   U:::::D     D:::::U 
# M::::::M     MMMMM     M::::::MII::::::IINU:::::UUUUUU:::::U 
# M::::::M               M::::::MI::::::::IU:::::::::::::::UU  
# M::::::M               M::::::MI::::::::IU:::::::::::::::UU  
# M::::::M               M::::::MIIIIIIIIIUUUUUUUUUUUUUUUUUUUU  


import asyncio #ibrary for writing asynchronous code
import pandas as pd #library for data manipulation and analysis
import numpy as np #library for numerical computing
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split #used to split the dataset into training and testing sets.
from sklearn.preprocessing import LabelEncoder, StandardScaler #It is used for label feature scaling.
from tensorflow import keras #Keras API provided by TensorFlow,(deep learning library) #Keras provides a high-level interface for building and training neural networks.
import tensorflow 
from keras.layers import Dense #A layer class in Keras that represents a fully connected (dense) layer in a neural network.
import globalflags

class DdosDetector: # constructor method initializes the DdosDetector object. It initializes the model and scaler attributes.
    def __init__(self):
        # self.data_file_path = data_file_path
        self.model = None
        self.scaler = None
    async def startretrain(self): #triggers the process of retraining the DDoS detection model. 
        self.load_data() #this function call the functions seq.
        self.build_model()
        self.train_model()
        self.evaluate_model()
        self.save_model('ddos_detector_model.h5')

    async def retrain(self): #An asynchronous method that creates an asynchronous task using asyncio.create_task() to run the startretrain() method.
        task1 = asyncio.create_task(self.startretrain())
        

    def load_data(self): #This method loads the dataset from a CSV file, performs necessary data preprocessing steps, such as dropping columns, converting categorical features to numerical values, and scaling the numerical features. It also splits the dataset into training and testing sets.
        # Load the dataset from CSV file
        df = pd.read_csv(globalflags.data_file_path)

        # Drop unnecessary columns
        df = df.drop(columns=['id', 'proto', 'service', 'state', 'attack_cat'])

        # Convert categorical features to numerical values

        # Scale the numerical features
        self.scaler = StandardScaler() #Scale the numerical features using StandardScaler from the sklearn.preprocessing module
        df.iloc[:, :-1] = self.scaler.fit_transform(df.iloc[:, :-1]) #(self.scaler) to the selected numerical columns.

        # Split the dataset into training and testing sets
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values #(target)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#The input features are selected from the DataFrame using df.iloc[:, :-1].values, and the target variable is selected from the DataFrame using df.iloc[:, -1].values. The test_size parameter specifies the proportion of the dataset to be used for testing (in this case, 20%),
#  and random_state ensures reproducibility of the split. #meaning that the same split will be generated each time the code is executed. 

    def build_model(self):#responsible for defining the architecture of the neural network model and compiling it.
        # Define the model architecture
        self.model = keras.Sequential([ #It creates an instance of the Sequential class from keras, which allows us to build a model by stacking layers one after another.
            Dense(64, activation='relu', input_shape=[self.X_train.shape[1]]),
            Dense(64, activation='relu'), #Inside the Sequential model, three dense layers are added. The first two layers have 64 units and use the ReLU activation function, which introduces non-linearity to the model. The input shape of the first layer is determined by the number of features in the training data (self.X_train.shape[1]).
            Dense(1, activation='sigmoid')#The last layer has a single unit and uses the sigmoid activation function. This is a binary classification task, so the output of the model will be a probability between 0 and 1, representing the likelihood of the input belonging to the positive class (DDoS attack).
        ])

        # Compile the model 
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])#The loss function is set to 'binary_crossentropy', which is commonly used for binary classification tasks. The optimizer is set to 'adam', which is an efficient optimization algorithm. The metrics are set to ['accuracy'], which will be used to evaluate the performance of the model during training.

    def train_model(self):
        # Train the model #self.model.fit: This line of code trains the model using the fit method of the model object.
        self.model.fit(self.X_train, self.y_train, epochs=10, batch_size=32, validation_split=0.2)# self.X_train contains the input features and self.y_train contains the corresponding target labels.
#epochs=10 indicates that the training process will iterate over the entire training dataset 10 times. Each iteration is considered as one epoch. 

def evaluate_model(self): 
        # Evaluate the model on the testing set
        test_loss, test_acc = self.model.evaluate(self.X_test, self.y_test, verbose=2)#One line per epoch mode. It displays a single line for each epoch showing the progress and evaluation metrics.
        
        # Evaluate the model on the testing set
        y_pred = self.model.predict(self.X_test)  # Predict the labels for the testing set
        y_pred = np.round(y_pred).flatten()  # Convert the predicted probabilities to binary labels

        # Calculate precision, recall, and F1 score
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)
        
       # Calculate confusion matrix
        cm = confusion_matrix(self.y_test, y_pred)
        print('Confusion Matrix:')
        print(cm)

        print('Test accuracy:', test_acc)
        print('Precision:', precision)
        print('Recall:', recall)
        print('F1 Score:', f1)
    def save_model(self, model_file_path):
        # save the trained model
        self.model.save(model_file_path)#location where the model will be saved.
        
    def load_model(self):
        # load the trained model
        self.model = keras.models.load_model(globalflags.modelpath)
