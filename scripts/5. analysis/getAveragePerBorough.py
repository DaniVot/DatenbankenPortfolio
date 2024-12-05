import mysql.connector

def get_average_scores_per_borough():
    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="my-secret-pw",
            port=3306,
            database="PortfolioPruefung"
        )

        cursor = connection.cursor()

        # SQL query to get the average score per borough
        query = """
        SELECT borough, AVG(score) as average_score
        FROM all_inspections
        GROUP BY borough;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(f"{row[0]} {row[1]:.2f}")

        for row in results:
            # Print only Boroughs
            print(f"{row[0]}")

        for row in results:
            # Print only Average Scores
            print(f"{row[1]:.2f}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    get_average_scores_per_borough()