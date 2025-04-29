import requests
from test.models import Vulnerability

url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
response = requests.get(url)
data = response.json()

print('Start')

i = 0
for vuln in data["vulnerabilities"]:
    cve = vuln["cve"]
    Vulnerability.objects.update_or_create(
        cve_id=cve["id"],
        defaults={
            "published_date": cve["published"],
            "last_modified_date": cve["lastModified"],
            "severity": cve["metrics"]["cvssMetricV2"][0]["baseSeverity"],
        }
    )
    i += 1
    if i == 20:
        break

print('End')
