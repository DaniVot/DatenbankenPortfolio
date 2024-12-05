import mysql.connector
import matlab.engine
from decimal import Decimal
import numpy as np

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

def plot_coordinates_in_matlab(coordinates, latlim, lonlim, output_file):
    """Plot the fetched coordinates on a map using MATLAB."""
    eng = matlab.engine.start_matlab()
    
    # Convert Decimal to float and filter out invalid coordinates
    valid_coordinates = [(float(lat), float(lon), int(score)) for lat, lon, score in coordinates if isinstance(lat, Decimal) and isinstance(lon, Decimal)]
    
    latitudes = [coord[0] for coord in valid_coordinates]
    longitudes = [coord[1] for coord in valid_coordinates]
    scores = [coord[2] for coord in valid_coordinates]
    
    # Normalize scores for color mapping
    norm_scores = [(score - min(scores)) / (max(scores) - min(scores)) for score in scores]
    colors = [(1 - norm_score, norm_score, 0) for norm_score in norm_scores]  # Green to red gradient
    
    latitudes = matlab.double(latitudes)
    longitudes = matlab.double(longitudes)
    colors = matlab.double(colors)

    # Create the map with specific limits
    eng.eval("figure('Color', 'none', 'Position', [100, 100, 1200, 800]);", nargout=0)
    eng.eval(f"ax = usamap({latlim}, {lonlim});", nargout=0)
    eng.eval("setm(ax, 'FFaceColor', 'none');", nargout=0)  # Transparent background
    eng.eval("hold on;", nargout=0)
    
    # Plot the coordinates with varying colors based on score
    eng.eval("colormap(ax, jet);", nargout=0)  # Use 'jet' colormap for blue to red gradient
    eng.scatterm(latitudes, longitudes, 20, colors, 'filled', nargout=0)  # Color points based on score
    eng.eval("hold off;", nargout=0)

    # Save as a PNG with transparency
    eng.eval("set(gcf, 'Color', 'none');", nargout=0)  # Ensure figure background is transparent
    eng.eval("set(gca, 'Color', 'none');", nargout=0)  # Ensure axes background is transparent
    eng.eval(f"exportgraphics(gcf, '{output_file}', 'BackgroundColor', 'none');", nargout=0)
    print(f"Heatmap saved as '{output_file}'.")
    eng.quit()

def main():
    coordinates = fetch_coordinates()
    
    # Plot the entire NYC area
    plot_coordinates_in_matlab(coordinates, [40.4774, 40.9176], [-74.2591, -73.7004], 'nyc_heatmap.png')
    
    # Plot Manhattan only
    plot_coordinates_in_matlab(coordinates, [40.6795, 40.8820], [-74.0479, -73.9067], 'manhattan_heatmap.png')

if __name__ == "__main__":
    main()