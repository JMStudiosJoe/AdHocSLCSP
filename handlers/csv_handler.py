import csv


class CSVHandler():
    def read_csv(self, path_to_csv):
        with open(path_to_csv) as csv_file:
            dict_reader = csv.DictReader(csv_file)
            return list(dict_reader)

    def read_plans_csv(self, path_to_csv, metal_level = 'Silver'):
        with open(path_to_csv) as csv_file:
            dict_reader = csv.DictReader(csv_file)
            plans = []
            for plan in dict_reader:
                if plan['metal_level'] == metal_level:
                    plans.append(plan)
            return plans

    def read_slcsp_zips(self, path_to_csv, slcsp_zips):
        with open(path_to_csv) as csv_file:
            dict_reader = csv.DictReader(csv_file)
            zips = []
            for zip_row in dict_reader:
                zipcode = zip_row['zipcode']
                if zipcode in slcsp_zips:
                    zips.append(zip_row)
            return zips


    def write_to_csv(self, path_to_csv, valid_zip_data, slcsp_zips):
        with open(path_to_csv, 'w') as slcsp_csv:
            fieldnames = slcsp_zips[0].keys()[::-1]
            writer = csv.DictWriter(slcsp_csv, fieldnames=fieldnames)
            writer.writeheader()
            for zip_data in slcsp_zips:
                zipcode = zip_data['zipcode']
                try:
                    if valid_zip_data[zipcode]:
                        data = {
                            'rate': valid_zip_data[zipcode],
                            'zipcode': zipcode
                        }
                        writer.writerow(data)

                except KeyError as e:
                    data = {
                        'rate': '',
                        'zipcode': zipcode
                    }
                    writer.writerow(data)
