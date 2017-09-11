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

        return self.build_valid_zip_with_rates(rate_area_rates)

    def build_valid_zip_with_rates(self, rate_area_rates):
        valid_min_for_zipcode = {}
        for area in rate_area_rates.keys():
            if len(rate_area_rates[area]) == 1:
                zipcode = rate_area_rates[area][0]['zipcode']
                rate = rate_area_rates[area][0]['second_lowest_rate']
                valid_min_for_zipcode[zipcode] = rate

        print(valid_min_for_zipcode)
        return valid_min_for_zipcode
