import subprocess
import os

# Get the base directory (assuming this script is in "scripts")
base_dir = os.path.dirname(__file__)

# Define the scripts to execute in the desired sequence
scripts = [
    os.path.join(base_dir, "2. faking data", "fakingScript.py"),
    os.path.join(base_dir, "3. data cleansing", "consistencyCheck.py"),
    os.path.join(base_dir, "3. data cleansing", "consistencyEnforcement.py"),
    os.path.join(base_dir, "3. data cleansing", "removeMissingGeoData.py"),
    os.path.join(base_dir, "3. data cleansing", "removeMissingScore.py"),
    os.path.join(base_dir, "3. data cleansing", "deleteRestaurantsWithoutInspections.py"),
    os.path.join(base_dir, "3. data cleansing", "dataTypesCheck.py"),
    os.path.join(base_dir, "3. data cleansing", "searchDuplicates.py"),
    os.path.join(base_dir, "4. mySQLExport", "export.py"),
]

# Loop through and execute each script
for script in scripts:
    print(f"Executing {script}...")
    try:
        subprocess.run(["python", script], check=True)  # Execute each script
        print(f"Finished {script}")
    except subprocess.CalledProcessError as e:
        print(f"Error while executing {script}: {e}")
        break  # Stop execution if a script fails
