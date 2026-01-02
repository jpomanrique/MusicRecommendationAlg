# SCRIPT 2 — CONVERTER usersha1-artmbid-artname-plays.tsv
# para user_artist_plays.csv

import csv
import os

# Corre Python no diretorio atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

input_file = "usersha1-artmbid-artname-plays.tsv"
output_file = "user_artist_plays.csv"

with open(input_file, "r", encoding="utf-8", errors="ignore") as fin, \
     open(output_file, "w", newline="", encoding="utf-8") as fout:

    reader = csv.reader(fin, delimiter="\t")
    writer = csv.writer(fout)

    # header
    writer.writerow(["user_id", "artist_id", "artist_name", "plays"])

    for row in reader:
        if len(row) < 4:
            continue

        user_id = row[0].strip()
        artist_id = row[1].strip() or "UNKNOWN"
        artist_name = row[2].strip()
        plays = row[3].strip()

        if user_id and artist_name and plays.isdigit():
            writer.writerow([user_id, artist_id, artist_name, int(plays)])

print("✅ user_artist_plays.csv gerado")
