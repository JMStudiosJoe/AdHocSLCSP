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


def find_plans_for_rate_area(zip_row, plans):
    rate_area_for_zip = zip_row['rate_area']
    plans = []
    for plan in plans:
        if plan['rate_area'] == rate_area_for_zip:
            plans.append(plan)

    return plans

def find_plans_for_zip(zips, plans):
    rate_area_plans = []
    for zip_row in zips:
        find_plans_for_rate_area(zip_row['rate_area'], plans)

        plans_for_zip.append(data)


# slcsp may not be found if silver plan not available in the area or if only one
# cost in the area?

if __name__ == '__main__':
    # process
    # 1. load all the zips
    # 2. go through plans and find plans for all zips
    reader = CSVReader()
    zips_list = reader.read_csv('./zips.csv')
    plans_list = reader.read_csv('./plans.csv')
    silver_plans = []
    for plan in plans_list:
        if plan['metal_level'] == 'Silver':
            silver_plans.append(plan)

    find_plans_for_zip(zips_list, silver_plans)

