import argparse
import json

parser = argparse.ArgumentParser(description='Takes country names, add local names into form a JSON title')
parser.add_argument('--tsv', metavar='FILE', type=str, help='Path to a geonames countryInfo.txt file.')
parser.add_argument('--localized', metavar='FILE', type=str, nargs='+', help='Path to a geonames countryInfo.txt file.', default=[])
parser.add_argument('--countries', metavar='COUNTRIES', type=str, help='Comma-separated list of 2-letter country codes. Default: all countries.')
parser.add_argument('--limit', metavar='N', type=int, help='Only use first N matching countries.')

args = parser.parse_args()

def get_english(args):
    countries = []
    all_countries = (args.countries == None)
    if not all_countries:
        countries = args.countries.split(',')

    limit = args.limit
    countries_dict = {}

    with open(args.tsv) as f:
        for line in f:
            if limit == 0: break

            if line[0] == '#': continue

            columns = line.rstrip().split('\t')

            country_code = columns[0]
            country_id = columns[2]
            title = columns[4]

            if not all_countries:
                if not country_code in countries: continue

            countries_dict[country_code] = {
                'id': country_id,
                'title_m': {'en': title},
            }

            if limit != None:
                limit -= 1

    return countries_dict

def add_localized(countries_dict, filename, lang, code_column, title_column):
    with open(filename) as f:
        for line in f:
            columns = line.rstrip().split('\t')
            code = columns[code_column]
            title = columns[title_column]

            if not code in countries_dict: continue

            countries_dict[code]['title_m'][lang] = title


countries_dict = get_english(args)

for localized in args.localized:
    parts = localized.split(',')

    filename        = parts[0]
    lang            = parts[1]
    code_column     = int(parts[2])
    title_column    = int(parts[3])

    add_localized(countries_dict, filename, lang, code_column, title_column)

for country_code in countries_dict:
    country_dict = countries_dict[country_code]
    columns = [
        country_dict['id'],
        country_code,
        "'" + json.dumps(country_dict['title_m'], ensure_ascii=False) + "'",
        # This would be better, but PhpStorm cannot import strings with quotations escaped with \"
        #json.dumps(json.dumps(country_dict['title_m'], ensure_ascii=False), ensure_ascii=False),
    ]
    print('\t'.join(columns))
