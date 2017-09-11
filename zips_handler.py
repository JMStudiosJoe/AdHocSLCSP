class ZipsHandler():
    def __init__(self, all_zips, slcsp_zips):
        self.all_zips = all_zips
        self.looking_for_zips = []
        for zip_row in all_zips:
            zipcode = zip_row['zipcode']
            if zipcode in slcsp_zips:
                self.looking_for_zips.append(zip_row)
