### **Use Case: Effizienzsteigerung der Inspektionsprozesse des DOHMH**

#### **Hintergrund:**
Das **Department of Health and Mental Hygiene (DOHMH)** hat die Herausforderung, die Einhaltung von Gesundheitsvorschriften in einer großen Anzahl von Restaurants (ca. 29 000) in New York City zu überwachen. Aufgrund begrenzter personeller Ressourcen ist eine gleichmäßig intensive Kontrolle aller Restaurants nicht möglich. Potenzielle Verstöße in Hochrisikobereichen oder bei wiederholt auffälligen Restaurantkategorien könnten unentdeckt bleiben. 

#### **Zielsetzung:**
Das DOHMH hat DataBros, kurz DB (eine Datenanalysefirma) damit beauftragt, eine datenbasierte Entscheidungsgrundlage zu entwickeln, um die Effizienz und Effektivität von Inspektionen zu verbessern. Der Schwerpunkt liegt darauf:  
1. **Hotspots von Gesundheitsverstößen** zu identifizieren.  
2. Restaurantkategorien zu erkennen, die regelmäßig Verstöße aufweisen.  

Das Ziel ist es, Inspektoren gezielt auf risikobehaftete Restaurants und Regionen zu fokussieren, sodass:  
- **Zeit eingespart** wird,  
- **Personalressourcen entlastet** werden, und  
- die **Qualität und Relevanz der Inspektionen** verbessert wird.  

Korellationskoeffiziert zwischen Bewertung auf yelp und dem Inspektions-Score.

---

#### **Genutzte Datensätze:**
1. **Yelp-Datensatz:**  
   - Gefakt und angepasst für die Bedürfnisse des Projekts, enthält Restaurantbewertungen, Kategorien und Check-in-Muster.  
2. **DOHMH-Inspektionsresultate:**  
   - Originaldatensatz mit Gesundheitsnoten, Verstoßdetails und geografischen Informationen.  
3. **Foursquare-Check-in-Datensatz:**  
   - Daten über Kundenaktivität und Check-in-Muster, die mit anderen Quellen verknüpft werden.  

---

#### **Eingesetzte Datenbankstruktur:**
- **Datenaufbereitung:**  
  - Die Daten werden mit **MongoDB** und **Python** aufbereitet, bereinigt und synthetisch ergänzt.  
  - Gründe für MongoDB:
    - Flexible Datenstruktur während der Datenbereinigung.
    - Effektives Handling von GeoJSON-Daten.  
- **Analyse:**  
  - Die bereinigten Daten werden in **MySQL** importiert und weiterverarbeitet.  
  - Gründe für MySQL:
    - Strukturierte Analysen und schnelle Aggregationen.
    - Indizes werden auf Feldern wie **Geodaten**, **Restaurant-ID**, und **Kategorie** gesetzt, um Abfragen zu beschleunigen.  

---

#### **Tools und Methoden:**
- **Datenaufbereitung:**  
  - **Python** (Pandas, NumPy) für Datenbereinigung, Transformation und Scripting.  
- **Visualisierung:**  
  - **Maptive** für interaktive Kartendarstellungen der Hotspots.  
- **Analyse:**  
  - **SQL** für Abfragen wie Clusteranalysen, Häufigkeitsverteilungen und Zeitreihenanalysen.  

---

#### **Entscheidungskriterien:**
1. **Hotspots:**  
   - Identifikation basierend auf dem **Gesundheitsscore** (z. B. Scores oberhalb eines bestimmten Schwellenwerts markieren Hotspots).  
2. **Risikokategorien:**  
   - Analyse der Häufigkeit und Art von Verstößen in verschiedenen Restaurantkategorien (z. B. Fast Food, italienisch).  
3. **Zeitliche Muster:**  
   - Untersuchung, ob bestimmte Zeiten oder Jahresperioden mit höheren Verstoßzahlen korrelieren.  

---

#### **Erwarteter Nutzen:**
- **Gezielte Inspektionen:**  
  Inspektoren können priorisiert Hotspots und Hochrisikokategorien überprüfen.  
- **Effiziente Ressourcenverteilung:**  
  Bessere Planung und Entlastung des Personals.  
- **Proaktive Maßnahmen:**  
  Identifizierung von wiederkehrenden Problemfeldern, um langfristig präventive Maßnahmen zu ermöglichen (z. B. gezielte Schulungen für Restauranttypen mit häufigen Verstößen).  

