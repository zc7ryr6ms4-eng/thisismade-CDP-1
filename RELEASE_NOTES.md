## Installieren

**Am einfachsten (Ubuntu 24.04 und neuer):** die Datei `thisismade-cd-player_*_all.deb` herunterladen und doppelt anklicken – das App-Zentrum installiert den Player samt allem, was er braucht.

**Oder im Terminal, ein Befehl:**
```bash
wget -qO- https://raw.githubusercontent.com/zc7ryr6ms4-eng/thisismade-CDP-1/main/install.sh | bash
```

**Als Snap:** die `.snap`-Datei herunterladen und
```bash
sudo snap install --dangerous ./thisismade-cd-player_*.snap
```
(`--dangerous` ist nötig, weil das Snap nicht aus dem Snap Store kommt.)

## macOS (13 Ventura und neuer, Apple Silicon und Intel)

**Ein Befehl im Terminal** – lädt die App, kopiert sie nach /Programme und startet sie:
```bash
curl -fsSL https://raw.githubusercontent.com/zc7ryr6ms4-eng/thisismade-CDP-1/main/install-mac.sh | bash
```

**Oder per DMG:** `ThisismadeCDPlayer.dmg` öffnen und die App auf „Programme“ ziehen. Weil die App nicht bei Apple notarisiert ist, beim ersten Start: Systemeinstellungen → Datenschutz & Sicherheit → „Dennoch öffnen“.
