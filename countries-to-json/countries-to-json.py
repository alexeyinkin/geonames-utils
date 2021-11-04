import argparse
import json

parser = argparse.ArgumentParser(description='Converts geonames countries to JSON suitable for Firebase import')
parser.add_argument('--tsv', metavar='FILE', type=str, help='Path to a geonames countryInfo.txt file.')

args = parser.parse_args()

countries_dict = {}

with open(args.tsv) as f:
    for line in f:
        if line[0] == '#': continue

        columns = line.rstrip().split('\t')

        alpha2 = columns[0]
        numeric = int(columns[2])
        title = columns[4]

        countries_dict[alpha2] = {
            'numeric': numeric,
            'title': title,
        }

print(json.dumps(countries_dict))
