import subprocess
import os
import sys

def run_command(step_name, command, cwd=None):
    """Utility to run a command and print status."""
    print(f"\n{'='*10} STARTING: {step_name} {'='*10}")
    try:
        # We use shell=True for Windows compatibility
        result = subprocess.run(command, shell=True, check=True, cwd=cwd)
        print(f"✅ SUCCESS: {step_name} completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {step_name} failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    # Get the absolute path of where this script is sitting
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Run the Extraction Script
    run_command(
        "Data Extraction", 
        f"python python/01_download.py"
    )

    # Step 2: Run the Cleaning & Validation Script
    run_command(
        "Data Cleaning", 
        f"python python/03_clean_validate.py"
    )

    # Step 3: Run dbt Transformations
    # We tell Python to run dbt inside the dbt_project folder
    dbt_path = os.path.join(base_path, "dbt_project")
    run_command(
        "dbt Analytics Transformations", 
        "dbt run --profiles-dir .", 
        cwd=dbt_path
    )

    # Step 4: Run dbt Tests (Data Quality)
    run_command(
        "Data Quality Testing", 
        "dbt test --profiles-dir .", 
        cwd=dbt_path
    )

    print("\n" + "="*35)
    print("🚀 FULL PIPELINE EXECUTED SUCCESSFULLY!")
    print("="*35)