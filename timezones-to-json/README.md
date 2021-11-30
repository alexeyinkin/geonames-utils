# geonames-to-json

This script converts timezone info from GeoNames' timeZones.txt TSV to JSON.

Usage:
```
python3 timezones-to-json.py [-h] [--tsv FILE] [--limit N]
```

Arguments:
-  `--tsv FILE`            Path to timeZones.txt TSV file.
-  `--limit N`             Only use first N non-header lines.

Example:
```bash
python3 timezones-to-json.py --tsv timeZones.txt --limit 3 > timezonesGeoNames.json
```

Output:
```json
{"Africa/Abidjan": {"countryAlpha2": "CI", "gmtOffsetWinter": 0.0, "gmtOffsetSummer": 0.0}, "Africa/Accra": {"countryAlpha2": "GH", "gmtOffsetWinter": 0.0, "gmtOffsetSummer": 0.0}, "Africa/Addis_Ababa": {"countryAlpha2": "ET", "gmtOffsetWinter": 3.0, "gmtOffsetSummer": 3.0}}
```

The output is mapped by timezone string IDs and contains:
- `countryAlpha2` for 2-letter country code.
- `gmtOffsetWinter`
- `gmtOffsetSummer`

## TODO
- Allow to pick and rename fields.

## Firebase Import
In case you want to import this JSON to Firebase, use this:

```bash
npm install -g node-firestore-import-export
firestore-import --accountCredentials credentials.json --backupFile timezoneGeoNames.json --nodePath timezoneGeoNames
```

where `credentials.json` is a file you export from Firebase console as per this tutorial: https://www.youtube.com/watch?v=gPzs6t3tQak
