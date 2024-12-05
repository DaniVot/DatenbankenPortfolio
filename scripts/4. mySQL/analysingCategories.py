import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime

# MySQL-Verbindung herstellen
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    port=3306,
    database="PortfolioPruefung"
)

# Mapping von Cuisine zu Kategorie
cuisine_to_category = {
    'American': 'Amerikanische Küche', 'Soul Food': 'Amerikanische Küche', 'Barbecue': 'Amerikanische Küche', 'Sandwiches': 'Amerikanische Küche', 'Hotdogs': 'Amerikanische Küche', 
    'Hamburgers': 'Amerikanische Küche', 'New American': 'Amerikanische Küche', 'Californian': 'Amerikanische Küche', 'Tex-Mex': 'Amerikanische Küche', 
    'Sandwiches/Salads/Mixed Buffet': 'Amerikanische Küche', 'Soups/Salads/Sandwiches': 'Amerikanische Küche', 'Creole/Cajun': 'Amerikanische Küche', 
    'Creole': 'Amerikanische Küche', 'Cajun': 'Amerikanische Küche', 'Southern': 'Amerikanische Küche', 
    'Italian': 'Europäische Küche', 'French': 'Europäische Küche', 'German': 'Europäische Küche', 'Spanish': 'Europäische Küche', 'Portuguese': 'Europäische Küche', 
    'Greek': 'Europäische Küche', 'Mediterranean': 'Europäische Küche', 'English': 'Europäische Küche', 'Polish': 'Europäische Küche', 'Russian': 'Europäische Küche', 
    'Scandinavian': 'Europäische Küche', 'New French': 'Europäische Küche', 'Basque': 'Europäische Küche', 'Dutch': 'Europäische Küche', 'Eastern European': 'Europäische Küche', 
    'Czech': 'Europäische Küche', 'Austrian': 'Europäische Küche', 'Haute Cuisine': 'Europäische Küche', 
    'Chinese': 'Asiatische Küche', 'Japanese': 'Asiatische Küche', 'Korean': 'Asiatische Küche', 'Indian': 'Asiatische Küche', 'Thai': 'Asiatische Küche', 
    'Vietnamese': 'Asiatische Küche', 'Filipino': 'Asiatische Küche', 'Indonesian': 'Asiatische Küche', 'Chinese/Cuban': 'Asiatische Küche', 'Chinese/Japanese': 'Asiatische Küche', 
    'Southeast Asian': 'Asiatische Küche', 'Asian/Asian Fusion': 'Asiatische Küche', 'Bangladeshi': 'Asiatische Küche', 'Pakistani': 'Asiatische Küche', 'Peruvian': 'Asiatische Küche', 
    'Fusion': 'Asiatische Küche', 'Moroccan': 'Asiatische Küche', 'Lebanese': 'Asiatische Küche', 'Turkish': 'Asiatische Küche', 'Middle Eastern': 'Asiatische Küche', 
    'Afghan': 'Asiatische Küche', 
    'African': 'Afrikanische Küche', 'Ethiopian': 'Afrikanische Küche', 'Egyptian': 'Afrikanische Küche', 
    'Mexican': 'Lateinamerikanische und Karibische Küche', 'Latin American': 'Lateinamerikanische und Karibische Küche', 'Caribbean': 'Lateinamerikanische und Karibische Küche', 
    'Brazilian': 'Lateinamerikanische und Karibische Küche', 'Peruvian': 'Lateinamerikanische und Karibische Küche', 'Cuban': 'Lateinamerikanische und Karibische Küche', 
    'Chilean': 'Lateinamerikanische und Karibische Küche', 
    'Pizza': 'Fast Food & Street Food', 'Donuts': 'Fast Food & Street Food', 'Bagels/Pretzels': 'Fast Food & Street Food', 'Pancakes/Waffles': 'Fast Food & Street Food', 
    'Tapas': 'Fast Food & Street Food', 'Hotdogs/Pretzels': 'Fast Food & Street Food', 'Sushi': 'Fast Food & Street Food', 'Chicken': 'Fast Food & Street Food', 
    'Seafood': 'Fast Food & Street Food', 'Bottled Beverages': 'Fast Food & Street Food', 'Juices/Smoothies/Fruit Salads': 'Fast Food & Street Food', 
    'Vegetarian': 'Gesunde und Vegetarische Küche', 'Vegan': 'Gesunde und Vegetarische Küche', 'Salads': 'Gesunde und Vegetarische Küche', 'Fruits/Vegetables': 'Gesunde und Vegetarische Küche', 
    'Soups': 'Gesunde und Vegetarische Küche', 'Juice': 'Gesunde und Vegetarische Küche', 'Smoothies': 'Gesunde und Vegetarische Küche', 'Fruit Salads': 'Gesunde und Vegetarische Küche', 
    'Bakery Products/Desserts': 'Sonstige', 'Frozen Desserts': 'Sonstige', 'Nuts/Confectionary': 'Sonstige', 'Not Listed/Not Applicable': 'Sonstige', 'Coffee/Tea': 'Sonstige', 
    'Sandwiches/Salads/Mixed Buffet': 'Sonstige', 'Fusion': 'Sonstige', 'Hawaiian': 'Sonstige', 'Chimichurri': 'Sonstige'
}

# Daten aus der MySQL-Datenbank abrufen
query_yelp = "SELECT * FROM yelp_business;"
query_inspection = "SELECT * FROM inspection_results;"

yelp_df = pd.read_sql(query_yelp, db_connection)
inspection_df = pd.read_sql(query_inspection, db_connection)

# Mappiere die Küchenarten zu den Kategorien
yelp_df['category'] = yelp_df['cuisine_description'].map(cuisine_to_category)

# Merge der beiden DataFrames basierend auf business_id
merged_df = pd.merge(inspection_df, yelp_df[['business_id', 'category']], on='business_id', how='inner')

# Filtere nur Inspektionen des letzten Jahres
current_year = datetime.now().year
last_year = current_year - 1
merged_df['inspection_date'] = pd.to_datetime(merged_df['inspection_date'])
merged_df = merged_df[merged_df['inspection_date'].dt.year == last_year]

# Datenbereinigung: Entfernen von Zeilen mit fehlenden Werten für Score oder Kategorie
merged_df = merged_df.dropna(subset=['score', 'category'])

# Konvertiere den Score in numerische Werte (falls noch nicht)
merged_df['score'] = pd.to_numeric(merged_df['score'], errors='coerce')

# Berechne Medianwerte des Scores pro Kategorie
category_scores = merged_df.groupby('category')['score'].median().reset_index()

# Visualisierung: Balkendiagramm der Medianwerte der Scores pro Kategorie
plt.figure(figsize=(12, 8))
sns.barplot(x='category', y='score', data=category_scores, palette='coolwarm')
plt.xticks(rotation=90)
plt.title('Median Gesundheitsscores pro Küchenkategorie im letzten Jahr')
plt.xlabel('Küchenkategorie')
plt.ylabel('Median Gesundheitsscore')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Gitterlinien hinzufügen
plt.tight_layout()  # Damit die Labels nicht abgeschnitten werden
plt.show()

# Statistischer Test: ANOVA, um zu prüfen, ob es signifikante Unterschiede zwischen den Kategorien gibt
anova_result = stats.f_oneway(
    *[merged_df[merged_df['category'] == category]['score'] for category in merged_df['category'].unique()]
)

print(f"ANOVA p-Wert: {anova_result.pvalue}")
if anova_result.pvalue < 0.05:
    print("Es gibt signifikante Unterschiede zwischen den Kategorien!")
else:
    print("Es gibt keine signifikanten Unterschiede zwischen den Kategorien.")

# Verbindung schließen
db_connection.close()
