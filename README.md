# Financial-Market-Simulator

This is a simple program designed to simulate transactions between agents in a financial market. Each agent within the market is a designated a trader or a financial intermediary and each is assigned a portfolio containing various assets (claims) in five asset classes: 
* currency (cash) 
* stocks (equities)
* bonds (debt instruments)
* loans (amount owed or amout due)
* accounts (assets in the posession of a financial intermediary)

Agents are initialized along with their portfolios (and accounts in the presence of a financial intermediary) and introduced into a financial market. For N time steps, each agent may enter into a random transaction with another agent in the market, opting into a loan contract (agent-agent loan), sale contract (agent-agent trade), or savings contract (account deposit or withdrawal). At each time step, the total wealth of each agent (along with totals of liquid and non-liquid assets) is archived for further use in the analysis and visualization of the data generated during the simulation.

This project employs pandas and matplotlib to work with and visualize simulated data. NetworkX may also be used in the future for network visualization.

To work with this library, install the necessary dependencies by running the following command:

pip install -r requirements.txt
