# countries-to-json

Converts geonames countries to JSON suitable for Firebase import.

Usage:
```
python3 countries-to-json.py [-h] --tsv=FILE > countries.json
```
Arguments:
-  `--tsv=FILE`            Path to a geonames countryInfo.txt file.

Output objects are mapped by alpha2 code and contain fields:
- numeric
- title
