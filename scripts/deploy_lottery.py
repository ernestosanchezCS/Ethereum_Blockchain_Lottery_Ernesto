from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
        # this last line above will default to False if not explicitly told ot verify
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery has been activated.")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    # returns cost to enter adding a little bit to ensure it passes
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery.")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # before we can end the lottery we gonna need to make sure our Lottery contract has some link in it
    # since it uses requestRandomness function itll need to have link to process the request
    # thus we need to fund the contract, then end the lottery
    # funding contracts with link will be quite common so lets make it into a helpful script
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    # now we have funded the contract with link
    tx_end = lottery.endLottery({"from": account})
    tx_end.wait(1)
    time.sleep(180)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
