import csv

class CSVReader():

    def read_csv(self, path_to_csv):
        with open(path_to_csv) as csv_file:
            dict_reader = csv.DictReader(csv_file)
            return list(dict_reader)


class ZipsHandler():
    def __init__(self, all_zips):
        self.all_zips = all_zips


class PlansHandler():
    def __init__(self, all_plans):
        self.all_plans = all_plans


def find_second_min_rate_for_rate_area(rate_area_for_zip, plans):
    min_rate = plans[0]['rate']
    second_lowest_rate = min_rate
    for plan in plans:
        if plan['rate_area'] == rate_area_for_zip:
            if plan['rate'] < min_rate:
                min_rate = plan['rate']
                second_lowest_rate = min_rate
            elif plan['rate'] < second_lowest_rate:
                second_lowest_rate = plan['rate']

    return second_lowest_rate

def find_plans_for_zip(zips, plans, looking_for_zips):
    rate_area_rates = {}
    plans_for_zip = []
    for zip_row in zips:
        zipcode = zip_row['zipcode']
        rate_area = zip_row['rate_area']
        data = {
            'second_lowest_rate': find_second_min_rate_for_rate_area(zip_row['rate_area'], plans),
            'state': zip_row['state'],
            'zipcode': zipcode
        }
        try:
            if len(rate_area_rates[rate_area]) != 0:
                rate_area_rates[rate_area].append(data)
        except Exception as e:
            print('ERROR OCCURRED')
            print(e)
            rate_area_rates[rate_area] = [data]

    print(rate_area_rates)
    import pdb; pdb.set_trace()

    return rate_area_rates
# slcsp may not be found if silver plan not available in the area or if only one
# cost in the area?

if __name__ == '__main__':
    # process
    # 1. load all the zips
    # 2. go through plans and find plans for all zips
    reader = CSVReader()
    zips_list = reader.read_csv('./zips.csv')
    plans_list = reader.read_csv('./plans.csv')
    looking_for_zips = reader.read_csv('./slcsp.csv')
    silver_plans = []
    for plan in plans_list:
        if plan['metal_level'] == 'Silver':
            silver_plans.append(plan)

    find_plans_for_zip(zips_list, silver_plans, looking_for_zips)

