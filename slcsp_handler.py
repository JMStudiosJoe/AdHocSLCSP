class SLCSPHandler():
    def __init__(self, plans_handler, zips_handler):
        self.plans_handler = plans_handler
        self.zips_handler = zips_handler
        self.rate_area_rates = {}

    def find_valid_slcsp_zips(self):
        for zip_row in self.zips_handler.looking_for_zips:
            self.add_to_rate_area_rates(zip_row)

        return self.build_valid_zip_with_rates()

    def add_to_rate_area_rates(self, zip_row):
        zipcode = zip_row['zipcode']
        rate_area = zip_row['rate_area']
        rate = self.plans_handler.find_second_min_rate(rate_area)
        data = {
            'second_lowest_rate': rate,
            'zipcode': zipcode
        }
        try:
            if len(self.rate_area_rates[rate_area]) != 0:
                self.rate_area_rates[rate_area].append(data)
        except KeyError as e:
            self.rate_area_rates[rate_area] = [data]

    def build_valid_zip_with_rates(self):
        valid_min_for_zipcode = {}
        for area in self.rate_area_rates.keys():
            if len(self.rate_area_rates[area]) == 1:
                zipcode = self.rate_area_rates[area][0]['zipcode']
                rate = self.rate_area_rates[area][0]['second_lowest_rate']
                valid_min_for_zipcode[zipcode] = rate

        return valid_min_for_zipcode
