from pymongo import MongoClient

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['PortfolioPruefung']

# Die Mappings aus der Collection "mapping" holen
mappings = db.mapping.find()

# Die originalen Daten holen
inspection_results = db['inspection_results']
yelp_business = db['yelp_business']

# Fake-Collections erstellen
fake_inspection_results = db.fake_inspection_results
fake_yelp_business = db.fake_yelp_business

for mapping in mappings:
    # Alle entsprechenden Dokumente aus inspection_results holen
    inspection_docs = list(inspection_results.find({'CAMIS': mapping['CAMIS']}))  # In eine Liste konvertieren

    # Falls keine Dokumente gefunden werden, Fehlermeldung ausgeben
    if not inspection_docs:
        print(f"Keine Einträge für CAMIS {mapping['CAMIS']} gefunden.")
        continue

    # Jedes Dokument verarbeiten
    for inspection_doc in inspection_docs:
        # Kopie des Inspektionsdatensatzes erstellen und CAMIS ersetzen
        fake_inspection_doc = inspection_doc.copy()
        fake_inspection_doc['CAMIS'] = mapping['business_id']  # CAMIS durch business_id ersetzen
        fake_inspection_results.insert_one(fake_inspection_doc)

    # Yelp-Daten holen und anpassen
    yelp_data = yelp_business.find_one({'business_id': mapping['business_id']})

    if yelp_data:
        fake_yelp_entry = yelp_data.copy()

        # Yelp-Daten mit Informationen aus einer beliebigen Inspektion ergänzen
        example_inspection = inspection_docs[0]
        fake_yelp_entry['name'] = example_inspection.get('DBA', 'Unbekannt')

        # Adresse zusammenfügen
        building = example_inspection.get('BUILDING', '')
        street = example_inspection.get('STREET', '')
        fake_yelp_entry['address'] = f"{building} {street}".strip()

        # Stadt und PLZ übernehmen
        fake_yelp_entry['city'] = example_inspection.get('BORO', 'Unbekannt')
        fake_yelp_entry['postal_code'] = example_inspection.get('ZIPCODE', 'Unbekannt')

        # Geodaten übernehmen
        fake_yelp_entry['latitude'] = example_inspection.get('Latitude', None)
        fake_yelp_entry['longitude'] = example_inspection.get('Longitude', None)

        # Fehlende Geodaten melden
        if fake_yelp_entry['latitude'] is None or fake_yelp_entry['longitude'] is None:
            print(f"Geodaten fehlen für CAMIS {mapping['CAMIS']}.")

        # Yelp-Daten einfügen
        fake_yelp_business.insert_one(fake_yelp_entry)
