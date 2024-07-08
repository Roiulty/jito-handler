import os

from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.rpc.requests import IsBlockhashValid
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction, Pubkey, Blockhash
from dotenv import load_dotenv
from config import Settings
import base58
import base64
import json
import random
import requests
import array

load_dotenv()
settings = Settings


class JitoClient(Client):

    def create_transaction(self, sender_object, sender, recipient, amount: int) -> str:
        # Init Transaction
        transaction = Transaction()

        # Create Instructions, add to Transaction
        transfer_instructions = transfer(
            TransferParams(
                from_pubkey=sender,
                to_pubkey=recipient,
                lamports=amount  # In Lamports
            )
        )
        transaction.add(transfer_instructions)

        # Get the Latest Blockhash from the network
        blockhash = self.get_recent_blockhash()
        transaction.recent_blockhash = Blockhash.from_string(blockhash)
        transaction.sign(sender_object)

        # Signed Transaction MUST be Base58 Encoded as Base64 is not supported by Jito
        serialized_tx = base58.b58encode(transaction.serialize()).decode('utf-8')

        return serialized_tx

    def create_tip_transaction(self, sender_object, sender, amount: int, environment) -> str:

        try:
            tip_accounts = self.get_tip_accounts()

        except KeyError as e:
            if environment == "DEV":
                tip_accounts = settings.TEST_BACKUP_TIP_ACCOUNTS
            elif environment == "PROD":
                tip_accounts = settings.MAIN_BACKUP_TIP_ACCOUNTS
            else:
                raise Exception("Environment not set, please set 'DEV' or 'PROD' under 'ENVIRONMENT' in config")

        tip_account = random.choice(tip_accounts)
        receiver = Pubkey.from_string(tip_account)

        # Init Transaction
        transaction = Transaction()

        # Create Instructions, add to Transaction
        transfer_instructions = transfer(
            TransferParams(
                from_pubkey=sender,
                to_pubkey=receiver,
                lamports=amount  # In Lamports
            )
        )
        transaction.add(transfer_instructions)

        # Get the Latest Blockhash from the network
        blockhash = self.get_recent_blockhash()
        transaction.recent_blockhash = Blockhash.from_string(blockhash)
        transaction.sign(sender_object)

        # Signed Transaction MUST be Base58 Encoded as Base64 is not supported by Jito
        serialized_tx = base58.b58encode(transaction.serialize()).decode('utf-8')

        return serialized_tx

    def get_recent_blockhash(self) -> str:
        # Get the latest Blockhash from the Solana Network
        recent_blockhash = self.get_latest_blockhash().to_json()

        # Convert to JSON for Parsing
        blockhash = json.loads(recent_blockhash)

        # Validate if a blockhash was returned
        if not blockhash or "result" not in blockhash or "value" not in blockhash["result"] or "blockhash" not in blockhash["result"]["value"]:
            raise Exception("Failed to get recent Blockhash")

        # Extract and return the blockhash
        result = blockhash["result"]["value"]["blockhash"]
        return result

    @staticmethod
    def get_tip_accounts():

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTipAccounts",
            "params": []
        }

        tip_accounts = requests.post(
            url=settings.JITO_TESTNET + settings.BUNDLE_ENDPOINT,
            headers=headers,
            json=payload
        )
        accounts = tip_accounts.json()
        result = accounts["result"]
        return result

    @staticmethod
    def get_bundle_statuses(bundle_id: str, network: str):
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBundleStatuses",
            "params": [
                [
                    bundle_id
                ]
            ]
        }

        response = requests.post(
            url=(network + settings.BUNDLE_ENDPOINT),
            headers=headers,
            json=payload
        )

        response = response.json()
        result = response["result"]
        value = result["value"]

        if not value:
            print("No bundles found in the response.")
            return None

            # Iterate through each bundle in the value list
        for bundle in value:
            confirmation_status = bundle.get('confirmation_status', 'unknown')
            print(f'Confirmation Status: {confirmation_status}')
            return confirmation_status

        print("No confirmation status found.")
        return None

    @staticmethod
    def send_bundle(transactions: list, network: str):
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sendBundle",
            "params": [
                transactions
            ]
        }

        response = requests.post(
            url=f'{network}{settings.BUNDLE_ENDPOINT}',
            headers=headers,
            json=payload
        )
        bundle = response.json()
        result = bundle["result"]
        return result

    @staticmethod # Helper Function
    def sol_to_lamports(sol: float):
        lamports = sol * 1000000000
        return lamports


###### EXAMPLE USAGE

# SETUP YOUR ENVIRONMENT IN CONFIG
# ENVIROMENT SHOULD BE DEV OR PROD
# IF YOURE USING DEV YOUR NETWORKS SHOULD BE TESTNET NOT MAINNET

# BUNDLE STATUSES DO NOT RETURN ON THE JITO TESTNET, HOWEVER THE SLOT THEY ARE PROCESSED IN DOES RETURN


client = JitoClient(settings.SOL_TESTNET)

#sx = Keypair()
#rx = Keypair()

#tx1 = client.create_transaction(sender_object=sx, sender=sx.pubkey(), recipient=rx.pubkey(), amount=100000)
#tx2 = client.create_transaction(sender_object=sx, sender=sx.pubkey(), recipient=rx.pubkey(), amount=100000)
#tx3 = client.create_transaction(sender_object=sx, sender=sx.pubkey(), recipient=rx.pubkey(), amount=100000)
#tip_tx = client.create_tip_transaction(sender_object=sx, sender=sx.pubkey(), amount=15000, environment=settings.ENVIRONMENT)

#txns = [tx1, tx2, tx3, tip_tx]

#bundle = client.send_bundle(transactions=txns, network=settings.JITO_TESTNET)

#print(client.get_bundle_statuses(bundle_id=bundle, network=settings.JITO_TESTNET))


sender = Keypair.from_base58_string(os.getenv('SEED_PHRASE'))

sx_addr = Pubkey.from_string(os.getenv('MAIN_WALLET'))
rx = Pubkey.from_string(os.getenv('TEST_WALLET'))

tx = client.create_transaction(sender_object=sender, sender=sx_addr, recipient=rx, amount=10000000)
tip = client.create_tip_transaction(sender_object=sender, sender=sx_addr, amount=2000, environment=settings.ENVIRONMENT)

txns = [tx, tip]

bundle = client.send_bundle(transactions=txns, network=settings.JITO_TESTNET)
print(bundle)
status = client.get_bundle_statuses(bundle_id=bundle, network=settings.JITO_TESTNET)
print(status)

