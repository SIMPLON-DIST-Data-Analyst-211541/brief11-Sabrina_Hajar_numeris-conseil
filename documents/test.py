from pathlib import Path

for fichier in Path(".").rglob("world-data-2023-clean.csv"):
    print(fichier.resolve())