import mysql.connector
import folium
from folium.plugins import HeatMap
from decimal import Decimal

def fetch_coordinates():
    """Fetch latitude, longitude, and score from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="my-secret-pw",
            port=3306,
            database="PortfolioPruefung"
        )
        
        cursor = connection.cursor()
        query = """
            SELECT DISTINCT latitude, longitude, score
            FROM PortfolioPruefung.all_inspections
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
        """
        cursor.execute(query)
        coordinates = cursor.fetchall()
        connection.close()
        print(f"Fetched {len(coordinates)} coordinates.")
        return coordinates
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return []

def plot_coordinates_with_folium(coordinates, center, zoom_start, output_file):
    """Plot the fetched coordinates on a map using Folium."""
    # Convert Decimal to float and filter out invalid coordinates
    valid_coordinates = [(float(lat), float(lon), int(score)) for lat, lon, score in coordinates if isinstance(lat, Decimal) and isinstance(lon, Decimal)]
    
    # Normalize scores for color mapping
    lats_longs_weights = [[lat, lon, min(score / 30, 1)] for lat, lon, score in valid_coordinates]  # Normalize scores to range [0, 1], clamping at 30
    
    # Create the map
    map_obj = folium.Map(location=center, zoom_start=zoom_start)
    
    # Add heatmap
    HeatMap(lats_longs_weights).add_to(map_obj)
    
    # Save the map as an HTML file
    map_obj.save(output_file)
    print(f"Heatmap saved as '{output_file}'.")

def main():
    coordinates = fetch_coordinates()
    
    # Plot the entire NYC area
    plot_coordinates_with_folium(coordinates, [40.7128, -74.0060], 10, 'nyc_heatmap.html')
    
    # Plot Manhattan only
    plot_coordinates_with_folium(coordinates, [40.7831, -73.9712], 12, 'manhattan_heatmap.html')

if __name__ == "__main__":
    main()