# HaTrNaAb_Zaehler
In dieser App kann man Dokumentieren, wie oft Schüler Hausaufgaben vergessen haben, in den Trainings, Nacharbeiten  oder etwas anderes Abschreiben müssen.


## Voraussetzungen
Die App ist in Python geschrieben und benötigt Kivy. Installiere es mit
```
pip3 install kivy
```

## Android App erstellen
In der Datei buildozer.spec sind die Voraussetzungen zur Erzeugung der Android App gegeben. Erzeuge die App mit dem Befehl
```
buildozer android debug
```

## Nutzung
Auf einem Linux/Windows Computer kann die App direkt genutzt werden:
```
python main.py
```
Der Ziel ist es aber, die App auf einem Android Smartphone zu nutzen.

 1. Erstelle im Home-Verzeichnis den Ordner "sitzplanNoten".
 2. Die App greift auf dem Pfad "os.path.join(os.getenv('EXTERNAL_STORAGE'),'sitzplanNoten')" zu.
 3. Installiere die App auf deinem Gerät
 4. Gib der App die Berechtigung, auf den Externen-Speicher zuzugreifen. Dies wird noch nicht abgefragt.
 5. Erstelle eine Komma getrennte Datei im Format (Vorname, Nachname). Speicher die Datei mit dem Namen ListeAusrutscher_Klasse.csv (siehe ListeAusrutscher_Test7a.csv) im Android-Ordner "sitzplan/Noten"
 6. Starte die App auf dem Smartphone
 7. Es folgt eine Übersicht aller Dateien mit dem Namensformate ListeAusrutscher_Klasse.csv.
 8. Wähle die gewünschte Klasse.
 9. Beim Speichern werden die aktuellen Vergessenen Hausaufgaben und co gespeichert.
 11. Auswertung: Kopiere die csv Datei auf den PC. Importiere die Datei in Calc oder Excel.

