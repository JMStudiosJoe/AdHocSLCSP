from handlers.csv_handler import CSVHandler
from handlers.plans_handler import PlansHandler
from handlers.slcsp_handler import SLCSPHandler
from handlers.zips_handler import ZipsHandler


if __name__ == '__main__':
    csv_handler = CSVHandler()
    slcsp_zips = csv_handler.read_csv('./slcsp.csv')
    slcsp_zips_list = [find_zip['zipcode'] for find_zip in slcsp_zips]
    zips_list = csv_handler.read_slcsp_zips('./zips.csv', slcsp_zips_list)
    plans_list = csv_handler.read_plans_csv('./plans.csv')

    zips_handler = ZipsHandler(zips_list)
    plans_handler = PlansHandler(plans_list)
    slcsp_handler = SLCSPHandler(plans_handler, zips_handler)

    valid_zip_data = slcsp_handler.find_valid_slcsp_zips()
    csv_handler.write_to_csv('./slcsp.csv', valid_zip_data, slcsp_zips)
