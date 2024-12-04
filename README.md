# DatenbankenPortfolio
Repo der Portfolioprüfung mit allen Skripten

# Vorgehensweise bei der Ausführung der Skripte:
1.	fakingScript (ändert yelp daten und verbindet yelp und inspections)
2.	consistencyCheck (prüft ob alle Datensätze dieselben Datenfelder hat)
3.	consistencyEnforcement (fügt fehlende Datensätze hinzu)
4.	removeMissingGeoData (löscht die in consistencyEnforcement erstellten Geodaten mit Null)
5.	removeMissingScrore (löscht inspections ohne Score und wenn dann ein Restaurant ohne Score löscht dieses auch)
6.	deleteRestaurantsWithoutInspections (Restaurants ohne Inspection werden gelöscht)
7.	dataTypesCheck (checkt aus einheitlichen Datentypen -> BUILDING & PHONE inkonsistent, aber irrelevant, da wir es nicht in SQL übernehmen)
8.	searchDuplicates (sucht nach Duplikate -> findet keine)