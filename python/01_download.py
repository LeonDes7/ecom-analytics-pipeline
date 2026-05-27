import requests
from pathlib import Path

# Source URL for the raw transactional Excel dataset
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"

def main():
    # Setup robust, cross-platform directory paths using pathlib
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "online_retail.xlsx"

    print("Downloading dataset...")
    # Stream the file content over HTTP with an explicit timeout to prevent hanging connections
    r = requests.get(URL, timeout=60)
    # Network Guardrail: Immediately raise an exception if the HTTP request failed (e.g., 404 or 500 error)
    r.raise_for_status()
    # Write the raw binary payload directly to disk
    out_path.write_bytes(r.content)

    print(f"Saved file to: {out_path}")

if __name__ == "__main__":
    main()