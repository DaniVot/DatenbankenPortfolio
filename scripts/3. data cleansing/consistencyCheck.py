from pymongo import MongoClient

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['PortfolioPruefung']


# Funktion zur Überprüfung der Konsistenz eines Datensatzes
def check_field_consistency(collection_name, required_fields):
    collection = db[collection_name]

    missing_fields_count = {field: 0 for field in required_fields}  # Initialisiere Zähler für jedes Feld

    # Alle Dokumente durchlaufen
    for document in collection.find():
        for field in required_fields:
            if field not in document:  # Wenn das Feld fehlt
                missing_fields_count[field] += 1

    # Ausgabe der Anzahl der fehlenden Felder pro Kategorie
    print(f"Konsistenzüberprüfung für '{collection_name}':")
    for field, count in missing_fields_count.items():
        if count > 0:
            print(f"Feld '{field}' fehlt in {count} Datensätzen.")
        else:
            print(f"Feld '{field}' ist in allen Datensätzen vorhanden.")


# Beispiel: Überprüfung der Konsistenz für fake_inspection_results
required_fields_fake_inspection = ['CAMIS', 'DBA', 'BORO', 'BUILDING', 'STREET', 'ZIPCODE', 'PHONE', 'CUISINE DESCRIPTION', 'INSPECTION DATE', 'ACTION', 'VIOLATION CODE', 'VIOLATION DESCRIPTION', 'CRITICAL FLAG', 'SCORE', 'GRADE', 'GRADE DATE', 'RECORD DATE', 'INSPECTION TYPE', 'BIN', 'BBL', 'NTA']

check_field_consistency("fake_inspection_results", required_fields_fake_inspection)

# Beispiel: Überprüfung der Konsistenz für fake_yelp_business
required_fields_fake_yelp = ['business_id', 'name', 'address', 'postal_code', 'city', 'latitude', 'longitude', 'phone', 'stars', 'review_count']
check_field_consistency("fake_yelp_business", required_fields_fake_yelp)
