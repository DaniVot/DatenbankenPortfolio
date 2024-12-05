from pymongo import MongoClient

# Verbindung zur MongoDB herstellen
client = MongoClient("mongodb://localhost:27017/")  # Passe die Verbindung bei Bedarf an
db = client["deine_datenbank"]  # Ersetze "deine_datenbank" durch den Namen deiner Datenbank

# Collection auswählen
fake_inspection_results = db["fake_inspection_results"]

# Alle Datensätze mit SCORE iterieren, bei denen GRADE nicht existiert
bulk_updates = []  # Liste, um Batch-Updates zu sammeln

for document in fake_inspection_results.find({"GRADE": {"$exists": False}}, {"_id": 1, "SCORE": 1}):
    score = document.get("SCORE")  # Holen des SCORE-Felds (in Großbuchstaben)

    try:
        # Sicherstellen, dass SCORE ein numerischer Wert ist
        score = float(score)

        # Grade berechnen
        if score < 14:
            grade = "A"
        elif 14 <= score <= 27:
            grade = "B"
        else:
            grade = "C"
    except (ValueError, TypeError):
        # Wenn SCORE ungültig ist, Grade auf null setzen
        grade = None

    # Batch-Update vorbereiten
    bulk_updates.append(
        {
            "updateOne": {
                "filter": {"_id": document["_id"]},
                "update": {"$set": {"GRADE": grade}}
            }
        }
    )

# Updates in einem Batch ausführen, falls Änderungen vorliegen
if bulk_updates:
    result = fake_inspection_results.bulk_write(bulk_updates)
    print(f"{result.modified_count} Dokumente erfolgreich aktualisiert.")
else:
    print("Keine Dokumente zu aktualisieren.")

print("Grades wurden erfolgreich berechnet und aktualisiert.")
