import argparse
import json

parser = argparse.ArgumentParser(description='Converts geonames cities to JSON suitable for Firebase import')
parser.add_argument('--tsv', metavar='FILE', type=str, help='Path to a geonames TSV export file.')
parser.add_argument('--countries', metavar='COUNTRIES', type=str, help='Comma-separated list of 2-letter country codes. Default: all countries.')
parser.add_argument('--skip_cities', metavar='CITIES', type=str, help='Comma-separated list of city names to skip.', default='')
parser.add_argument('--limit', metavar='N', type=int, help='Only use first N matching cities.')

args = parser.parse_args()

countries = []
all_countries = (args.countries == None)
if not all_countries:
    countries = args.countries.split(',')

skip_cities_with_empty = args.skip_cities.split(',')
skip_cities = [c for c in skip_cities_with_empty if c]

limit = args.limit
dict = {}

with open(args.tsv) as f:
    for line in f:
        if limit == 0: break

        columns = line.rstrip().split('\t')

        if not all_countries:
            country = columns[8]
            if not country in countries: continue

        id = columns[0]
        title = columns[1]
        population = int(columns[14])

        if title in skip_cities: continue

        dict[id] = {
            'title': title,
            'score': population,
        }

        if limit != None:
            limit -= 1

print(json.dumps(dict))
