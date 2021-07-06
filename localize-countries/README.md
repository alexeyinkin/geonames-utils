# extract-city-altnames

Takes country names, add local names into form a JSON title.

Usage:
```
python3 localize-countries.py [-h] --tsv=FILE --localized=FILE,LANG,ALPHA2_COLUMN,TITLE_COLUMN [--localized=...]
```
optional arguments:
-  `-h`, `--help`          show this help message and exit
-  `--tsv=FILE`            Path to a geonames countryInfo.txt file.
-  `--localized=FILE,LANG,ALPHA2_COLUMN,TITLE_COLUMN` Path to a file with localizations, language code, index of ISO alpha2 column, index of title column.
-  `--skip_countries`      Comma-separated list of 2-letter country codes to skip.

Example:
```bash
python3 localize-countries.py --tsv=../countryInfo.txt --localized=localized/ru_artlebedev_3_0.tsv,ru,3,0 --localized=localized/ru_inkin_0_1.tsv,ru,0,1 --skip_countries=CS,AN > countries.tsv
```
