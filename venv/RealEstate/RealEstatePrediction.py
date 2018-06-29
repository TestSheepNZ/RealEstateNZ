""""    Previously with FindResidentialPropertyValue, I've run through a set of data finding price
        bandings for residential properties in a location
        This script will feed that data into a machine learning algorithm """
import numpy as np


# Initialise arrays
inputArray = []
outputArray = []

# Open our source data
with open("Property Data For ML.csv") as sourceFile:
    for line in sourceFile:


        # First line will contain titles data
        if "Item Num" not in line:
            elements = line.split('|')
            print ("Loading data item " + elements[0])
            try:
                # My longitude and lattitude are the wrong way around I know!
                lattitude = float(elements[1])
                longitude = float(elements[2])
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
ML_NeuralNet = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(100, 100, 100, 100, 100, 100, 100, 100, 100), random_state=1)
ML_NeuralNet.fit(inputData, outputData)

# Predict house on Ponsonby road
ponsonbyLat =  -36.848461
ponsonbyLong = 174.763336
ponsonby = [[ponsonbyLat, ponsonbyLong]]

orientalBayLat = -41.2913
orientalBayLong = 174.7941
orientalBay = [[orientalBayLat, orientalBayLong]]


# Should be the middle of nowhere - hence about 1 price bracket
kakatahiLat = -39.701072
kakatahiLong = 175.328703
kakatahi = [[kakatahiLat, kakatahiLong]]

# Upper Hutt
upperHuttLat = -41.1244
upperHuttLong = 175.0708
upperHutt = [[upperHuttLat, upperHuttLong]]


print("Neural Net predicts Ponsonby Rd price class as " + str(ML_NeuralNet.predict(ponsonby)))

print("Bay Ridge predicts Ponsonby Rd price class as " + str(ML_BayRidge.predict(ponsonby)))

from sklearn.neighbors import KNeighborsClassifier
neighbours = KNeighborsClassifier(n_neighbors=3)
neighbours.weights = 'distance'
neighbours.algorithm = 'auto'
neighbours.fit(inputData,outputData)

np = [ponsonbyLat, ponsonbyLong]

print ("KNN predicts Ponsonby Rd price class as " + str(neighbours.predict(ponsonby)))
print ("KNN predicts Oriental Bay price class as " + str(neighbours.predict(orientalBay)))
print ("KNN predicts Kakatahi price class as " + str(neighbours.predict(kakatahi)))
print ("KNN predicts Upper Hutt price class as " + str(neighbours.predict(upperHutt)))