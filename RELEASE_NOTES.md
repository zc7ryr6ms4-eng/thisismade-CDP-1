## Windows 11

**`ThisismadeCDPlayer-Setup-1.0.0.exe`** herunterladen und starten. Bei der SmartScreen-Meldung „Der Computer wurde durch Windows geschützt“ auf **Weitere Informationen → Trotzdem ausführen** klicken (das Setup ist nicht kostenpflichtig signiert).
Ohne Installation: `ThisismadeCDPlayer-portable-win-x64.zip` entpacken und `ThisismadeCDPlayer.exe` starten.

## Ubuntu / Linux

**Am einfachsten (Ubuntu 24.04 und neuer):** die Datei `thisismade-cd-player_*_all.deb` herunterladen und doppelt anklicken – das App-Zentrum installiert den Player samt allem, was er braucht.

**Oder im Terminal, ein Befehl:**
```bash
wget -qO- https://raw.githubusercontent.com/zc7ryr6ms4-eng/thisismade-CDP-1/main/install.sh | bash
```

**Als Snap:** die `.snap`-Datei herunterladen und
```bash
sudo snap install --dangerous ./thisismade-cd-player_*.snap
```
(`--dangerous` ist nötig, weil das Snap nicht aus dem Snap Store kommt.) Das Snap läuft nur unter **Wayland** (Standard bei Ubuntu mit GNOME), es nutzt kein X11.

## macOS (13 Ventura und neuer, Apple Silicon und Intel)

**Ein Befehl im Terminal** – lädt die App, kopiert sie nach /Programme und startet sie:
```bash
curl -fsSL https://raw.githubusercontent.com/zc7ryr6ms4-eng/thisismade-CDP-1/main/install-mac.sh | bash
```

**Oder als Installationspaket:** `ThisismadeCDPlayer-1.0.0.pkg` doppelklicken (fertig kompiliert). **Oder per DMG:** `ThisismadeCDPlayer.dmg` öffnen und die App auf „Programme“ ziehen. Weil die App nicht bei Apple notarisiert ist, beim ersten Start: Systemeinstellungen → Datenschutz & Sicherheit → „Dennoch öffnen“.
