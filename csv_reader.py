import csv

class CSVReader():

    def read_csv(self, path_to_csv):
        with open(path_to_csv) as csv_file:
            dict_reader = csv.DictReader(csv_file)
            return list(dict_reader)

# slcsp may not be found if silver plan not available in the area or if only one
# cost in the area?

if __name__ == '__main__':
    # process
    # 1. load all the zips
    # 2. go through plans and find plans for all zips
    reader = CSVReader()
    zips_csv = reader.read_csv('./zips.csv')
    import pdb;pdb.set_trace()
    plans_csv = reader.read_csv('./plans.csv')
    slcsp_csv = reader.read_csv('./slcsp.csv')

