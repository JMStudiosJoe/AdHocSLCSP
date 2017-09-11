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
    def __init__(self, all_zips, slcsp_zips):
        self.all_zips = all_zips
        self.looking_for_zips = []
        for zip_row in all_zips:
            zipcode = zip_row['zipcode']
            if zipcode in slcsp_zips:
                self.looking_for_zips.append(zip_row)


class PlansHandler():
    def __init__(self, plans_list, metal_level='Silver'):
        self.plans = []
        for plan in plans_list:
            if plan['metal_level'] == metal_level:
                self.plans.append(plan)

    def find_second_min_rate_for_rate_area(self, rate_area):
        min_rate = self.plans[0]['rate']
        second_lowest_rate = min_rate
        for plan in self.plans:
            if plan['rate_area'] == rate_area:
                if plan['rate'] < min_rate:
                    min_rate = plan['rate']
                    second_lowest_rate = min_rate
                elif plan['rate'] < second_lowest_rate:
                    second_lowest_rate = plan['rate']

        return second_lowest_rate


class SLCSPHandler():

    def __init__(self, plans_handler, zips_handler):
        '''
        load the zips for slcps, the class for handling plans with already loaded silver plans
        zips_handler not used yet will see it soon
        '''
        self.plans_handler = plans_handler
        self.zips_handler = zips_handler

    def find_valid_slcsp_zips(self):
        rate_area_rates = {}
        for zip_row in self.zips_handler.looking_for_zips:
            zipcode = zip_row['zipcode']
            rate_area = zip_row['rate_area']
            data = {
                'second_lowest_rate': self.plans_handler.find_second_min_rate_for_rate_area(rate_area),
                'zipcode': zipcode
            }
            try:
                if len(rate_area_rates[rate_area]) != 0:
                    rate_area_rates[rate_area].append(data)
            except Exception as e:
                rate_area_rates[rate_area] = [data]

        return build_valid_zip_with_rates(rate_area_rates)

    def build_valid_zip_with_rates(rate_area_rates):
        valid_min_for_zipcode = {}
        for area in rate_area_rates.keys():
            if len(rate_area_rates[area]) == 1:
                zipcode = rate_area_rates[area][0]['zipcode']
                rate = rate_area_rates[area][0]['second_lowest_rate']
                valid_min_for_zipcode[zipcode] = rate

        print(valid_min_for_zipcode)
        return valid_min_for_zipcode





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

def find_valid_slcsp_zips(zips, plans, slcsp_zips_list):
    rate_area_rates = {}
    for zip_row in zips:
        zipcode = zip_row['zipcode']
        if zipcode in slcsp_zips_list:
            rate_area = zip_row['rate_area']
            data = {
                'second_lowest_rate': find_second_min_rate_for_rate_area(rate_area, plans),
                'zipcode': zipcode
            }
            try:
                if len(rate_area_rates[rate_area]) != 0:
                    rate_area_rates[rate_area].append(data)
            except KeyError as e:
                rate_area_rates[rate_area] = [data]

    return build_valid_zip_with_rates(rate_area_rates)


if __name__ == '__main__':
    csv_handler = CSVHandler()
    zips_list = csv_handler.read_csv('./zips.csv')
    plans_list = csv_handler.read_csv('./plans.csv')
    slcsp_zips = csv_handler.read_csv('./slcsp.csv')
    slcsp_zips_list = [find_zip['zipcode'] for find_zip in slcsp_zips]

    zips_handler = ZipsHandler(zips_list, slcsp_zips_list)
    plans_handler = PlansHandler(plans_list)
    slcsp_handler = SLCSPHandler(plans_handler, zips_handler)
    valid_zip_data_class = slcsp_handler.find_valid_slcsp_zips()

    silver_plans = []
    for plan in plans_list:
        if plan['metal_level'] == 'Silver':
            silver_plans.append(plan)

    valid_zip_data = find_valid_slcsp_zips(zips_list, silver_plans, slcsp_zips_list)
    import pdb; pdb.set_trace()
    csv_handler.write_to_csv('./slcsp_found.csv', valid_zip_data, slcsp_zips)

