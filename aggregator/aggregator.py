class Aggregator:
    """Class to aggregate data from various APIs."""

    def __init__(self, apis):
        self.apis = apis

    def aggregate_market_data(self, market_ids):
        data = {}
        for api in self.apis:
            data[api.__class__.__name__] = api.fetch_market_data(market_ids)
        # Implement aggregation logic
        return data

    def aggregate_global_data(self):
        data = {}
        for api in self.apis:
            data[api.__class__.__name__] = api.fetch_global_data()
        # Implement aggregation logic
        return data