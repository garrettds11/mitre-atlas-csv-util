# MITRE ATLAS CSV Util

A lightweight companion utility for exporting and enriching case study data from [MITRE ATLAS](https://atlas.mitre.org/).

## Features

- ✅ Dynamically counts and parses all raw YAML case studies in MITRE ATLAS repository
- ✅ Extracts key metadata (ID, tactic, technique, target, actor)
- ✅ Resolves YAML placeholders (e.g., `{{reconnaissance.id}}`)
- ✅ Adds matching mitigation strategies (if available)
- ✅ Outputs a clean CSV file for downstream analysis
- ✅ Includes both `.py` and `.exe` versions for easy use

## Usage

#### Note:
GitHub API rate-limits unauthenticated requests are limited to 60 per hour. You can raise this to 5,000/hour by adding a token.
Uncomment these lines in ```mitre_atlas_case_study_crawler.py```

```headers = {"Authorization": "token ```<YOUR_PERSONAL_ACCESS_TOKEN>```"}```
```response = requests.get(api_url, headers=headers)```


### Option 1: Run Pre-compiled EXE

Open dist\\`mitre_atlas_case_study_crawler.exe`
(Requires internet access to fetch latest MITRE data)

### Option 2: Convert to .exe on Windows:

In terminal, do:

1) Install PyInstaller:
```pip install pyinstaller```

2) Navigate to the folder with ```mitre_atlas_case_study_crawler.py```:
```cd mitre-atlas-csv-util```

3) Build the executable:
```pyinstaller --onefile mitre_atlas_case_study_crawler.py```

Your .exe will appear in the dist folder.

## Output

- `mitre_atlas_case_studies.csv` – extractions from raw YAML case studies
- `mitre_atlas_case_studies_enriched.csv` – enriched tactics, techniques & mitigations fields

## License

MIT License (same as MITRE ATLAS)

---

Maintained as an independent companion tool. Not affiliated with MITRE.
