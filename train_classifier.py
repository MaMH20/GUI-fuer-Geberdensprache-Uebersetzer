import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn import metrics

#Laden der Daten aus der Pickle-Datei
data_dict = pickle.load(open('./data.pickle', 'rb'))
#data_left_Hand_A_Z.pickle--->zum Trainieren der linken Hand
#data_Righ_Hand_A_Z.pickle--->zum Trainieren der rechten Hand


#Umwandeln der Daten in ein Numpy-Array
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])


#Aufteilung der Daten in Trainings- und Testdaten
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, stratify=labels,shuffle=True)


#Erstellung des Support Vector Classifier
svc_model = SVC(C=2.0, kernel='rbf', gamma='scale')


#K-Fold Cross-Validation
kfold = KFold(n_splits=5)
scores = cross_val_score(svc_model, x_train, y_train, cv=kfold, scoring='accuracy')

#Berechnung der Genauigkeit der Kreuzvalidierung
average_accuracy = scores.mean()
print('Cross-Validation Accuracy : ', average_accuracy * 100, '%')

#Berechnung der Genauigkeit an Testdaten
svc_model_after_val = svc_model.fit(x_train, y_train)
test_accuracy = svc_model_after_val.score(x_test, y_test)
print('Accuracy : ', test_accuracy * 100, '%')


#Speichern des trainierten Modells in einer Pickle-Datei
f = open('model.p', 'wb')##--->Eingabe des korrekten Modellnamens(rechts oder links)
pickle.dump({'model': svc_model_after_val}, f)
f.close()
