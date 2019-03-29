import copy
import numpy as np


class Claim:
    def __init__(self):
        self.owner_class = ''
        self.owner_id = ''
        self.claim_title = ''
        self.claim_id = ''
        self.value = 0


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

    # allow agent to borrow currency from another agent
    def borrow(self, target, amount, log_transactions=False, log_portfolio=False):

        if log_transactions:
            print('Agent', self.id, 'attempted to borrow', amount, 'from agent', target.id)

        # prevent transaction if target agent cannot lend desired amount
        # otherwise subtract amount from lender cash and add to borrower cash
        # and account for loan in each agent's portfolio
        if target.portfolio['currency'][0].value < amount:
            if log_transactions:
                print("Cannot borrow desired amount")
        else:
            if log_portfolio:
                print('_____________New transaction_____________')
                self.print_portfolio()
                target.print_portfolio()

            self.portfolio['currency'][0].value += amount
            self.portfolio['loans'][0].value -= amount
            target.portfolio['currency'][0].value -= amount
            target.portfolio['loans'][0].value += amount

            if log_transactions:
                print('Transaction completed successfully')

            if log_portfolio:
                self.print_portfolio()
                target.print_portfolio()

    # allow agent to lend currency from another agent
    def lend(self, target, amount, log_transactions=False, log_portfolio=False):

        if log_transactions:
            print('Agent', self.id, 'attempted to loan', amount, 'to agent', target.id)

        # prevent transaction if target agent cannot borrow desired amount
        # otherwise subtract amount from lender cash and add to borrower cash
        # and account for loan in each agent's portfolio
        if self.portfolio['currency'][0].value < amount:
            if log_transactions:
                print("Cannot lend desired amount")
        else:
            if log_portfolio:
                print('_____________New transaction_____________')
                self.print_portfolio()
                target.print_portfolio()

            self.portfolio['currency'][0].value -= amount
            self.portfolio['loans'][0].value += amount
            target.portfolio['currency'][0].value += amount
            target.portfolio['loans'][0].value -= amount

            if log_transactions:
                print('Transaction completed successfully')

            if log_portfolio:
                self.print_portfolio()
                target.print_portfolio()

    def trade(self, target, asset_class_a, asset_class_b, log_transactions=False, log_portfolio=False):

        # convert class indices to strings
        asset_class_a = self.assets[asset_class_a]
        asset_class_b = target.assets[asset_class_b]

        # prevent transaction if either agent has no more assets of a particular class to trade
        # otherwise, randomly select an available asset
        if len(self.portfolio[asset_class_a]) > 0 and len(target.portfolio[asset_class_b]) > 0:
            asset_a = np.random.random_integers(0, len(self.portfolio[asset_class_a]) - 1, 1)[0]
            asset_b = np.random.random_integers(0, len(target.portfolio[asset_class_b]) - 1, 1)[0]
        else:
            if log_transactions:
                print('Could not trade desired asset')
            return 0

        if log_transactions:
            print('Agent', self.id, 'attempted to trade', self.portfolio[asset_class_a][asset_a].claim_class, self.portfolio[asset_class_a][asset_a].claim_id, 'to agent', target.id, 'for', target.portfolio[asset_class_b][asset_b].claim_class, target.portfolio[asset_class_b][asset_b].claim_id)

        # store asset values to determine transaction viability
        asset_a_value = self.portfolio[asset_class_a][asset_a].value
        asset_b_value = target.portfolio[asset_class_b][asset_b].value

        # if a non-cash asset is traded for a cash asset, ensure that the trader has sufficient funds
        # and then swap the cash amounts and assets in each trader's portfolio
        # in the case of a non-cash asset-non-cash asset transaction
        # the values of each asset must match for the transaction to proceed
        if asset_class_a == 'currency' and asset_class_b != 'currency':
            if asset_a_value < asset_b_value:
                if log_transactions:
                    print('Cannot trade desired asset')
            else:
                if log_portfolio:
                    print('_____________New transaction_____________')
                    self.print_portfolio()
                    target.print_portfolio()

                # account for cash transfer
                self.portfolio[asset_class_a][asset_a].value -= target.portfolio[asset_class_b][asset_b].value
                target.portfolio[asset_class_a][asset_a].value += target.portfolio[asset_class_b][asset_b].value

                # copy asset to source portfolio
                self.portfolio[asset_class_b].append(copy.deepcopy(target.portfolio[asset_class_b][asset_b]))
                self.portfolio[asset_class_b][-1].owner_class = self.type
                self.portfolio[asset_class_b][-1].owner_id = self.id
                self.portfolio[asset_class_b][-1].claim_id = asset_class_b[0] + str(self.id) + str(len(self.portfolio[asset_class_b]) - 1)

                # remove asset from target portfolio
                del target.portfolio[asset_class_b][asset_b]

                if log_transactions:
                    print('Transaction completed successfully')
                if log_portfolio:
                    self.print_portfolio()
                    target.print_portfolio()

        elif asset_class_a != 'currency' and asset_class_b == 'currency':
            if asset_a_value > asset_b_value:
                if log_transactions:
                    print('Cannot trade desired asset')
            else:
                if log_portfolio:
                    print('_____________New transaction_____________')
                    self.print_portfolio()
                    target.print_portfolio()

                # account for cash transfer
                target.portfolio[asset_class_b][asset_b].value -= self.portfolio[asset_class_a][asset_a].value
                self.portfolio[asset_class_b][asset_b].value += self.portfolio[asset_class_a][asset_a].value

                # copy asset to target portfolio
                target.portfolio[asset_class_a].append(copy.deepcopy(self.portfolio[asset_class_a][asset_a]))
                target.portfolio[asset_class_a][-1].owner_class = target.type
                target.portfolio[asset_class_a][-1].owner_id = target.id
                target.portfolio[asset_class_a][-1].claim_id = asset_class_a[0] + str(target.id) + str(len(target.portfolio[asset_class_a]) - 1)

                # remove asset from source portfolio
                del self.portfolio[asset_class_a][asset_a]

                if log_transactions:
                    print('Transaction completed successfully')
                if log_portfolio:
                    self.print_portfolio()
                    target.print_portfolio()
        else:
            if asset_a_value != asset_b_value:
                if log_transactions:
                    print('Cannot trade desired asset')
            else:
                if log_portfolio:
                    print('_____________New transaction_____________')
                    self.print_portfolio()
                    target.print_portfolio()

                # copy asset to source portfolio
                self.portfolio[asset_class_b].append(copy.deepcopy(target.portfolio[asset_class_b][asset_b]))
                self.portfolio[asset_class_b][-1].owner_class = self.type
                self.portfolio[asset_class_b][-1].owner_id = self.id
                self.portfolio[asset_class_b][-1].claim_id = asset_class_b[0] + str(self.id) + str(len(self.portfolio[asset_class_b]) - 1)

                # copy asset to target portfolio
                target.portfolio[asset_class_a].append(copy.deepcopy(self.portfolio[asset_class_a][asset_a]))
                target.portfolio[asset_class_a][-1].owner_class = target.type
                target.portfolio[asset_class_a][-1].owner_id = target.id
                target.portfolio[asset_class_a][-1].claim_id = asset_class_a[0] + str(target.id) + str(len(target.portfolio[asset_class_a]) - 1)

                # remove asset from target portfolio
                del target.portfolio[asset_class_b][asset_b]

                # remove asset from source portfolio
                del self.portfolio[asset_class_a][asset_a]

                if log_transactions:
                    print('Transaction completed successfully')
                if log_portfolio:
                    self.print_portfolio()
                    target.print_portfolio()

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
        val = 0

        for i in range(currency_vals):
            asset = Claim()
            self.portfolio['currency'].append(asset)
            self.portfolio['currency'][i].owner_class = self.type
            self.portfolio['currency'][i].owner_id = self.id
            self.portfolio['currency'][i].claim_class = self.assets[0]
            if num_accounts > 0:
                for j in range(num_accounts):
                    val = val + self.accounts[j].asset[0].value
                self.portfolio['currency'][i].value = val

        for i in range(num_stocks):
            asset = Claim()
            self.portfolio['stocks'].append(asset)
            self.portfolio['stocks'][i].owner_class = self.type
            self.portfolio['stocks'][i].owner_id = self.id
            self.portfolio['stocks'][i].claim_class = self.assets[1]
            self.portfolio['stocks'][i].claim_id = self.assets[1][0] + str(self.id) + str(i)
            if num_accounts > 0:
                for j in range(num_accounts):
                    val = val + self.accounts[j].asset[1].value
                self.portfolio['stocks'][i].value = val

        for i in range(num_bonds):
            asset = Claim()
            self.portfolio['bonds'].append(asset)
            self.portfolio['bonds'][i].owner_class = self.type
            self.portfolio['bonds'][i].owner_id = self.id
            self.portfolio['bonds'][i].claim_class = self.assets[2]
            self.portfolio['bonds'][i].claim_id = self.assets[2][0] + str(self.id) + str(i)
            if num_accounts > 0:
                for j in range(num_accounts):
                    val = val + self.accounts[j].asset[2].value
                self.portfolio['bonds'][i].value = val

        for i in range(num_loans):
            asset = Claim()
            self.portfolio['loans'].append(asset)
            self.portfolio['loans'][i].owner_class = self.type
            self.portfolio['loans'][i].owner_id = self.id
            self.portfolio['loans'][i].claim_class = self.assets[3]
            self.portfolio['loans'][i].claim_id = self.assets[3][0] + str(self.id) + str(i)
            if num_accounts > 0:
                for j in range(num_accounts):
                    val = val + self.accounts[j].asset[i].value
                self.portfolio['loans'][i].value = val


class Trader(Agent):

    def __init__(self, agent_id):
        super().__init__(agent_id)
        self.type = 'Trader'

    def create_portfolio(self, currency_vals, num_stocks, num_bonds, num_loans, num_accounts, max_money):

        for i in range(currency_vals):
            asset = Claim()
            self.portfolio['currency'].append(asset)
            self.portfolio['currency'][i].owner_class = self.type
            self.portfolio['currency'][i].owner_id = self.id
            self.portfolio['currency'][i].claim_class = self.assets[0]
            self.portfolio['currency'][i].value = np.random.random(1)[0] * max_money

        for i in range(num_stocks):
            asset = Claim()
            self.portfolio['stocks'].append(asset)
            self.portfolio['stocks'][i].owner_class = self.type
            self.portfolio['stocks'][i].owner_id = self.id
            self.portfolio['stocks'][i].claim_class = self.assets[1]
            self.portfolio['stocks'][i].claim_id = self.assets[1][0] + str(self.id) + str(i)
            self.portfolio['stocks'][i].value = np.random.random(1)[0] * max_money

        for i in range(num_bonds):
            asset = Claim()
            self.portfolio['bonds'].append(asset)
            self.portfolio['bonds'][i].owner_class = self.type
            self.portfolio['bonds'][i].owner_id = self.id
            self.portfolio['bonds'][i].claim_class = self.assets[2]
            self.portfolio['bonds'][i].claim_id = self.assets[2][0] + str(self.id) + str(i)
            self.portfolio['bonds'][i].value = np.random.random(1)[0] * max_money

        for i in range(num_loans):
            asset = Claim()
            self.portfolio['loans'].append(asset)
            self.portfolio['loans'][i].owner_class = self.type
            self.portfolio['loans'][i].owner_id = self.id
            self.portfolio['loans'][i].claim_class = self.assets[3]
            self.portfolio['loans'][i].claim_id = self.assets[3][0] + str(self.id) + str(i)
            self.portfolio['loans'][i].value = 0

        for i in range(num_accounts):
            asset = Claim()
            self.portfolio['accounts'].append(asset)
            self.portfolio['accounts'][i].owner_class = self.type
            self.portfolio['accounts'][i].owner_id = self.id
            self.portfolio['accounts'][i].claim_class = self.assets[4]
            self.portfolio['accounts'][i].value = 0

    # allow a trader to deposit cash into an account
    def deposit_cash(self, target, amount, log_transactions=False, log_portfolio=False):

        if log_transactions:
            print('Agent', self.id, 'attempted to deposit', amount)

        if self.portfolio['currency'][0].value < amount:
            if log_transactions:
                print('Insufficient funds')
        else:
            if log_portfolio:
                print('_____________New transaction_____________')
                self.print_portfolio()
                target.print_portfolio()

            # remove cash from source cash store, account for deposit within accounts store
            # and add deposited cash to target account
            self.portfolio['currency'][0].value -= amount
            self.portfolio['accounts'][0].value += amount
            target.accounts[self.id].assets['currency'] += amount

            if log_transactions:
                print('Agent', self.id, 'deposited', amount, 'successfully')

            if log_portfolio:
                self.print_portfolio()
                target.print_portfolio()

    # allow a trader to withdraw cash from an account
    def withdraw_cash(self, target, amount, log_transactions=False, log_portfolio=False):

        if log_transactions:
            print('Agent', self.id, 'attempted to withdraw', amount)

        if target.accounts[self.id].assets['currency'] < amount:
            if log_transactions:
                print('Insufficient funds')
        else:
            if log_portfolio:
                print('_____________New transaction_____________')
                self.print_portfolio()
                target.print_portfolio()

            # remove cash from target account,
            # add withdrawn cash to source cash, and account for withdrawal within accounts store
            target.accounts[self.id].assets['currency'] -= amount
            self.portfolio['currency'][0].value += amount
            self.portfolio['accounts'][0].value -= amount

            if log_transactions:
                print('Agent', self.id, 'withdrew', amount, 'successfully')

            if log_portfolio:
                self.print_portfolio()
                target.print_portfolio()
