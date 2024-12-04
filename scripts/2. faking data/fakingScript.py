from pymongo import MongoClient, ASCENDING

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['PortfolioPruefung']

# Die originalen Daten holen
inspection_results = db['inspection_results']
yelp_business = db['yelp_business']

# Indizes erstellen, falls noch nicht vorhanden
inspection_results.create_index([('CAMIS', ASCENDING)])
yelp_business.create_index([('business_id', ASCENDING)])

# Die Mappings aus der Collection "mapping" holen
mappings = list(db.mapping.find())  # Hole alle Mappings auf einmal

# Fake-Collections erstellen
fake_inspection_results = db.fake_inspection_results
fake_yelp_business = db.fake_yelp_business

# Listen für Einfügungen erstellen
fake_inspection_docs = []
fake_yelp_docs = []

# Durchlaufe alle Mappings und bearbeite die Dokumente
for mapping in mappings:
    # Alle entsprechenden Dokumente aus inspection_results holen
    inspection_docs_cursor = list(inspection_results.find({'CAMIS': mapping['CAMIS']}))
    
    # Durch die gefundenen Inspektionsdokumente iterieren
    for inspection_doc in inspection_docs_cursor:
        # Kopie des Inspektionsdatensatzes erstellen und CAMIS ersetzen
        fake_inspection_doc = inspection_doc.copy()
        fake_inspection_doc['CAMIS'] = mapping['business_id']  # CAMIS durch business_id ersetzen
        fake_inspection_docs.append(fake_inspection_doc)

    # Yelp-Daten holen und anpassen
    yelp_data = yelp_business.find_one({'business_id': mapping['business_id']})
    
    if yelp_data and inspection_docs_cursor:
        fake_yelp_entry = yelp_data.copy()
        
        # Yelp-Daten mit Informationen aus einer beliebigen Inspektion ergänzen
        example_inspection = inspection_docs_cursor[0]  # Nehme das erste Inspektionsdokument
        fake_yelp_entry['name'] = example_inspection.get('DBA', None)
        
        # Adresse zusammenfügen
        building = example_inspection.get('BUILDING', None)
        street = example_inspection.get('STREET', None)
        fake_yelp_entry['address'] = f"{building} {street}".strip() if building or street else None

        # Stadt und PLZ übernehmen
        fake_yelp_entry['city'] = example_inspection.get('BORO', None)
        fake_yelp_entry['postal_code'] = example_inspection.get('ZIPCODE', None)

        # Geodaten übernehmen
        fake_yelp_entry['latitude'] = example_inspection.get('Latitude', None)
        fake_yelp_entry['longitude'] = example_inspection.get('Longitude', None)

        # Fehlende Geodaten melden
        if fake_yelp_entry['latitude'] is None or fake_yelp_entry['longitude'] is None:
            print(f"Geodaten fehlen für CAMIS {mapping['CAMIS']}.")

        # Yelp-Daten zur Liste hinzufügen
        fake_yelp_docs.append(fake_yelp_entry)

    # Wenn genug Inspektionsdokumente gesammelt sind, diese in einem Batch einfügen
    if len(fake_inspection_docs) >= 1000:  # Beispiel für Batchgröße
        fake_inspection_results.insert_many(fake_inspection_docs)
        fake_inspection_docs.clear()  # Liste leeren nach dem Einfügen

# Yelp-Daten in einem Batch einfügen
if fake_yelp_docs:
    fake_yelp_business.insert_many(fake_yelp_docs)
    fake_yelp_docs.clear()

# Restliche Inspektionsdokumente einfügen
if fake_inspection_docs:
    fake_inspection_results.insert_many(fake_inspection_docs)
    fake_inspection_docs.clear()

print("Datenverarbeitung abgeschlossen.")