import copy
import numpy as np


# allow agent to borrow currency from another agent
def borrow(source, target, amount, log_transactions=False, log_portfolio=False):
    if log_transactions:
        print('Agent', source.id, 'attempted to borrow', amount, 'from agent', target.id)

    # prevent transaction if target agent cannot lend desired amount
    # otherwise subtract amount from lender cash and add to borrower cash
    # and account for loan in each agent's portfolio
    if target.portfolio['currency'][0].value < amount:
        if log_transactions:
            print("Cannot borrow desired amount")
    else:
        if log_portfolio:
            print('_____________New transaction_____________')
            source.print_portfolio()
            target.print_portfolio()

        source.portfolio['currency'][0].value += amount
        source.portfolio['loans'][0].value -= amount
        target.portfolio['currency'][0].value -= amount
        target.portfolio['loans'][0].value += amount

        if log_transactions:
            print('Transaction completed successfully')

        if log_portfolio:
            source.print_portfolio()
            target.print_portfolio()


# allow agent to lend currency from another agent
def lend(source, target, amount, log_transactions=False, log_portfolio=False):
    if log_transactions:
        print('Agent', source.id, 'attempted to loan', amount, 'to agent', target.id)

    # prevent transaction if target agent cannot borrow desired amount
    # otherwise subtract amount from lender cash and add to borrower cash
    # and account for loan in each agent's portfolio
    if source.portfolio['currency'][0].value < amount:
        if log_transactions:
            print("Cannot lend desired amount")
    else:
        if log_portfolio:
            print('_____________New transaction_____________')
            source.print_portfolio()
            target.print_portfolio()

        source.portfolio['currency'][0].value -= amount
        source.portfolio['loans'][0].value += amount
        target.portfolio['currency'][0].value += amount
        target.portfolio['loans'][0].value -= amount

        if log_transactions:
            print('Transaction completed successfully')

        if log_portfolio:
            source.print_portfolio()
            target.print_portfolio()


def trade(source, target, asset_class_a, asset_class_b, log_transactions=False, log_portfolio=False):
    # convert class indices to strings
    asset_class_a = source.assets[asset_class_a]
    asset_class_b = target.assets[asset_class_b]

    # prevent transaction if either agent has no more assets of a particular class to trade
    # otherwise, randomly select an available asset
    if len(source.portfolio[asset_class_a]) > 0 and len(target.portfolio[asset_class_b]) > 0:
        asset_a = np.random.random_integers(0, len(source.portfolio[asset_class_a]) - 1, 1)[0]
        asset_b = np.random.random_integers(0, len(target.portfolio[asset_class_b]) - 1, 1)[0]
    else:
        if log_transactions:
            print('Could not trade desired asset')
        return 0

    if log_transactions:
        print('Agent', source.id, 'attempted to trade', source.portfolio[asset_class_a][asset_a].claim_class,
              source.portfolio[asset_class_a][asset_a].claim_id, 'to agent', target.id, 'for',
              target.portfolio[asset_class_b][asset_b].claim_class, target.portfolio[asset_class_b][asset_b].claim_id)

    # store asset values to determine transaction viability
    asset_a_value = source.portfolio[asset_class_a][asset_a].value
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
                source.print_portfolio()
                target.print_portfolio()

            # account for cash transfer
            source.portfolio[asset_class_a][asset_a].value -= target.portfolio[asset_class_b][asset_b].value
            target.portfolio[asset_class_a][asset_a].value += target.portfolio[asset_class_b][asset_b].value

            # copy asset to source portfolio
            source.portfolio[asset_class_b].append(copy.deepcopy(target.portfolio[asset_class_b][asset_b]))
            source.portfolio[asset_class_b][-1].owner_class = source.type
            source.portfolio[asset_class_b][-1].owner_id = source.id
            source.portfolio[asset_class_b][-1].claim_id = asset_class_b[0] + str(source.id) + str(
                len(source.portfolio[asset_class_b]) - 1)

            # remove asset from target portfolio
            del target.portfolio[asset_class_b][asset_b]

            if log_transactions:
                print('Transaction completed successfully')
            if log_portfolio:
                source.print_portfolio()
                target.print_portfolio()

    elif asset_class_a != 'currency' and asset_class_b == 'currency':
        if asset_a_value > asset_b_value:
            if log_transactions:
                print('Cannot trade desired asset')
        else:
            if log_portfolio:
                print('_____________New transaction_____________')
                source.print_portfolio()
                target.print_portfolio()

            # account for cash transfer
            target.portfolio[asset_class_b][asset_b].value -= source.portfolio[asset_class_a][asset_a].value
            source.portfolio[asset_class_b][asset_b].value += source.portfolio[asset_class_a][asset_a].value

            # copy asset to target portfolio
            target.portfolio[asset_class_a].append(copy.deepcopy(source.portfolio[asset_class_a][asset_a]))
            target.portfolio[asset_class_a][-1].owner_class = target.type
            target.portfolio[asset_class_a][-1].owner_id = target.id
            target.portfolio[asset_class_a][-1].claim_id = asset_class_a[0] + str(target.id) + str(
                len(target.portfolio[asset_class_a]) - 1)

            # remove asset from source portfolio
            del source.portfolio[asset_class_a][asset_a]

            if log_transactions:
                print('Transaction completed successfully')
            if log_portfolio:
                source.print_portfolio()
                target.print_portfolio()
    else:
        if asset_a_value != asset_b_value:
            if log_transactions:
                print('Cannot trade desired asset')
        else:
            if log_portfolio:
                print('_____________New transaction_____________')
                source.print_portfolio()
                target.print_portfolio()

            # copy asset to source portfolio
            source.portfolio[asset_class_b].append(copy.deepcopy(target.portfolio[asset_class_b][asset_b]))
            source.portfolio[asset_class_b][-1].owner_class = source.type
            source.portfolio[asset_class_b][-1].owner_id = source.id
            source.portfolio[asset_class_b][-1].claim_id = asset_class_b[0] + str(source.id) + str(
                len(source.portfolio[asset_class_b]) - 1)

            # copy asset to target portfolio
            target.portfolio[asset_class_a].append(copy.deepcopy(source.portfolio[asset_class_a][asset_a]))
            target.portfolio[asset_class_a][-1].owner_class = target.type
            target.portfolio[asset_class_a][-1].owner_id = target.id
            target.portfolio[asset_class_a][-1].claim_id = asset_class_a[0] + str(target.id) + str(
                len(target.portfolio[asset_class_a]) - 1)

            # remove asset from target portfolio
            del target.portfolio[asset_class_b][asset_b]

            # remove asset from source portfolio
            del source.portfolio[asset_class_a][asset_a]

            if log_transactions:
                print('Transaction completed successfully')
            if log_portfolio:
                source.print_portfolio()
                target.print_portfolio()


# allow a trader to deposit cash into an account
def deposit_cash(source, target, amount, log_transactions=False, log_portfolio=False):

    if log_transactions:
        print('Agent', source.id, 'attempted to deposit', amount)

    if source.portfolio['currency'][0].value < amount:
        if log_transactions:
            print('Insufficient funds')
    else:
        if log_portfolio:
            print('_____________New transaction_____________')
            source.print_portfolio()
            target.print_portfolio()

        # remove cash from source cash store, account for deposit within accounts store
        # and add deposited cash to target account
        source.portfolio['currency'][0].value -= amount
        source.portfolio['accounts'][0].value += amount
        target.accounts[source.id].assets['currency'] += amount

        if log_transactions:
            print('Agent', source.id, 'deposited', amount, 'successfully')

        if log_portfolio:
            source.print_portfolio()
            target.print_portfolio()


# allow a trader to withdraw cash from an account
def withdraw_cash(source, target, amount, log_transactions=False, log_portfolio=False):

    if log_transactions:
        print('Agent', source.id, 'attempted to withdraw', amount)

    if target.accounts[source.id].assets['currency'] < amount:
        if log_transactions:
            print('Insufficient funds')
    else:
        if log_portfolio:
            print('_____________New transaction_____________')
            source.print_portfolio()
            target.print_portfolio()

        # remove cash from target account,
        # add withdrawn cash to source cash, and account for withdrawal within accounts store
        target.accounts[source.id].assets['currency'] -= amount
        source.portfolio['currency'][0].value += amount
        source.portfolio['accounts'][0].value -= amount

        if log_transactions:
            print('Agent', source.id, 'withdrew', amount, 'successfully')

        if log_portfolio:
            source.print_portfolio()
            target.print_portfolio()