import csv

class CSVReader():

    def __init__(self, path_to_csv):
        with open(path_to_csv) as csv_file:
            print(csv_file)


if __name__ == '__main__':
    slcsp_csv = CSVReader('./slcsp.csv')
    plans_csv = CSVReader('./plans.csv')
    zips_csv = CSVReader('./zips.csv')

