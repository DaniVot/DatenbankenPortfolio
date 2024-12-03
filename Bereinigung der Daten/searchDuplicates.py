from pymongo import MongoClient

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['NYAnalyse']


# Funktion zur Überprüfung auf Duplikate in einer Collection
def check_duplicates(collection_name, fields_to_check):
    collection = db[collection_name]

    # Aggregation, um Duplikate zu finden
    pipeline = [
        {"$group": {
            "_id": {field: f"${field}" for field in fields_to_check},  # Gruppieren nach den angegebenen Feldern
            "count": {"$sum": 1}  # Anzahl der Dokumente pro Gruppe zählen
        }},
        {"$match": {
            "count": {"$gt": 1}  # Nur Gruppen mit mehr als einem Dokument behalten
        }}
    ]

    duplicates = list(collection.aggregate(pipeline))

    # Ergebnisse ausgeben
    if duplicates:
        print(f"Duplikate gefunden in '{collection_name}':")
        for duplicate in duplicates:
            print(f"Wert(e): {duplicate['_id']}, Anzahl: {duplicate['count']}")
    else:
        print(f"Keine Duplikate in '{collection_name}' gefunden.")


# Beispiele für die Prüfung
check_duplicates("fake_inspection_results", ["CAMIS"])  # Überprüfung auf Duplikate basierend auf CAMIS
check_duplicates("fake_yelp_business", ["business_id"])  # Überprüfung auf Duplikate basierend auf business_id