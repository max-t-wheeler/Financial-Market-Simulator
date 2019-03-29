import csv
import fs_functions
import node
import numpy as np
import pandas as pd


class FinancialMarket:

    def __init__(self, num_financial_intermediaries, num_traders, max_money, log_portfolio=False):
        self.num_financial_intermediaries = num_financial_intermediaries
        self.num_traders = num_traders
        self.max_money = max_money

        # initialize node containers
        self.financial_intermediaries = []
        self.traders = []

        # create new financial intermediary,
        # create a portfolio, and add it to the storage list
        for i in range(self.num_financial_intermediaries):
            bank = node.FinancialIntermediary(i)
            bank.create_portfolio(1, 3, 1, 1)
            if log_portfolio:
                bank.print_portfolio()
            self.financial_intermediaries.append(bank)

        # create new trader,
        # create a portfolio, and add it to the storage list
        for i in range(num_traders):
            trader = node.Trader(i)
            trader.create_portfolio(1, 2, 2, 1, 1, self.max_money)
            if log_portfolio:
                trader.print_portfolio()
            self.traders.append(trader)

        # create accounts for each trader with the first financial intermediary
        if self.num_financial_intermediaries > 0:
            for trader in self.traders:
                self.financial_intermediaries[0].create_account(trader)

        self.agents = self.financial_intermediaries + self.traders

    # for a specified duration, simulate transactions between traders and financial intermediaries
    def simulate(self, t_max, file, log_portfolio=False, log_transactions=False):

        # at each time step, archive the current state of each agent
        # and perform random transaction between randomly selected pairs of nodes
        for t in range(t_max):
            for u in self.agents[:(len(self.agents) - 1)]:

                # archive data
                fs_functions.archive_portfolio(u, t, file)

                for v in self.agents[(self.agents.index(u) + 1):]:
                    if np.random.random(1) > 0.5:

                        # generate random transaction type
                        # 1: borrow; 2: lend; 3: trade; 4: deposit; 5: withdraw
                        transaction_type = np.random.random_integers(1, 5, 1)

                        if transaction_type == 1:
                            u.borrow(v, np.random.random() * self.max_money, log_transactions=log_transactions,
                                     log_portfolio=log_portfolio)
                        elif transaction_type == 2:
                            u.lend(v, np.random.random() * self.max_money, log_transactions=log_transactions,
                                   log_portfolio=log_portfolio)
                        elif transaction_type == 3:
                            asset_class_u = np.random.random_integers(0, 2, 1)[0]
                            asset_class_v = np.random.random_integers(0, 2, 1)[0]

                            if asset_class_u + asset_class_v > 0:
                                u.trade(v, asset_class_u, asset_class_v, log_transactions=log_transactions,
                                        log_portfolio=log_portfolio)
                        elif transaction_type == 4 and u.type != v.type:
                            u.deposit_cash(v, np.random.random() * u.portfolio['currency'][0].value,
                                           log_transactions=log_transactions, log_portfolio=log_portfolio)
                        elif transaction_type == 5 and u.type != v.type:
                            u.withdraw_cash(v, np.random.random() * u.portfolio['accounts'][0].value,
                                            log_transactions=log_transactions, log_portfolio=log_portfolio)

            # archive data for last node
            fs_functions.archive_portfolio(self.agents[-1], t, file)

    # print a summary of agent holdings along with overall market holdings
    def summary(self, asset_classes=None):

        fs_functions.print_holdings_summary(self.agents, asset_classes)

        print('')

        # print summary of initial economy holdings
        print('Money supply: ', fs_functions.money_supply(self.agents))

        print('')


if __name__ == "__main__":

    # declare constants
    DATA_FILE = 'data.csv'

    # initialize file for use in dataframe generation
    with open(DATA_FILE, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([
            'period',
            'type',
            'id',
            'wealth',
            'total cash',
            'total stock',
            'total bonds',
            'total liquid',
            'total loans',
            'total accounts'
        ])
    f.close()

    # create market
    market = FinancialMarket(0, 5, 10000)

    # display initial holdings
    market.summary(['currency', 'stocks', 'bonds'])

    # simulate agent-agent transactions
    market.simulate(3000, file=DATA_FILE, log_portfolio=False, log_transactions=False)

    # display final holdings
    market.summary(['currency', 'stocks', 'bonds'])

    # load data generated during simulation
    df = pd.read_csv(DATA_FILE)

    # plot wealth totals for all agents
    fs_functions.plot_wealth(df, market.agents, 'period', 'total liquid')
