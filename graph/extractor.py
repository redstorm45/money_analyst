import datetime

from graph.element import GraphLayer, GraphNode, GraphLink

DATE_FORMAT_PY = '%Y-%m-%d'


class Extractor:
    def __init__(self, models):
        self.model_cat = models["categories"]
        self.model_tr = models["transactions"]
        self.model_lab = models["labels"]
        self.layers = []
        self.links = []

    def update(self):
        """
        This function generates the layers from the models
        """
        pass

    @staticmethod
    def amount_to_text(amount):
        return str(amount//100) + "," + str(amount % 100).zfill(2) + "€"


class MonthExtractor(Extractor):
    def __init__(self, models, month=None):
        super(MonthExtractor, self).__init__(models)
        if month is None:
            month = datetime.datetime.now()
        self.month = month

    def filter_transactions(self, element):
        tr_date = datetime.datetime.strptime(element["date"], DATE_FORMAT_PY)
        return tr_date.year == self.month.year and tr_date.month == self.month.month

    def update(self):
        """
        This function generates the layers from the models
        """
        # generate all transactions in the month
        transactions_received = []
        transactions_payed = []
        for element in self.model_tr.generate_all_transactions(self.filter_transactions):
            if element["amount"] > 0:
                transactions_received.append(element)
            else:
                transactions_payed.append(element)

        # get all the categories of origin
        categories_receive = {}
        for element in transactions_received:
            category = element["category_id"]
            if category not in categories_receive:
                categories_receive[category] = {"name": self.model_cat.get_name_for_id(category),
                                                "color": self.model_cat.get_colorstr_for_id(category),
                                                "amount": 0}
            categories_receive[category]["amount"] += element["amount"]
            element["category"] = categories_receive[category]

        # get all the destination categories
        categories_pay = {}
        for element in transactions_payed:
            category = element["category_id"]
            if category not in categories_pay:
                categories_pay[category] = {"name": self.model_cat.get_name_for_id(category),
                                            "color": self.model_cat.get_colorstr_for_id(category),
                                            "amount": 0}
            categories_pay[category]["amount"] -= element["amount"]
            element["category"] = categories_pay[category]

        total_receive = sum(element["amount"] for element in transactions_received)
        total_payed = sum(element["amount"] for element in transactions_payed)

        # update the layers 1 by 1
        self.layers = [GraphLayer() for i in range(5)]
        self.links = []

        # layer 1: origin categories
        for category_id, category in categories_receive.items():
            category["node"] = GraphNode(category["amount"], category["color"], info={"title": category["name"],
                                                                                      "text": ""})
            self.layers[1].nodes.append(category["node"])

        # layer 0: all transaction origins
        for element in transactions_received:
            info = {"title": element["desc"], "text": self.amount_to_text(element["amount"])}
            element["node"] = GraphNode(element["amount"], element["category"]["color"], info=info)
            self.layers[0].nodes.append(element["node"])

            self.links.append(GraphLink(element["node"], element["category"]["node"], element["amount"], info=info))

        # layer 0-1: origin accounts
        account_color = "#f0f0f0"
        if total_receive < total_payed:
            amt = total_payed-total_receive
            self.layers[0].nodes.append(GraphNode(amt, account_color))
            self.layers[1].nodes.append(GraphNode(amt, account_color))
            self.links.append(GraphLink(self.layers[0].nodes[-1], self.layers[1].nodes[-1], amt))

        # layer 3: dest categories
        for category_id, category in categories_pay.items():
            category["node"] = GraphNode(category["amount"], category["color"], info={"title": category["name"],
                                                                                      "text": ""})
            self.layers[3].nodes.append(category["node"])

        # layer 4: all transaction origins
        for element in transactions_payed:
            info = {"title": element["desc"], "text": self.amount_to_text(element["amount"])}
            element["node"] = GraphNode(element["amount"], element["category"]["color"], info=info)
            self.layers[4].nodes.append(element["node"])

            self.links.append(GraphLink(element["node"], element["category"]["node"], element["amount"], info=info))

        # layer 3-4: dest accounts
        account_color = "#a0a0a0"
        if total_receive > total_payed:
            amt = total_receive-total_payed
            self.layers[3].nodes.append(GraphNode(amt, account_color))
            self.layers[4].nodes.append(GraphNode(amt, account_color))
            self.links.append(GraphLink(self.layers[3].nodes[-1], self.layers[4].nodes[-1], amt))

        # layer 2: merge
        merge = GraphNode(max(total_receive, total_payed), account_color)
        self.layers[2].nodes.append(merge)
        for node in self.layers[1].nodes:
            self.links.append(GraphLink(node, merge, node.amount))
        for node in self.layers[3].nodes:
            self.links.append(GraphLink(merge, node, node.amount))
