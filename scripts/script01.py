# SCRIPT 1 — CONVERTER userid-timestamp-artid-artname-traid-traname.tsv
# para istening_events.csv
import csv
import os

# Corre Python no diretorio atual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

input_file = "userid-timestamp-artid-artname-traid-traname.tsv"
output_file = "listening_events.csv"

with open(input_file, "r", encoding="utf-8", errors="ignore") as fin, \
     open(output_file, "w", newline="", encoding="utf-8") as fout:

    reader = csv.reader(fin, delimiter="\t")
    writer = csv.writer(fout)

    # header
    writer.writerow(["user_id", "artist_id", "artist_name", "timestamp"])

    for row in reader:
        if len(row) < 4:
            continue

        user_id = row[0].strip()
        timestamp = row[1].strip()
        artist_id = row[2].strip()
        artist_name = row[3].strip()

        if user_id and artist_id:
            writer.writerow([user_id, artist_id, artist_name, timestamp])

print("✅ listening_events.csv gerado")