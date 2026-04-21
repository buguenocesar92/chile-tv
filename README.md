# Chile TV Proxy

Proxy para streaming de canales de television nacional chilena.
Resuelve los tokens de autenticacion que cambian diariamente en YouTube.

## Canales incluidos

- Canal 13
- CHV (Chilevision)
- TVN
- Mega

## El problema que resuelve

Los canales chilenos transmiten en vivo en YouTube pero cambian sus tokens
de seguridad casi a diario. Las listas M3U publicas quedan obsoletas en horas.

Este proxy resuelve el stream en tiempo real con yt-dlp cada vez que se solicita.

## Como funciona

    Smarters / VLC / TiviMate
            |
    GET /stream/tvn
            |
    proxy.py -> yt-dlp -> URL real del stream
            |
    Stream de video en vivo

## Instalacion

    git clone https://github.com/buguenocesar92/chile-tv.git
    cd chile-tv
    pip install flask yt-dlp --break-system-packages

## Uso

    python3 proxy.py
    # Servidor en http://localhost:5000

    # Agregar en tu app de IPTV:
    # http://TU_IP:5000/playlist.m3u

## Endpoints

    GET /playlist.m3u    <- lista M3U con los 4 canales
    GET /stream/tvn      <- stream de TVN
    GET /stream/t13      <- stream de Canal 13
    GET /stream/chv      <- stream de Chilevision
    GET /stream/mega     <- stream de Mega

## Deploy recomendado

Raspberry Pi en tu red local con IP fija.
Opcionalmente exponer con subdominio via Cloudflare DDNS.

    tv.tudominio.cl/playlist.m3u

## Stack

- Python 3.12 + Flask
- yt-dlp
- GitHub Actions (actualizacion automatica de URLs)

---

Parte del ecosistema KraftDo SpA — digitalizamos PYMEs chilenas.
https://kraftdo.cl
