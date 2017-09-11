from csv_handler import CSVHandler
from plans_handler import PlansHandler
from slcsp_handler import SLCSPHandler
from zips_handler import ZipsHandler


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
    second_lowest_rate = str(float(min_rate) + 200)
    rates = []
    for plan in plans:
        if plan['rate_area'] == rate_area_for_zip:
            rates.append(plan['rate'])
            if plan['rate'] < min_rate:
                min_rate = plan['rate']
            elif plan['rate'] < second_lowest_rate and plan['rate'] > min_rate:
                second_lowest_rate = plan['rate']
    print('----------\n')
    print(sorted(rates))
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

