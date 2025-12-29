import requests
from pathlib import Path

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"

def main():
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / "online_retail.xlsx"

    print("Downloading dataset...")
    r = requests.get(URL, timeout=60)
    r.raise_for_status()
    out_path.write_bytes(r.content)

    print(f"Saved file to: {out_path}")

if __name__ == "__main__":
    main()