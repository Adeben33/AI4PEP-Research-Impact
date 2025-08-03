import os
import csv
import json

# Base directory
base_path = '/Users/adeben/Desktop/AI4PEP'

# Known variants of Jude Kong (case-insensitive)
jude_kong_variants = [
    "jude kong",
    "jude dzevela kong",
    "jude d. kong",
    "jd kong",
    "j. d. kong",
    "kong, jude"
]

# Helper: detect Jude Kong in author list
def contains_jude_kong(authors_field):
    if not authors_field:
        return False
    authors = [a.strip().lower() for a in authors_field.split(" and ")]
    return any(any(variant in author for variant in jude_kong_variants) for author in authors)

# Helper: safe year extraction
def safe_year(entry):
    try:
        return int(entry.get("Year", 0))
    except (ValueError, TypeError):
        return 0

# Loop through folders
folders = [f for f in os.listdir(base_path)
           if os.path.isdir(os.path.join(base_path, f))]

for folder in folders:
    folder_path = os.path.join(base_path, folder)
    csv_path = os.path.join(folder_path, 'impact_metrics.csv')
    output_json_path = os.path.join(folder_path, 'jude_kong_filtered.json')

    if not os.path.exists(csv_path):
        print(f"⚠️  Skipped (no CSV): {csv_path}")
        continue

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            filtered_rows = [
                row for row in reader
                if contains_jude_kong(row.get("Authors", "")) and safe_year(row) >= 2024
            ]

        with open(output_json_path, 'w', encoding='utf-8') as out_file:
            json.dump(filtered_rows, out_file, indent=2)

        print(f"✅ {folder}: Saved {len(filtered_rows)} filtered entries to {output_json_path}")

    except Exception as e:
        print(f"❌ Error in '{folder}': {str(e)} — Skipped.")
