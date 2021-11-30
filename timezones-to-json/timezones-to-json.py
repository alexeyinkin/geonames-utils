import argparse
import json

parser = argparse.ArgumentParser(description='Converts the geonames timezone dictionary to JSON suitable for Firebase import')
parser.add_argument('--tsv', metavar='FILE', type=str, help='Path to a geonames timeZones.txt TSV file.')
parser.add_argument('--limit', metavar='N', type=int, help='Only use first N non-header lines.')

args = parser.parse_args()

limit = args.limit
dict = {}
skip_lines = 1

with open(args.tsv) as f:
    for line in f:
        if skip_lines > 0:
            skip_lines -= 1
            continue

        if limit == 0: break

        columns = line.rstrip().split('\t')

        country_alpha2 = columns[0]
        timezone = columns[1]
        gmt_offset_winter = float(columns[2])
        gmt_offset_summer = float(columns[3])

        dict[timezone] = {
            'countryAlpha2': country_alpha2,
            'gmtOffsetWinter': gmt_offset_winter,
            'gmtOffsetSummer': gmt_offset_summer,
        }

        if limit != None:
            limit -= 1

print(json.dumps(dict))
