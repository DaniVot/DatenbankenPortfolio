// Schritt 1: Alle eindeutigen Restaurants aus den Inspection Results extrahieren
const uniqueRestaurants = db.NYC.Restaurant.Inspection.Results.distinct("CAMIS");

// Schritt 2: Yelp-Restaurants mit ausreichend Bewertungen und Top-Bewertungen filtern
const topYelpRestaurants = db.yelp_business.aggregate([
    {
        $match: { review_count: { $gte: 10 } } // Mindestens 10 Bewertungen
    },
    {
        $sort: { stars: -1, review_count: -1 } // Nach Sternen und Bewertungen sortieren
    },
    {
        $limit: uniqueRestaurants.length // Genau so viele Yelp-Daten wie CAMIS-Einträge
    },
    {
        $project: { business_id: 1, _id: 0 } // Nur business_id extrahieren
    }
]).toArray();

// Schritt 3: Mapping zwischen CAMIS und Yelp erstellen
const mappingData = uniqueRestaurants.map((camis, index) => ({
    CAMIS: camis,
    business_id: topYelpRestaurants[index].business_id
}));

// Schritt 4: Mapping-Collection befüllen
db.mapping.insertMany(mappingData);