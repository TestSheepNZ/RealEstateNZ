""""    Previously with FindResidentialPropertyValue, I've run through a set of data finding price
        bandings for residential properties in a location
        This script will feed that data into a machine learning algorithm """
import numpy as np


# Initialise arrays
inputArray = []
outputArray = []

# Open our source data
with open("Property Data For ML") as sourceFile:
    for line in sourceFile:


        # First line will contain titles data
        if "Item Num" not in line:
            elements = line.split('|')
            print ("Loading data item " + elements[0])
            try:
                # My longitude and lattitude are the wrong way around I know!
                longitude = float(elements[1])
                lattitude = float(elements[2])
                priceCategory = int(elements[3])

                inputArray.append([lattitude, longitude])
                outputArray.append(priceCategory)
            except:
                print("Data error: " + line)


# Turn lists into NumPy arrays
inputData = np.array(inputArray)
outputData = np.array(outputArray)

# Turn data into a model and print predictions
# ============================================
print
print("CREATING MODEL")
print("==============")
print


# Nearest Centroid Classifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
ML_Centroid = NearestCentroid()
ML_Centroid.fit (inputData, outputData)


# Baysiean Ridge
from sklearn import linear_model
ML_BayRidge = linear_model.BayesianRidge()
ML_BayRidge.fit(inputData, outputData)

# Neural Network
from sklearn.neural_network import MLPClassifier
ML_NeuralNet = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
ML_NeuralNet.fit(inputData, outputData)

# Predict house on Ponsonby road
ponsonbyLat = -36.848461
ponsonbyLong = 174.763336

""""
ML_NeuralNet.predict(ponsonbyLat, ponsonbyLong)

print("Neural Net predicts Ponsonby Rd price class as " + str(ML_NeuralNet.predict(ponsonbyLat, ponsonbyLong)))

print("Bay Ridge predicts Ponsonby Rd price class as " + str(ML_BayRidge.predict(ponsonbyLat, ponsonbyLong)))


"""


