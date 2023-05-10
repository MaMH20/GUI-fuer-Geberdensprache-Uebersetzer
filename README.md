# Gebärdensprache Übersetzer „Applikation“ (Buchstabenerkennung)

## Graphische Oberfläche GUI

#### Bilder aufnehmen

  - Lösung: Take-picture Button

#### App verlassen können

- Lösung: Quit Button

#### Picture und der erkannte Buchstabe löschen können.

- Lösung: Clear Button

#### App leicht und schnell bedienen

- Lösung: Shortcuts

#### Erkannter Buchtstabe anzeigen lassen

- Lösung: anzeigen auf dem Picture

#### Aus mehreren hintereinander erkannten Buchstaben ein Wort bilden können

- Lösung: anzeigen auf dem Picture

#### Kamera Übertragung durch das aufgenommene Picture ersetzen. <br><br><br>
  


## Umgehen mit dem Input bzw. den aufgenommenen Pictures

#### Einheitliche Skalierung der Pictures

- Lösung: Picture reskalieren

#### Einheitliche Farbformat

- Lösung: OpenCv bietet diesbezüglich verschiedene Methoden an

- Warum: bietet eine breite Palette von Funktionen für die Bildverarbeitung und -analyse, weshalb es häufig bevorzugt, wird

#### Extrahierung der wesentlichen Informationen des Pictures (Handlandmarks)

- Lösung: Mediapipe bietet diesbezüglich verschiedene Methoden an

- Warum:

  - Handlandmarks unabhängig von der Hintergrundumgebung ist

  - leicht von anderen Objekten im Bild segmentiert zu werden

  - sind invariant gegenüber verschiedenen Beleuchtungsbedingungen und Farben

  - sind als komprimierte Form der Information zu betrachten à Verarbeitung durch z.B. CNN beschleunigen. <br><br><br>

## Daten:

- Beschaffung von Daten (Bilder)

- Einheitliche Skalierung der Daten bzw. der Bilder

- Sortierung und Speicherung in verschiedenen Ordner mit dem entsprechenden Label je nachdem Gest
    -  Lösung: Aufnahme von Bildern durch ein Programm. <br><br><br>

## Dataset:

#### Datenquellen

- Lösung: Importieren der erstellen Daten

#### Ordnerstruktur der Datenquellen

#### Speicherplatz

#### Extrahierung der wesentlichen Informationen der Bilder (Handlandmarks)

- Lösung: Mediapipe bietet diesbezüglich verschiedene Methoden an

- Warum Mediapipe:

  - Handlandmarks sind unabhängig von der Hintergrundumgebung

  - leicht von anderen Objekten im Bild segmentiert zu werden

  - sind invariant gegenüber verschiedenen Beleuchtungsbedingungen und Farben

  - sind als komprimierte Form der Information zu betrachten à Verarbeitung durch z.B. CNN beschleunigen

#### Speicherung der wesentlichen Informationen der Bilder und des jeweiligen Labels

- Speicherort

  - Lokalen Festplatte

#### in welchen Format?à JSON oder Pickle

- Lösung: Pickle Bibliothek

  - Vorteile: Einfache Integration in Python, Unterstützung für beliebige Python-Objekte , Behält die Objektstruktur bei.

  - Nachteile: eingeschränkte Interoperabilität mit anderen Sprachen

- Lösung: JSON Bibliothek

  - Vorteile: JSON wird von vielen Programmiersprachen unterstützt und kann auf jeder Plattform verwendet werden.

  - Nachteile: JSON ist ein einfaches Textformat und unterstützt nicht alle Datenstrukturen, die ein typisches Machine-Learning-Modell haben kann. <br><br><br>

## Erstellung eines trainierten Modells

#### Dataset Importieren

#### Modell trainieren

  - Unterscheiden zwischen bestimmte Geste (vordefinierte Kategorien)

    - Lösung: Supervised Learning (Classification problem)

    - Warum:

      - Unser Dataset enthält Daten-Label-Paaren.

      - Supervised Learning lernt Modellparameter anhand des Datensatzes von Daten-Label-Paaren

      - Klassifizierungsproblem erfordert Datensatz mit Daten-Label-Paaren

- Geeignetes Classification Algorithmus

  - Lösung: Random Forests Algorithmus

  - Warum:

    - hohe Genauigkeit der Vorhersage

    - Gutes Umgehen mit großen Datenmengen

    - “The advantages of Random Forest are that it prevents overfitting and is more accurate in predictions”

#### Modell speichern

- Lösung: Pickle Bibliothek

  - Vorteile: Einfache Integration in Python, Unterstützung für beliebige Python-Objekte , Behält die Objektstruktur bei.

  - Nachteile: eingeschränkte Interoperabilität mit anderen Sprachen  

- Lösung: JSON Bibliothek

  - Vorteile: JSON wird von vielen Programmiersprachen unterstützt und kann auf jeder Plattform verwendet werden.

  - Nachteile: JSON ist ein einfaches Textformat und unterstützt nicht alle Datenstrukturen, die ein typisches Machine-Learning-Modell haben kann.
