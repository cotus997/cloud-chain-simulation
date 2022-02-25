import json
import os

from eth_typing import ChecksumAddress, Address
from solcx import install_solc, set_solc_version, compile_files
from web3 import Web3, AsyncHTTPProvider, WebsocketProvider, HTTPProvider
from web3.eth import AsyncEth
from web3.middleware import geth_poa_middleware

from settings import HTTP_URI, WEB_SOCKET_URI
from utility import get_credentials


class Web3Client:
    def __init__(self, blockchain: str):
        self.w3_async = Web3(
            AsyncHTTPProvider(HTTP_URI),
            modules={
                'eth': AsyncEth
            },
            middlewares=[]  # geth_poa_middleware not supported yet
        )

        if blockchain == 'polygon':
            self.w3 = Web3(HTTPProvider(HTTP_URI))
        else:
            self.w3 = Web3(WebsocketProvider(WEB_SOCKET_URI))
        # TODO: check middleware with HTTP method
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # TODO: review, use @property instead of get methods
    def get_w3(self):
        return self.w3

    def get_w3_async(self):
        return self.w3_async

    def get_contract_address(self) -> {}:
        summary = []
        _, private_keys = get_credentials('polygon')
        contract_names = ['Migrations.sol', 'FileDigestOracle.sol', 'Factory.sol']

        it = iter(private_keys)
        for pk_0, pk_1, pk_2 in zip(it, it, it):
            contract_addresses = []
            for contract in contract_names:
                pk = pk_2 if contract == contract_names[1] else pk_0

                if contract != contract_names[0]:
                    contract_addresses.append(self.__deploy_contract(contract, pk))

            summary.append({
                # 'contract_addresses': contract_addresses,
                'contracts': {
                    contract_names[1]: contract_addresses[0],
                    contract_names[2]: contract_addresses[1]
                },
                'private_keys': [pk_0, pk_1, pk_2]
            })

        return summary

    def pks_to_addresses(self, pks: []) -> []:
        addresses = []
        for pk in pks:
            addresses.append(
                self.w3.eth.account.privateKeyToAccount(pk).address
            )
        return addresses if len(addresses) > 1 else addresses[0]

    def __deploy_contract(self, filename: str, pk: Address) -> ChecksumAddress:
        old_cwd = os.getcwd()
        filename_no_ext = filename.split('.')[0]
        key = f'{filename}:{filename_no_ext}'

        # TODO: check version and install only if there isn't
        install_solc('0.8.9')
        set_solc_version('0.8.9')

        os.chdir('../contracts')
        compiled_sol = compile_files(
            filename,
            output_values=['abi', 'bin']
        )

        os.chdir('../build/contracts')
        with open(f'{filename_no_ext}.json', 'w') as file:
            json.dump(compiled_sol[key], file, indent=4)

        # TODO: review
        if 'Factory' in filename:
            with open('CloudSLA.json', 'w') as file:
                json.dump(compiled_sol['CloudSLA.sol:CloudSLA'], file, indent=4)

        os.chdir(old_cwd)

        bytecode = compiled_sol[key]['bin']
        abi = compiled_sol[key]['abi']

        self.w3.eth.default_account = self.pks_to_addresses([pk])

        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        tx = Contract.constructor().buildTransaction({
            'gasPrice': 0,
            'from': self.w3.eth.default_account,
            'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account)
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        contract = self.w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )

        return contract.address