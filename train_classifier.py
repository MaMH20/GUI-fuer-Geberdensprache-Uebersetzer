import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

#Laden der Daten aus der Pickle-Datei
data_dict = pickle.load(open('./data.pickle', 'rb'))

#Umwandeln der Daten in ein Numpy-Array
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

#Aufteilung der Daten in Trainings- und Testdaten
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

#Erstellen des Random Forest Klassifikators
model = RandomForestClassifier()

#Trainieren des Klassifikators mit den Trainingsdaten
model.fit(x_train, y_train)

#Vorhersage der Labels für die Testdaten
y_predict = model.predict(x_test)

#Berechnen der Genauigkeit des Klassifikators
score = accuracy_score(y_predict, y_test)
#Ausgabe der Genauigkeit
print('{}% of samples were classified correctly !'.format(score * 100))

#Speichern des trainierten Modells in einer Pickle-Datei
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
