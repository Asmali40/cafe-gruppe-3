# cafe-gruppe-3

Ein FastAPI-basiertes Projekt mit REST- und GraphQL-Schnittstellen, PostgreSQL-Datenbank und Keycloak-Authentifizierung.

## Projektmitglieder

| Nachname | Vorname | Kürzel | E-Mail |
|----------|---------|--------|--------|
| Abdi Tube | Abubakar | abab1016 | abab1016@h-ka.de |
| Yueksel | Cevdet Efe | yuce1011 | yuce1011@h-ka.de |

## Git Befehle

### Repository klonen
```bash
git clone https://github.com/Asmali40/cafe-gruppe-3.git
cd cafe-gruppe-3
```

### Branch wechseln
```bash
git checkout main          # Zum Hauptbranch wechseln
git checkout implementierung  # Zum Implementierungsbranch wechseln
```

### Änderungen anzeigen
```bash
git status                # Status der Arbeitskopie anzeigen
git diff                  # Änderungen anzeigen
git diff --staged         # Gestage Änderungen anzeigen
```

### Änderungen committen
```bash
git add .                 # Alle Änderungen zur Staging-Area hinzufügen
git add <datei>           # Bestimmte Datei hinzufügen
git commit -m "Nachricht" # Änderungen commiten
```

### Änderungen hochladen (pushen)
```bash
git push                  # Commits auf Remote hochladen
git push origin main      # Auf Hauptbranch pushen
git push -u origin branch # Branch erstellen und pushen
```

### Änderungen herunterladen (pullen)
```bash
git pull                 # Änderungen vom Remote herunterladen
git pull origin main     # Vom Hauptbranch pullen
```

### Branch verwalten
```bash
git branch               # Alle Branches anzeigen
git branch -a            # Alle Branches (lokal + remote) anzeigen
git branch -d <branch>   # Branch löschen (lokaler)
git checkout -b <branch> # Neuen Branch erstellen und wechseln
```

### Log und History
```bash
git log                  # Commit-History anzeigen
git log --oneline        # Kurzformat anzeigen
git log -n <anzahl>      # Letzte n Commits anzeigen
```

### Reset und Restore
```bash
git reset --soft HEAD~1  # Letzten Commit rückgängig machen (Änderungen bleiben)
git reset --hard HEAD~1  # Letzten Commit rückgängig machen (Änderungen weg)
git checkout -- <datei> # Änderungen an Datei verwerfen
```

## Einrichtung

### Voraussetzungen
- Python 3.14+
- uv (Package Manager)

### Installation der Abhängigkeiten
```bash
uv sync --all-groups
```

### Virtuelle Umgebung aktivieren
```bash
# Windows PowerShell
.venv\Scripts\activate.ps1

# Linux/Mac
source .venv/bin/activate
```

## Projekt starten

### Option 1: Mit uv run
```bash
uv run cafe
```

### Option 2: Mit Python direkt
```bash
uv run python -m cafe
```

### Option 3: Mit FastAPI Dev-Server
```bash
uv run fastapi dev src/cafe
```

### Option 4: Mit Uvicorn (mit TLS)
```bash
uv run uvicorn src.cafe:app --ssl-certfile=src\cafe\config\resources\tls\certificate.crt --ssl-keyfile=src\cafe\config\resources\tls\key.pem
```

## Tests ausführen

### Alle Tests ausführen
```bash
uv run pytest
```

### Nur REST-Tests ausführen
```bash
uv run pytest -m rest
```

### Bestimmte Tests ausführen
```bash
uv run pytest -k test_post_invalid_json
```

### HTML-Testreport erstellen
```bash
uv run pytest --html=report.html
```

## Code-Qualität

### Linting mit Ruff
```bash
uvx ruff check src tests
uvx ruff check --fix src tests  # Automatisch fixen
```

### Code formatieren
```bash
uvx ruff format src tests
uvx ruff format --check src tests  # Nur prüfen, nicht formatieren
```

### Typprüfung mit Ty
```bash
uvx ty check src tests
```

## Abhängigkeiten verwalten

### Veraltete Pakete anzeigen
```bash
uv tree --outdated --all-groups --depth=1
```

### Alle veralteten Pakete anzeigen
```bash
uv tree --outdated --all-groups
```

### Paket-Abhängigkeiten invertiert anzeigen
```bash
uv tree --invert --package pydantic
```

### Python-Versionen anzeigen
```bash
uv python list
```

### Veraltete Pakete im Projekt anzeigen
```bash
uv pip list --outdated
```

## Sicherheit

### Sicherheitsprüfung mit pip-audit
```bash
# Zuerst requirements.txt erstellen
uv pip compile pyproject.toml > requirements.txt
# Dann prüfen
uvx pip-audit -r requirements.txt
```

### Sentry für Fehlerverfolgung
```bash
uvx pysentry-rs
```

## Dokumentation

### MkDocs Server starten
```bash
uv run mkdocs serve
```

## Build und Veröffentlichung

### Projekt bauen
```bash
uv build
```

### Projekt veröffentlichen
```bash
uv publish --token <UV_PUBLISH_TOKEN>
```

## Export und Import

### Exportieren zu pylock.toml
```bash
uv export -o pylock.toml
```

### Installieren mit pylock.toml
```bash
uv pip install mit pylock.toml
```

## Load Testing

### Locust starten
```bash
uvx locust -f .\extras\locustfile.py
```

## Projektstruktur

```
cafe-gruppe-3/
├── src/cafe/                 # Hauptquellcode
│   ├── config/              # Konfiguration
│   ├── entity/              # Datenbank-Entities
│   ├── graphql_api/         # GraphQL-Schnittstelle
│   ├── repository/          # Datenbank-Zugriff
│   ├── router/              # REST-Routen
│   ├── security/            # Sicherheit & Auth
│   ├── service/             # Geschäftslogik
│   └── static/              # Statische Dateien
├── tests/                    # Tests
│   ├── integration/         # Integrationstests
│   └── unit/               # Unit-Tests
├── Dockerfile               # Docker-Container
├── pyproject.toml           # Projekt-Konfiguration
└── README.md               # Diese Datei
```

## Technologien

- **FastAPI**: Web-Framework
- **PostgreSQL**: Datenbank
- **SQLAlchemy**: OR-Mapping
- **Keycloak**: Authentifizierung
- **GraphQL**: Alternative API-Schnittstelle
- **Pytest**: Testing-Framework
- **Ruff**: Linting und Formatierung
- **Ty**: Typprüfung
- **uv**: Package Manager

## Lizenz

GPL-3.0-or-later