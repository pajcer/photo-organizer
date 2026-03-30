import os
import shutil
import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

# --- Mappa bekérés ---
forras = Path(input("Add meg a forrás mappát: ").strip())
cel = Path(input("Add meg a cél mappát: ").strip())

# --- Megerősítés ---
print("\n--- ÖSSZEFOGLALÓ ---")
print(f"Forrás: {forras}")
print(f"Cél:    {cel}")
print("--------------------")

while True:
    valasz = input("Elkezdhetem a másolást? (igen/nem): ").strip().lower()
    if valasz in ["igen", "i"]:
        break
    elif valasz in ["nem", "n"]:
        print("Művelet megszakítva.")
        exit()
    else:
        print("Kérlek 'igen' vagy 'nem'-et írj.")

print("\nMásolás indul...\n")

media_ext = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi", ".heic", ".webp", ".mkv"}

def get_exif_datetime(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag in ("DateTimeOriginal", "DateTime"):
                try:
                    return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                except Exception:
                    pass
        return None
    except Exception:
        return None

for gyoker, _, fajlok in os.walk(forras):
    for f in fajlok:
        kiterj = os.path.splitext(f)[1].lower()
        if kiterj in media_ext:
            teljes_ut = Path(gyoker) / f
            try:
                exif_datum = get_exif_datetime(teljes_ut)
                if exif_datum:
                    datum = exif_datum
                else:
                    datum = datetime.datetime.fromtimestamp(os.path.getmtime(teljes_ut))

                ev = str(datum.year)
                honap = f"{datum.month:02d}"

                cel_mappa = cel / ev / honap
                cel_mappa.mkdir(parents=True, exist_ok=True)

                cel_fajl = cel_mappa / f
                sorszam = 1
                while cel_fajl.exists():
                    nev, ext = os.path.splitext(f)
                    cel_fajl = cel_mappa / f"{nev}_{sorszam}{ext}"
                    sorszam += 1

                shutil.copy2(teljes_ut, cel_fajl)
                print(f"Másolva: {cel_fajl}")

            except Exception as e:
                print(f"Hiba: {teljes_ut} -> {e}")