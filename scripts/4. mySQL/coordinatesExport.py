import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my-secret-pw",
    port=3306,
    database="PortfolioPruefung"
)

cursor = conn.cursor()

# Drop views if they already exist
cursor.execute("DROP VIEW IF EXISTS A_inspections")
cursor.execute("DROP VIEW IF EXISTS B_inspections")
cursor.execute("DROP VIEW IF EXISTS C_inspections")
cursor.execute("DROP VIEW IF EXISTS all_inspections")

# Create views
cursor.execute("""
    CREATE VIEW A_inspections AS
    SELECT ir.business_id, ir.inspection_date, ir.score, yb.latitude, yb.longitude, yb.borough, yb.postal_code
    FROM inspection_results ir
    JOIN yelp_business yb ON ir.business_id = yb.business_id
    WHERE ir.score BETWEEN 0 AND 13
""")

cursor.execute("""
    CREATE VIEW B_inspections AS
    SELECT ir.business_id, ir.inspection_date, ir.score, yb.latitude, yb.longitude, yb.borough, yb.postal_code
    FROM inspection_results ir
    JOIN yelp_business yb ON ir.business_id = yb.business_id
    WHERE ir.score BETWEEN 14 AND 27
""")

cursor.execute("""
    CREATE VIEW C_inspections AS
    SELECT ir.business_id, ir.inspection_date, ir.score, yb.latitude, yb.longitude, yb.borough, yb.postal_code
    FROM inspection_results ir
    JOIN yelp_business yb ON ir.business_id = yb.business_id
    WHERE ir.score BETWEEN 28 AND 100
""")

cursor.execute("""
    CREATE VIEW all_inspections AS
    SELECT ir.business_id, ir.inspection_date, ir.score, yb.latitude, yb.longitude, yb.borough, yb.postal_code
    FROM inspection_results ir
    JOIN yelp_business yb ON ir.business_id = yb.business_id
""")

# Commit and close connection
conn.commit()
cursor.close()
conn.close()

print("Views created successfully.")