import csv
import fs_functions
import node
import numpy as np
import pandas as pd

if __name__ == "__main__":

    # declare constants
    DATA_FILE = 'data.csv'

    # specify logging preferences
    log_money_supply = False
    log_transactions = False
    log_portfolio = False

    # initialize lists to store agent types
    financial_intermediaries = []
    traders = []

    # specify number of each agent type
    num_fin_int = 0
    num_traders = 5

    # specify number of time steps
    t_max = 3000

    # create new financial intermediary,
    # create a portfolio, and add it to the storage list
    for i in range(num_fin_int):
        bank = node.FinancialIntermediary(i)
        bank.create_portfolio(1, 3, 1, 1)
        if log_portfolio:
            bank.print_portfolio()
        financial_intermediaries.append(bank)

    # create new trader,
    # create a portfolio, and add it to the storage list
    for i in range(num_traders):
        trader = node.Trader(i)
        trader.create_portfolio(1, 2, 2, 1, 1)
        if log_portfolio:
            trader.print_portfolio()
        traders.append(trader)

    # create accounts for each trader at the first financial intermediary
    if num_fin_int > 0:
        for trader in traders:
            financial_intermediaries[0].create_account(trader)

    # create network to store agents
    financial_market = traders + financial_intermediaries

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

    if log_money_supply:
        # print summary of initial holdings
        for v in financial_market:
            print(v.type, v.id, 'has', v.wealth(['currency']), 'in cash')

        print('')

        # print summary of initial economy holdings
        print('Money supply: ', fs_functions.money_supply(financial_market))

        print('')

    # at each time step, archive the current state of each agent
    # and perform random transaction between randomly selected pairs of nodes
    for t in range(t_max):
        for u in financial_market[:(len(financial_market) - 1)]:

            # archive data
            fs_functions.archive_portfolio(u, t, DATA_FILE)

            for v in financial_market[(financial_market.index(u) + 1):]:
                if np.random.random(1) > 0.5:

                    # generate random transaction type
                    # 1: borrow; 2: lend; 3: trade; 4: deposit; 5: withdraw
                    transaction_type = np.random.random_integers(1, 5, 1)

                    if transaction_type == 1:
                        u.borrow(v, np.random.random() * 100, log_transactions=log_transactions, log_portfolio=log_portfolio)
                    elif transaction_type == 2:
                        u.lend(v, np.random.random() * 100, log_transactions=log_transactions, log_portfolio=log_portfolio)
                    elif transaction_type == 3:
                        asset_class_u = np.random.random_integers(0, 2, 1)[0]
                        asset_class_v = np.random.random_integers(0, 2, 1)[0]

                        if asset_class_u + asset_class_v > 0:
                            u.trade(v, asset_class_u, asset_class_v, log_transactions=log_transactions, log_portfolio=log_portfolio)
                    elif transaction_type == 4 and u.type != v.type:
                        u.deposit_cash(v, np.random.random() * u.portfolio['currency'][0].value, log_transactions=log_transactions, log_portfolio=log_portfolio)
                    elif transaction_type == 5 and u.type != v.type:
                        u.withdraw_cash(v, np.random.random() * u.portfolio['accounts'][0].value, log_transactions=log_transactions, log_portfolio=log_portfolio)

        # archive data for last node
        fs_functions.archive_portfolio(financial_market[-1], t, DATA_FILE)

    if log_money_supply:

        # print summary of initial holdings
        for v in financial_market:
            print(v.type, v.id, 'has', v.wealth(['currency']), 'in cash')

        print('')

        # print summary of initial economy holdings
        print('Money supply: ', fs_functions.money_supply(financial_market))

        print('')

    # generate dataframe
    df = pd.read_csv(DATA_FILE)

    # plot wealth totals for all agents
    fs_functions.plot_wealth(df, financial_market, 'period', 'total liquid')
