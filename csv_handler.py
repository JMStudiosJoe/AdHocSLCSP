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
