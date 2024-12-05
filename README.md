# DatenbankenPortfolio
Repo der Portfolioprüfung mit allen Skripten

# Bei beiden Vorgehensweisen
MongoSH Skript in MongoDBCompass ausführen um die mapping collection zu erhalten

# Vorgehensweise mit Master Skript
1. Ausführung des masterScript.py -> Führt alle aufgelisteten Skripte automatisch aus

# Vorgehensweise bei der manuellen Ausführung der Skripte:
1.	fakingScript (ändert yelp daten und verbindet yelp und inspections)
2.	consistencyCheck (prüft ob alle Datensätze dieselben Datenfelder hat)
3.	consistencyEnforcement (fügt fehlende Datensätze hinzu)
4.	removeMissingGeoData (löscht die in consistencyEnforcement erstellten Geodaten mit Null)
5.	removeMissingScore (löscht inspections ohne Score und wenn dann ein Restaurant ohne Score löscht dieses auch)
6.	deleteRestaurantsWithoutInspections (Restaurants ohne Inspection werden gelöscht)
7.	dataTypesCheck (checkt aus einheitlichen Datentypen -> BUILDING & PHONE inkonsistent, aber irrelevant, da wir es nicht in SQL übernehmen)
8.	searchDuplicates (sucht nach Duplikate -> findet keine)
9.  export (exportiert die Daten in mySQL)

# Koordinaten exportieren
Die Koordinaten sind nach durchlaufen aller Skripts in den Views. 
Diese sind in 3 Kategorien eingeteilt:
0-33: bad
34-66 : ok
67-100 : good

# Auswertung
1. Hotspots visulasieren (MatLab)
2. Zip codes bewerten (Manuell im schlimmsten Fall)
3. Yelp Korrelationskoeffizient (zwischen Yelp Bewertung und Score)

# Warum SQL?