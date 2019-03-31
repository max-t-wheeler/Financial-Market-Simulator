import copy
import numpy as np


class Claim:
    def __init__(self, owner_class, owner_id, claim_class, claim_id, value):
        self.owner_class = owner_class
        self.owner_id = owner_id
        self.claim_class = claim_class
        self.claim_id = claim_id
        self.value = value


class Account:
    def __init__(self):
        self.assets = {
            'currency': 0
        }


# base class for agents in financial markets
class Agent:

    assets = ["currency", "stocks", "bonds", "loans", "accounts"]

    def __init__(self, agent_id):
        self.id = agent_id
        self.accounts = {}
        self.portfolio = {
            'currency': [],
            'stocks': [],
            'bonds': [],
            'loans': [],
            'accounts': []
        }

    # print portfolio contents
    def print_portfolio(self):
        for asset_class in self.portfolio:
            for asset in self.portfolio[asset_class]:
                print('Owner Class', ':', asset.owner_class)
                print('Owner ID', ':', asset.owner_id)
                print('Claim Class', ':', asset.claim_class)
                print('Claim ID', ':', asset.claim_id)
                print('Value', ':', asset.value)
                print('')

    # return the sum of one or more asset class values
    def wealth(self, asset_classes=None):
        wealth = 0
        if asset_classes is None:
            asset_classes = self.portfolio
        for asset_class in asset_classes:
            for asset in self.portfolio[asset_class]:
                wealth += asset.value
        return wealth


class FinancialIntermediary(Agent):

    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.type = 'Financial Intermediary'

    def create_account(self, agent):
        account = Account()
        self.accounts[agent.id] = account

    def create_portfolio(self, currency_vals, num_stocks, num_bonds, num_loans):

        num_accounts = len(self.accounts)

        for i in range(currency_vals):
            asset = Claim(self.type, self.id, self.assets[0], '', 0)
            if num_accounts > 0:
                for j in range(num_accounts):
                    asset.value = asset.value + self.accounts[j].asset[0].value
            self.portfolio['currency'].append(asset)

        for i in range(num_stocks):
            asset = Claim(self.type, self.id, self.assets[1], self.assets[1][0] + str(self.id) + str(i), 0)
            if num_accounts > 0:
                for j in range(num_accounts):
                    asset.value = asset.value + self.accounts[j].asset[1].value
            self.portfolio['stocks'].append(asset)

        for i in range(num_bonds):
            asset = Claim(self.type, self.id, self.assets[2], self.assets[2][0] + str(self.id) + str(i), 0)
            if num_accounts > 0:
                for j in range(num_accounts):
                    asset.value = asset.value + self.accounts[j].asset[1].value
            self.portfolio['bonds'].append(asset)

        for i in range(num_loans):
            asset = Claim(self.type, self.id, self.assets[3], self.assets[3][0] + str(self.id) + str(i), 0)
            if num_accounts > 0:
                for j in range(num_accounts):
                    asset.value = asset.value + self.accounts[j].asset[3].value
            self.portfolio['loans'].append(asset)


class Trader(Agent):

    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.type = 'Trader'

    def create_portfolio(self, currency_vals, num_stocks, num_bonds, num_loans, num_accounts, money_cap):

        for i in range(currency_vals):
            asset = Claim(self.type, self.id, self.assets[0], '', np.random.random(1)[0] * money_cap)
            self.portfolio['currency'].append(asset)

        for i in range(num_stocks):
            asset = Claim(self.type, self.id, self.assets[1], self.assets[1][0] + str(self.id) + str(i), np.random.random(1)[0] * money_cap)
            self.portfolio['stocks'].append(asset)

        for i in range(num_bonds):
            asset = Claim(self.type, self.id, self.assets[2], self.assets[2][0] + str(self.id) + str(i), np.random.random(1)[0] * money_cap)
            self.portfolio['bonds'].append(asset)

        for i in range(num_loans):
            asset = Claim(self.type, self.id, self.assets[3], self.assets[3][0] + str(self.id) + str(i), 0)
            self.portfolio['loans'].append(asset)

        for i in range(num_accounts):
            asset = Claim(self.type, self.id, self.assets[4], '', 0)
            self.portfolio['accounts'].append(asset)
