class PlansHandler():
    def __init__(self, plans_list, metal_level='Silver'):
        self.plans = []
        for plan in plans_list:
            if plan['metal_level'] == metal_level:
                self.plans.append(plan)

    def find_second_min_rate_for_rate_area(self, rate_area):
        min_rate = self.plans[0]['rate']
        second_lowest_rate = min_rate
        for plan in self.plans:
            if plan['rate_area'] == rate_area:
                if plan['rate'] < min_rate:
                    min_rate = plan['rate']
                elif plan['rate'] < second_lowest_rate and plan['rate'] > min_rate:
                    second_lowest_rate = plan['rate']

        return second_lowest_rate
