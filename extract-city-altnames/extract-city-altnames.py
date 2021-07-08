import argparse
import json

class AltName:
    def __init__(
        self,
        *,
        name_id: int,
        city_id: int,
        language: str,
        name: str,
        is_preferred: bool
    ) -> None:
        self.name_id = name_id
        self.city_id = city_id
        self.language = language
        self.name = name
        self.is_preferred = is_preferred

class LanguageAltNames:
    def __init__(self) -> None:
        self.found_preferred = False
        self.altnames = []

    def add_name(self, altname: AltName) -> None:
        if not altname.is_preferred and self.found_preferred:
            return

        if altname.is_preferred and not self.found_preferred:
            self.found_preferred = True
            self.altnames = []

        self.altnames.append(altname)

class CityAltNames:
    def __init__(self) -> None:
        self.altnames_by_language = {}

    def add_name(self, altname: AltName) -> None:
        if not altname.language in self.altnames_by_language:
            self.altnames_by_language[altname.language] = LanguageAltNames()

        self.altnames_by_language[altname.language].add_name(altname)

class City:
    def __init__(self, *, country_code: str, population: int) -> None:
        self.country_code = country_code
        self.population = population
        self.names = CityAltNames()

parser = argparse.ArgumentParser(description='Extracts only cities from alternate names, adds country and population.')
parser.add_argument('--cities', metavar='FILE', type=str, help='Path to the cities TSV file.')
parser.add_argument('--altnames', metavar='FILE', type=str, help='Path to the alternate names TSV file.')
parser.add_argument('--countries', metavar='COUNTRIES', type=str, help='Comma-separated list of 2-letter country codes. Default: all countries.')
parser.add_argument('--skip_cities', metavar='CITIES', type=str, help='Comma-separated list of city names to skip.', default='')
parser.add_argument('--limit', metavar='N', type=int, help='Only use first N matching altnames.')

args = parser.parse_args()

skip_languages = {
    'post': 1,
    'iata': 1,
    'icao': 1,
    'faac': 1,
    'tcid': 1,
    'fr_1793': 1,
    'abbr': 1,
    'link': 1,
    'wkdt': 1,
    'uncl': 1,
    'unlc': 1,
    'phon': 1,
    'piny': 1,
}

altnames_column_count = 10

def get_cities(args):
    result = {}

    countries = []
    all_countries = (args.countries == None)
    if not all_countries:
        countries = args.countries.split(',')

    skip_cities_with_empty = args.skip_cities.split(',')
    skip_cities = [c for c in skip_cities_with_empty if c]

    with open(args.cities) as f:
        for line in f:
            columns = line.rstrip().split('\t')

            country = columns[8]
            if not all_countries:
                if not country in countries: continue

            id = columns[0]
            population = columns[14]
            result[id] = City(
                country_code=country,
                population=int(columns[14]),
            );

    return result;

limit = args.limit
cities = get_cities(args)

with open(args.altnames) as f:
    for line in f:
        if limit == 0: break

        columns = line.rstrip().split('\t')

        geonameid = columns[1]
        if not (geonameid in cities): continue

        language = columns[2]
        if language in skip_languages: continue

        columns += [''] * (altnames_column_count - len(columns))

        is_colloquial = columns[6]
        if is_colloquial == '1': continue

        is_historic = columns[7]
        if is_historic == '1': continue

        altname = AltName(
            name_id=int(columns[0]),
            city_id=int(columns[1]),
            language=columns[2],
            name=columns[3],
            is_preferred=columns[4],
        )

        city = cities[geonameid]
        city.names.add_name(altname)

        if limit != None:
            limit -= 1

for city_id in cities:
    city = cities[city_id]

    for language in city.names.altnames_by_language:
        altnames = city.names.altnames_by_language[language]

        for altname in altnames.altnames:
            columns = [
                altname.name_id,
                altname.city_id,
                language,
                altname.name,
                city.country_code,
                city.population,
            ]
            print('\t'.join(str(c) for c in columns))
