from pymongo import MongoClient

# MongoDB-Verbindung aufbauen
client = MongoClient('mongodb://localhost:27017/')
db = client['NYAnalyse']

# Die Mappings aus der Collection "mapping" holen
mappings = db.mapping.find()

# Die originalen Daten holen
inspection_results = db['inspections']
yelp_business = db['yelpBusiness']

# Fake-Collections erstellen
fake_inspection_results = db.fake_inspection_results
fake_yelp_business = db.fake_yelp_business

for mapping in mappings:
    # Für jedes Mapping die entsprechenden Dokumente holen
    inspection_result = inspection_results.find_one({'CAMIS': mapping['CAMIS']})
    yelp_data = yelp_business.find_one({'business_id': mapping['business_id']})

    # Fehlerbehandlung, falls das inspection_result Dokument nicht existiert
    if inspection_result is None:
        print(f"Kein Eintrag für CAMIS {mapping['CAMIS']} gefunden.")
        continue

    # Erstellen der fake_inspection_results Collection
    fake_inspection_result = inspection_result.copy()
    fake_inspection_result['CAMIS'] = mapping['business_id']  # CAMIS durch business_id ersetzen
    fake_inspection_results.insert_one(fake_inspection_result)

    # Erstellen der fake_yelp_business Collection
    fake_yelp_entry = yelp_data.copy()

    # Name von NYC Inspection übernehmen
    fake_yelp_entry['name'] = inspection_result.get('DBA', 'Unbekannt')

    # Adresse von NYC Inspection übernehmen (mit Fehlerbehandlung)
    building = inspection_result.get('BUILDING', '')
    street = inspection_result.get('STREET', '')
    fake_yelp_entry['address'] = f"{building} {street}".strip()  # Adresse zusammenfügen

    # Stadt und PLZ von NYC Inspection übernehmen
    fake_yelp_entry['city'] = inspection_result.get('BORO', 'Unbekannt')
    fake_yelp_entry['postal_code'] = inspection_result.get('ZIPCODE', 'Unbekannt')

    # Geodaten von NYC Inspection übernehmen
    fake_yelp_entry['latitude'] = inspection_result.get('Latitude', None)
    fake_yelp_entry['longitude'] = inspection_result.get('Longitude', None)

    # Wenn Geodaten fehlen, setzen wir sie auf None (oder einen Standardwert)
    if fake_yelp_entry['latitude'] is None or fake_yelp_entry['longitude'] is None:
        print(f"Geodaten fehlen für CAMIS {mapping['CAMIS']}.")

    fake_yelp_business.insert_one(fake_yelp_entry)