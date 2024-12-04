from pymongo import MongoClient

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['PortfolioPruefung']

# Standardwerte für fehlende Felder (nur Geodaten und Adressfelder als None)
default_values = {
    'BUILDING': None,
    'STREET': None,
    'ZIPCODE': None,
    'Latitude': None,  # Geodaten werden später geprüft
    'Longitude': None
}


# Funktion zum Ersetzen von fehlenden Werten und Löschen von Datensätzen mit fehlenden Geodaten
def replace_missing_and_delete_geodata():
    # Sammlung für fake_inspection_results
    inspection_results_collection = db['fake_inspection_results']
    yelp_business_collection = db['fake_yelp_business']
    mapping_collection = db['mapping']

    # Alle Dokumente in fake_inspection_results durchgehen
    for inspection_result in inspection_results_collection.find():
        # Überprüfen, ob Geodaten fehlen
        if not inspection_result.get('Latitude') or not inspection_result.get('Longitude'):
            # Wenn Geodaten fehlen, löschen auch den entsprechenden Yelp-Eintrag
            business_id = inspection_result.get('CAMIS')
            yelp_business_collection.delete_one({'business_id': business_id})  # Yelp-Datensatz löschen
            inspection_results_collection.delete_one({'CAMIS': business_id})  # Fake Inspection-Datensatz löschen
            continue

        # Fehlende Felder durch Standardwerte ersetzen
        updated_result = {}
        for field, default_value in default_values.items():
            if field not in inspection_result or inspection_result[field] in [None, ""]:
                updated_result[field] = default_value
            else:
                updated_result[field] = inspection_result[field]

        # Datensatz aktualisieren
        inspection_results_collection.update_one(
            {'_id': inspection_result['_id']},
            {'$set': updated_result}
        )
        # Hier könnte man optional auch den Yelp-Eintrag mit weiteren Informationen aktualisieren, falls gewünscht.


# Funktion aufrufen
replace_missing_and_delete_geodata()
