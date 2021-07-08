# extract-city-altnames

Extracts only cities from alternate names, adds country and population.

Usage:
```
python3 extract-city-altnames.py --cities=FILE --altnames=FILE [--countries COUNTRIES] [--limit N]
```
optional arguments:
-  `--cities=FILE`         Path to a geonames TSV export file.
-  `--altnames=FILE`       Path to a alternate names TSV export file.
-  `--countries COUNTRIES` Comma-separated list of 2-letter country codes. Default: all countries.
-  `--limit N`             Only use first N matching cities.

Examples:
```bash
python3 extract-city-altnames.py --cities=../cities500.txt --altnames=../alternateNamesV2.txt > altnames.tsv
```

For each city and each language if a preferred name exists, then only this preferred name is kept (or multiple preferred names for this city-and-language if it happens to be).

Otherwise all the names for this city and language are kept.

The script keeps the 4 first original columns:
1. alternateNameId   : the id of this alternate name, int
1. geonameid         : geonameId referring to id in table 'geoname', int
1. isolanguage       : iso 639 language code 2- or 3-characters, varchar(7)
1. alternate name    : alternate name or name variant, varchar(400)

Then it adds 2 columns from city:
5. country code      : ISO-3166 2-letter country code, 2 characters
5. population        : bigint (8 byte int) 

This is intended for a table with type suggestions. If the user selects United States as a country and types 'Moscow' as a city, then Russia's Moscow can be filtered out without joining cities table. And if the city name is not unique in the country, then sotring by population DESC can highlight the likely cities.
