import argparse
import json

parser = argparse.ArgumentParser(description='Converts geonames cities to JSON suitable for Firebase import')
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
    'fr_1793': 1,
    'abbr': 1,
    'link': 1,
    'wkdt': 1,
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
            result[id] = {
                'country': country,
                'population': population,
            };

    return result;

limit = args.limit
cities = get_cities(args)
#print(city_ids)

with open(args.altnames) as f:
    for line in f:
        if limit == 0: break

        columns = line.rstrip().split('\t')

        geonameid = columns[1]
        if not (geonameid in cities): continue

        language = columns[2]
        if language in skip_languages: continue

        columns += [''] * (altnames_column_count - len(columns))

        city = cities[geonameid]
        columns.append(city['country'])
        columns.append(city['population'])

        print('\t'.join(columns))

        if limit != None:
            limit -= 1
