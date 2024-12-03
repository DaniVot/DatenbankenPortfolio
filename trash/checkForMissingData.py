from pymongo import MongoClient
import pandas as pd

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['PortfolioPruefung']

# Die originalen Daten holen
inspection_results = db['NYC.Restaurant.Inspection.Results']
yelp_business = db['yelp_business']

# Funktionen zur Überprüfung von Duplikaten und fehlenden Daten

def check_duplicates(collection, unique_field):
    """
    Prüft auf Duplikate basierend auf einem eindeutigen Feld (z.B. CAMIS oder business_id).
    Gibt eine Zusammenfassung der Duplikate zurück.
    """
    cursor = collection.aggregate([
        {"$group": {"_id": f"${unique_field}", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ])
    duplicates = list(cursor)
    if duplicates:
        print(f"\nDuplikate basierend auf {unique_field}:")
        for duplicate in duplicates:
            print(f"ID: {duplicate['_id']} hat {duplicate['count']} Einträge")
    else:
        print(f"\nKeine Duplikate basierend auf {unique_field} gefunden.")

def check_missing_data(collection, fields):
    """
    Prüft auf fehlende Daten in den angegebenen Feldern.
    Gibt eine Zusammenfassung der fehlenden Daten zurück.
    """
    for field in fields:
        cursor = collection.find({field: {"$exists": False}})
        missing_entries = list(cursor)
        if missing_entries:
            print(f"\nFehlende Daten im Feld '{field}': {len(missing_entries)} Einträge")
        else:
            print(f"\nKeine fehlenden Daten im Feld '{field}'.")

def check_invalid_lat_long(collection):
    """
    Prüft, ob die Geodaten (Latitude, Longitude) im gültigen Bereich liegen.
    (Latitude: -90 bis 90, Longitude: -180 bis 180)
    """
    cursor = collection.find({
        "Latitude": {"$not": {"$gte": -90, "$lte": 90}},
        "Longitude": {"$not": {"$gte": -180, "$lte": 180}}
    })
    invalid_geo_entries = list(cursor)
    if invalid_geo_entries:
        print(f"\nUngültige Geodaten: {len(invalid_geo_entries)} Einträge")
    else:
        print("\nAlle Geodaten sind gültig.")

# Teste Duplikate für 'CAMIS' in inspection_results
check_duplicates(inspection_results, 'CAMIS')

# Teste Duplikate für 'business_id' in yelp_business
check_duplicates(yelp_business, 'business_id')

# Teste auf fehlende Daten in spezifischen Feldern
inspection_fields = ['BUILDING', 'STREET', 'DBA', 'Latitude', 'Longitude', 'ZIPCODE', 'BORO']
check_missing_data(inspection_results, inspection_fields)

yelp_fields = ['name', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude']
check_missing_data(yelp_business, yelp_fields)

# Teste auf ungültige Geodaten
check_invalid_lat_long(inspection_results)
check_invalid_lat_long(yelp_business)
