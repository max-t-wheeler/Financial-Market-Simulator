import csv
import matplotlib.pyplot as plt
import pandas as pd


# calculate total amount of money in a financial market
def money_supply(economy):
    wealth_sum = 0
    for agent in economy:
        wealth_sum += agent.wealth()
    return wealth_sum

# print agent holdings summary
def print_holdings_summary(financial_market, assets):
    for v in financial_market:
        print(v.type, v.id, 'has', v.wealth(assets))

# write portfolio data to csv
def archive_portfolio(agent, period, target):

    with open(target, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        new_record = [
            period,
            agent.type,
            agent.id,
            agent.wealth(),
            agent.wealth(['currency']),
            agent.wealth(['stocks']),
            agent.wealth(['bonds']),
            agent.wealth(['currency', 'stocks', 'bonds']),
            agent.wealth(['loans']),
            agent.wealth(['accounts'])
        ]
        csv_writer.writerow(new_record)
    f.close()


# plot wealth
def plot_wealth(data, financial_market, x='period', y='wealth'):
    for v in financial_market:
        agent_data = data[data['type'] == v.type]
        agent_data = agent_data[agent_data.id == v.id]
        plt.plot(agent_data[x], agent_data[y], label=v.type + ' ' + str(v.id))
    plt.title('Agent Wealth vs Time')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    plt.show()
