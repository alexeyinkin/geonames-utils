# extract-city-altnames

Extracts only cities from alternate names, adds country and population.

Usage:
```
python3 extract-city-altnames.py [-h] --cities=FILE --altnames=FILE [--countries COUNTRIES] [--limit N]
```
optional arguments:
-  `-h`, `--help`            show this help message and exit
-  `--cities=FILE`         Path to a geonames TSV export file.
-  `--altnames=FILE`       Path to a alternate names TSV export file.
-  `--countries COUNTRIES` Comma-separated list of 2-letter country codes. Default: all countries.
-  `--limit N`             Only use first N matching cities.

Examples:
```bash
python3 extract-city-altnames.py --cities=../cities500.txt --altnames=../alternateNamesV2.txt > altnames.tsv
```

This script also adds 2 columns:
1. 2-letter country code.
2. City population.

This is intended for a table with type suggestions. If selects United States as a country and types 'Moscow' as a city, then Russia's Moscow can be filtered out without joining cities table. And if the city name is not unique in the country, then sotring by population DESC can help filtering out the unlikely cities.
