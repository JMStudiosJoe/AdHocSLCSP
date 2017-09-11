class PlansHandler():
    def __init__(self, plans_list):
        self.plans = plans_list

    def find_second_min_rate(self, rate_area):
        min_rate = self.plans[0]['rate']
        offset_price = 300
        second_lowest_rate = str(float(min_rate) + offset_price)
        for plan in self.plans:
            if plan['rate_area'] == rate_area:
                if plan['rate'] < min_rate:
                    min_rate = plan['rate']
                elif plan['rate'] < second_lowest_rate and plan['rate'] > min_rate:
                    second_lowest_rate = plan['rate']

        return second_lowest_rate
