
import requests
import yaml
import pandas as pd
import re

# Download and parse all case study YAML files
base_url = "https://raw.githubusercontent.com/mitre-atlas/atlas-data/refs/heads/main/data/case-studies/"
def get_all_case_study_filenames():
    api_url = "https://api.github.com/repos/mitre-atlas/atlas-data/contents/data/case-studies"
    response = requests.get(api_url)
    response.raise_for_status()
    return [item["name"] for item in response.json() if item["name"].startswith("AML.CS") and item["name"].endswith(".yaml")]

case_ids = get_all_case_study_filenames()
records = []

## GitHub API rate-limits unauthenticated requests are limited to 60 per hour. You can raise this to 5,000/hour by adding a token
## headers = {"Authorization": "token YOUR_PERSONAL_ACCESS_TOKEN"}
## response = requests.get(api_url, headers=headers)

for case_file in case_ids:
    url = base_url + case_file
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = yaml.safe_load(response.text)

        case_id = data.get("id", "")
        name = data.get("name", "")
        obj_type = data.get("object-type", "")
        incident_date = data.get("incident-date", "")
        target = data.get("target", "")
        actor = data.get("actor", "")

        procedures = data.get("procedure", [])
        if not isinstance(procedures, list):
            procedures = [procedures]

        for proc in procedures:
            tactic = proc.get("tactic", "")
            technique = proc.get("technique", "")
            records.append({
                "id": case_id,
                "name": name,
                "object-type": obj_type,
                "incident-date": incident_date,
                "procedure.tactic": tactic,
                "procedure.technique": technique,
                "target": target,
                "actor": actor
            })

    except Exception as e:
        print(f"Failed to fetch or parse {case_file}: {e}")

df = pd.DataFrame(records)
df.to_csv("mitre_atlas_case_studies.csv", index=False)
print("CSV saved as mitre_atlas_case_studies.csv")

# Function to build lookup using YAML anchors
def build_anchor_lookup(yaml_url):
    raw_text = requests.get(yaml_url).text
    anchors = re.findall(r"- +&([\w_]+)[\s\S]+?id: ([^\n]+)\n +name: ([^\n]+)", raw_text)
    return {f"{{{{{anchor}.id}}}}": name for anchor, _id, name in anchors}

# Create lookup dictionaries from anchor references
tactic_lookup = build_anchor_lookup("https://raw.githubusercontent.com/mitre-atlas/atlas-data/refs/heads/main/data/tactics.yaml")
technique_lookup = build_anchor_lookup("https://raw.githubusercontent.com/mitre-atlas/atlas-data/refs/heads/main/data/techniques.yaml")

# Load mitigations separately and map by technique ID
mitigations_raw = yaml.safe_load(requests.get("https://raw.githubusercontent.com/mitre-atlas/atlas-data/refs/heads/main/data/mitigations.yaml").text)
mitigation_lookup = {}
for m in mitigations_raw:
    if 'techniques' in m:
        for tech in m['techniques']:
            mitigation_lookup[tech['id']] = m['name']

# Reload the raw data
df = pd.read_csv("mitre_atlas_case_studies.csv")

# Replace placeholders with names
df['procedure.tactic'] = df['procedure.tactic'].map(tactic_lookup).fillna(df['procedure.tactic'])
df['procedure.technique'] = df['procedure.technique'].map(technique_lookup).fillna(df['procedure.technique'])

# Add mitigation column
df['mitigation'] = df['procedure.technique'].map(lambda t: mitigation_lookup.get(t, ''))

# Save enriched version
df.to_csv("mitre_atlas_case_studies_enriched.csv", index=False)
print("Saved: mitre_atlas_case_studies_enriched.csv")
