# Gebärdensprache Übersetzer „Applikation“ (Buchstabenerkennung)

#### Das Ziel unseres Projekts ist es, eine Anwendung zu entwickeln, die die Gebärdensprache Alphapet erkennen kann. Um unser Ziel zu erreichen, mussten wir verschiedene Technologien verwenden und viele Prozesse durchführen.
#### Zuerst mussten wir Daten (Bilder) sammeln und in Zielordnern speichern, wofür wir das Skript Collect_imgs.py verwendet haben. [Collect_imgs.py](https://github.com/MaMH20/GUI-fuer-Geberdensprache-Uebersetzer/blob/main/Collect_imgs.py)
#### Danach mussten wir die Daten aufbereiten und bearbeiten, damit wir das Dataset erstellen konnten, das wir später zum Trainieren des Modells verwenden werden, dafür haben wir das Skript create_dataset.py verwendet. [create_dataset.py](https://github.com/MaMH20/GUI-fuer-Geberdensprache-Uebersetzer/blob/main/create_dataset.py)

#### Um den geeigneten Trainingsalgorithmus auszuwählen, haben wir verschiedene Trainingsalgorithmen mit unterschiedlichen Parametern getestet und verglichen und die entsprechenden Diagramme dargestellt, um die bestmögliche Leistung des Modells zu erzielen. Der vollständige Quellcode ist unter Modellauswahl und -bewertung zu finden. [Modellauswahl und -bewertung](https://github.com/MaMH20/GUI-fuer-Geberdensprache-Uebersetzer/blob/main/Modelauswahl%20und%20Bewertung.ipynb)

#### Als nächstes haben wir das Modell mit geeigneten Trainingsalgorithmen trainiert und die Genauigkeit berechnet, dafür haben wir die Scikit-Learn-Bibliothek verwendet, die im Skript train_classsifier.py zu finden ist. [train_classifier.py](https://github.com/MaMH20/GUI-fuer-Geberdensprache-Uebersetzer/blob/main/train_classifier.py)

#### Am Ende haben wir ein GUI erstellt, um unsere Ergebnisse benutzerfreundlich darzustellen und das Modell zu testen. 
#### Detaillierte Erklärungen sind im folgenden Bericht zu finden. [Projektbericht](https://github.com/MaMH20/GUI-fuer-Geberdensprache-Uebersetzer/blob/main/Projektbericht.pdf)
