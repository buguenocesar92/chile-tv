import subprocess
import os
import json

CANALES = [
    ("TVN - 24 Horas",  "https://www.youtube.com/channel/UCTXNz3gjAypWp3EhlIATEJQ/live"),
    ("Canal 13 - T13",  "https://www.youtube.com/channel/UCsRnhjcUCR78Q3Ud6OXCTNg/live"),
    ("Chilevision",     "https://www.youtube.com/@Chilevision/live"),
    ("Meganoticias",    "https://www.youtube.com/channel/UCkccyEbqhhM3uKOI6Shm-4Q/live"),
]

CACHE_FILE = "cache.json"

def get_stream_url(yt_url):
    try:
        result = subprocess.run(
            ["/home/cesar/.local/bin/yt-dlp", "-g", "--no-warnings", yt_url],
            capture_output=True, text=True, timeout=60
        )
        lines = [l for l in result.stdout.strip().splitlines() if l.startswith("http")]
        return lines[0] if lines else None
    except Exception as e:
        print(f"  Error: {e}")
        return None

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Cargar cache anterior
cache = {}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE) as f:
        cache = json.load(f)

lines = ["#EXTM3U"]
for nombre, yt_url in CANALES:
    print(f"Extrayendo {nombre}...")
    url = get_stream_url(yt_url)
    if url:
        cache[nombre] = url
        print("  OK")
    elif nombre in cache:
        url = cache[nombre]
        print("  FALLO - usando URL anterior")
    else:
        print("  FALLO - sin fallback")
        continue
    lines.append(f'#EXTINF:-1 group-title="Chile",{nombre}')
    lines.append(url)

# Guardar cache actualizado
with open(CACHE_FILE, "w") as f:
    json.dump(cache, f)

with open("canales_chile.m3u", "w") as f:
    f.write("\n".join(lines))

subprocess.run(["git", "pull", "--rebase", "--autostash"])
subprocess.run(["git", "add", "canales_chile.m3u", CACHE_FILE])
subprocess.run(["git", "commit", "-m", "Update M3U"])
subprocess.run(["git", "push"])

print("\nListo.")