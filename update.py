import subprocess

CANALES = [
    ("TVN - 24 Horas",        "https://www.youtube.com/channel/UCTXNz3gjAypWp3EhlIATEJQ/live"),
    ("Canal 13 - T13",        "https://www.youtube.com/channel/UCsRnhjcUCR78Q3Ud6OXCTNg/live"),
    ("Chilevision Noticias",  "https://www.youtube.com/watch?v=LEZNra3U8jg"),
    ("Meganoticias",          "https://www.youtube.com/channel/UCkccyEbqhhM3uKOI6Shm-4Q/live"),
]

def get_stream_url(yt_url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", "--no-warnings", "--js-runtimes", "nodejs", yt_url],
            capture_output=True, text=True, timeout=60
        )
        print(f"  stdout: {result.stdout[:200]}")
        print(f"  stderr: {result.stderr[:200]}")
        lines = [l for l in result.stdout.strip().splitlines() if l.startswith("http")]
        return lines[0] if lines else None
    except Exception as e:
        print(f"  Excepcion: {e}")
        return None

lines = ["#EXTM3U"]
for nombre, yt_url in CANALES:
    print(f"Extrayendo {nombre}...")
    url = get_stream_url(yt_url)
    if url:
        lines.append(f'#EXTINF:-1 group-title="Chile",{nombre}')
        lines.append(url)
        print("  OK")
    else:
        print("  FALLO")

with open("canales_chile.m3u", "w") as f:
    f.write("\n".join(lines))

print("\ncanales_chile.m3u generado.")