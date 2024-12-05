import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# MySQL-Verbindung herstellen
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    port=3306,
    database="PortfolioPruefung"
)

# Yelp- und Inspektionsdaten abrufen
query_yelp = "SELECT business_id, stars FROM yelp_business;"
query_inspection = "SELECT business_id, score, inspection_date FROM inspection_results;"

yelp_df = pd.read_sql(query_yelp, db_connection)
inspection_df = pd.read_sql(query_inspection, db_connection)

# Filtere nur Inspektionen des letzten Jahres
current_year = datetime.now().year
last_year = current_year - 1
inspection_df['inspection_date'] = pd.to_datetime(inspection_df['inspection_date'])
inspection_df = inspection_df[inspection_df['inspection_date'].dt.year == last_year]

# Merge der beiden DataFrames basierend auf business_id
merged_df = pd.merge(inspection_df, yelp_df, on='business_id', how='inner')

# Datenbereinigung: Entferne fehlende Werte und konvertiere Daten in numerische Werte
merged_df = merged_df.dropna(subset=['score', 'stars'])
merged_df['score'] = pd.to_numeric(merged_df['score'], errors='coerce')
merged_df['stars'] = pd.to_numeric(merged_df['stars'], errors='coerce')

# Gruppiere die Daten nach Sternebewertung und berechne den Durchschnitt der Scores
grouped_df = merged_df.groupby('stars').agg(
    avg_score=('score', 'mean'),
    count=('score', 'size')
).reset_index()

# Visualisiere die Durchschnitts-Scores pro Yelp-Bewertung
plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_df, x='stars', y='avg_score', color='skyblue')
plt.title('Durchschnitt der Gesundheitsscores nach Yelp-Sternebewertung')
plt.xlabel('Yelp-Sternebewertung (1-5)')
plt.ylabel('Durchschnitt Gesundheitsinspektionsscore (höher = schlechter)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Visualisierung als Boxplot für die Verteilung der Scores
plt.figure(figsize=(10, 6))
sns.boxplot(data=merged_df, x='stars', y='score', color='skyblue')
plt.title('Verteilung der Gesundheitsscores nach Yelp-Sternebewertung')
plt.xlabel('Yelp-Sternebewertung (1-5)')
plt.ylabel('Gesundheitsinspektionsscore (höher = schlechter)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Verbindung schließen
db_connection.close()
