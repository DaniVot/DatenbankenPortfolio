from pymongo import MongoClient
from collections import defaultdict

# Verbindung zu MongoDB herstellen
client = MongoClient("mongodb://localhost:27017/")  # Passe die Verbindungsdetails an
db_name = "PortfolioPruefung"  # Name der Datenbank

db = client[db_name]

# List der zu durchsuchenden Collections
collection_names = ["fake_inspection_results", "fake_yelp_business"]

# Dictionary für Feldnamen und Datentypen
field_type_counts = defaultdict(lambda: defaultdict(int))

# Alle Collections durchgehen
for collection_name in collection_names:
    collection = db[collection_name]
    
    # Alle Dokumente durchgehen
    for doc in collection.find():
        for field, value in doc.items():
            field_type_counts[(collection_name, field)][type(value).__name__] += 1

# Ergebnisse anzeigen
print(f"Datentyp-Verteilung in den Collections {', '.join(collection_names)}:\n")
for (collection_name, field), type_counts in field_type_counts.items():
    print(f"Collection: {collection_name}, Feld: {field}")
    for type_name, count in type_counts.items():
        print(f"  {type_name}: {count}")
    print()

'''
{
  "fieldName": { "$type": "desiredDataType" }
}

-> zum testen in MongoDB Compass
'''
