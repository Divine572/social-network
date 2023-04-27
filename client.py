import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

import deploy

# Load environment variables
load_dotenv()

# Set up web3 connection
provider_url = os.getenv("CELO_PROVIDER_URL")
w3 = Web3(HTTPProvider(provider_url))
assert w3.is_connected(), "Not connected to a Celo node"

# Add PoA middleware to web3.py instance
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Get contract ABI and address
abi = deploy.abi
contract_address = deploy.contract_address

# Initialize account
deployer_address = os.getenv("CELO_DEPLOYER_ADDRESS")
private_key = os.getenv("CELO_DEPLOYER_PRIVATE_KEY")
# account = w3.eth.account.from_key(private_key)


# Set default gas price and gas limit
default_gas_limit = 2000000

# Get contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)


def create_user(username):
    # Estimate gas required for the transaction
    gas_estimate = contract.functions.createUser(
        username).estimate_gas({"from": deployer_address})

    # Set gas price and limit
    gas_price = w3.eth.gas_price
    gas_limit = min(gas_estimate * 2, default_gas_limit)

    # Build transaction object
    txn = contract.functions.createUser(username).build_transaction({
        "from": deployer_address,
        "nonce": w3.eth.get_transaction_count(deployer_address),
        "gasPrice": gas_price,
        "gas": gas_limit
    })

    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for transaction confirmation and return receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


def create_post(content):
    # Estimate gas required for the transaction
    gas_estimate = contract.functions.createPost(
        content).estimate_gas({"from": deployer_address})

    # Set gas price and limit
    gas_price = w3.eth.gas_price
    gas_limit = min(gas_estimate * 2, default_gas_limit)

    # Build transaction object
    txn = contract.functions.createPost(content).build_transaction({
        "from": deployer_address,
        "nonce": w3.eth.get_transaction_count(deployer_address),
        "gasPrice": gas_price,
        "gas": gas_limit
    })

    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for transaction confirmation and return receipt
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


def get_post(index):
    try:
        post = contract.functions.getPost(index).call()
        return post
    except Exception as e:
        print(f"Error retrieving post: {e}")
        return None


def get_post_count():
    try:
        post_count = contract.functions.getPostCount().call()
        return post_count
    except Exception as e:
        print(f"Error retrieving post count: {e}")
        return None


# Test functions
def main():
    try:
        # Test create_user and create_post functions
        create_user("Gloria")
        create_user("John")
        create_post("Hello, world!")
        create_post("This is my first post.")
        # Test get_post and get_post_count functions
        post_count = get_post_count()
        if post_count is not None:
            print("Total number of posts:", post_count)

            for i in range(post_count):
                post = get_post(i)
                if post is not None:
                    print("Post", i + 1)
                    print("Author:", post[0])
                    print("Content:", post[1])
                    print("Timestamp:", post[2])

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
