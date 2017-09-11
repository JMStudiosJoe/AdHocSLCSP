import csv

class CSVHandler():

    def read_csv(self, path_to_csv):
        with open(path_to_csv) as csv_file:
            dict_reader = csv.DictReader(csv_file)
            return list(dict_reader)

    def write_to_csv(self, path_to_csv, valid_zip_data, slcsp_zips):
        with open(path_to_csv, 'w') as slcsp_csv:
            writer = csv.DictWriter(slcsp_csv, slcsp_zips[0].keys())
            writer.writeheader()
            for zip_data in slcsp_zips:
                zipcode = zip_data['zipcode']
                try:
                    if valid_zip_data[zipcode]:
                        data = {
                            'zipcode': zipcode,
                            'rate': valid_zip_data[zipcode]
                        }
                        writer.writerow(data)

                except KeyError as e:
                    data = {
                        'zipcode': zipcode,
                        'rate': ''
                    }
                    writer.writerow(data)


class ZipsHandler():
    def __init__(self, all_zips, looking_for_zips):
        self.all_zips = all_zips
        self.looking_for_zips = looking_for_zips


class PlansHandler():
    def __init__(self, silver_plans):
        self.silver_plans = silver_plans

    def find_second_min_rate_for_rate_area(self, rate_area):
        min_rate = self.silver_plans[0]['rate']
        second_lowest_rate = min_rate
        for plan in self.silver_plans:
            if plan['rate_area'] == rate_area:
                if plan['rate'] < min_rate:
                    min_rate = plan['rate']
                    second_lowest_rate = min_rate
                elif plan['rate'] < second_lowest_rate:
                    second_lowest_rate = plan['rate']

        return second_lowest_rate



def build_valid_zip_with_rates(rate_area_rates):
    valid_min_for_zipcode = {}
    for area in rate_area_rates.keys():
        if len(rate_area_rates[area]) == 1:
            zipcode = rate_area_rates[area][0]['zipcode']
            rate = rate_area_rates[area][0]['second_lowest_rate']
            valid_min_for_zipcode[zipcode] = rate

    print(valid_min_for_zipcode)
    return valid_min_for_zipcode

def find_second_min_rate_for_rate_area(rate_area_for_zip, plans):
    min_rate = plans[0]['rate']
    second_lowest_rate = min_rate
    rates = []
    for plan in plans:
        if plan['rate_area'] == rate_area_for_zip:
            rates.append(plan['rate'])
            if plan['rate'] < min_rate:
                min_rate = plan['rate']
                second_lowest_rate = min_rate
            elif plan['rate'] < second_lowest_rate:
                second_lowest_rate = plan['rate']
    print('----------\n')
    print(rates)
    print('MIN RATE = ', min_rate)
    print('SECOND RATE = ', second_lowest_rate)
    print('\n\n----------\n')
    return second_lowest_rate

def find_plans_for_zip(zips, plans, looking_for_zips):
    rate_area_rates = {}
    for zip_row in zips:
        zipcode = zip_row['zipcode']
        if zipcode in looking_for_zips:
            rate_area = zip_row['rate_area']
            data = {
                'second_lowest_rate': find_second_min_rate_for_rate_area(rate_area, plans),
                'zipcode': zipcode
            }
            try:
                if len(rate_area_rates[rate_area]) != 0:
                    rate_area_rates[rate_area].append(data)
            except Exception as e:
                rate_area_rates[rate_area] = [data]

    return build_valid_zip_with_rates(rate_area_rates)


if __name__ == '__main__':
    csv_handler = CSVHandler()
    zips_list = csv_handler.read_csv('./zips.csv')
    plans_list = csv_handler.read_csv('./plans.csv')
    slcsp_zips = csv_handler.read_csv('./slcsp.csv')
    looking_for_zips = [find_zip['zipcode'] for find_zip in slcsp_zips]
    silver_plans = []
    for plan in plans_list:
        if plan['metal_level'] == 'Silver':
            silver_plans.append(plan)

    valid_zip_data = find_plans_for_zip(zips_list, silver_plans, looking_for_zips)
    csv_handler.write_to_csv('./slcsp_found.csv', valid_zip_data, slcsp_zips)

