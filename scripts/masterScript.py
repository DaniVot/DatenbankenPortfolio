import subprocess
import os

# Get the base directory (assuming this script is in the folder "3. data cleansing")
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define the scripts to execute in order, with their relative paths
scripts = [
    os.path.join(base_dir, "2. faking data", "fakingScript.py"),
    os.path.join(base_dir, "3. data cleansing", "consistencyCheck.py"),
    os.path.join(base_dir, "3. data cleansing", "consistencyEnforcer.py"),
    os.path.join(base_dir, "3. data cleansing", "deleteEmptyInspection.py"),
    os.path.join(base_dir, "3. data cleansing", "deleteEmptyYelpBusiness.py"),
    os.path.join(base_dir, "3. data cleansing", "searchDuplicates.py"),
    os.path.join(base_dir, "4. mySQLImport", "import.py")
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
