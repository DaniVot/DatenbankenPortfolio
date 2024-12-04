from pymongo import MongoClient

# Verbindung zur MongoDB herstellen
client = MongoClient("mongodb://localhost:27017/")  # Passe die Verbindung bei Bedarf an
db = client["PortfolioPruefung"]  # Ersetze "deine_datenbank" durch den Namen deiner Datenbank

# Collections auswählen
fake_yelp_business = db["fake_yelp_business"]
fake_inspection_results = db["fake_inspection_results"]

# Finde alle Inspektionen ohne Score
inspections_without_score = fake_inspection_results.find({"SCORE": {"$exists": False}})

# Extrahiere alle CAMIS (business_ids) von Inspektionen ohne Score
business_ids_without_score = [inspection["CAMIS"] for inspection in inspections_without_score]

# Lösche Inspektionen ohne Score
result_inspection = fake_inspection_results.delete_many({"SCORE": {"$exists": False}})
print(f"Gelöschte Inspektionen ohne Score: {result_inspection.deleted_count}")

# Lösche alle Restaurants, die keine Inspektionen mehr haben
for business_id in business_ids_without_score:
    # Prüfe, ob noch Inspektionen für dieses Restaurant existieren
    remaining_inspections = fake_inspection_results.count_documents({"CAMIS": business_id})
    
    # Wenn keine Inspektionen mehr vorhanden sind, lösche das Restaurant aus fake_yelp_business
    if remaining_inspections == 0:
        result_yelp = fake_yelp_business.delete_one({"business_id": business_id})
        if result_yelp.deleted_count > 0:
            print(f"Restaurant mit Business ID {business_id} wurde gelöscht.")
        else:
            print(f"Restaurant mit Business ID {business_id} konnte nicht gelöscht werden.")
