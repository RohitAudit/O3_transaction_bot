from web3 import Web3
import time

class TransactionBuilder:
    web3_eth:Web3
    account: None

    def __init__(self,url,private_key):
        self.web3_eth= Web3(Web3.HTTPProvider(url))
        self.web3_eth.eth.account.enable_unaudited_hdwallet_features()
        self.account = self.web3_eth.eth.account.from_key(private_key)

    def create_ERC20_tx(self, contract_address,address, value):
        """

        :param address:
        :param value:
        :return:
        """
        abi = [{
        "inputs": [
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "value",
          "type": "uint256"
        }
      ],
      "name": "transfer",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    }]
        erc20_contract = self.web3_eth.eth.contract(contract_address,abi=abi)
        return erc20_contract.functions.transfer(address,value).build_transaction({"gasPrice": Web3.to_wei("10", "gwei"), "gas": 1000000})


    def send_tx(self,tx):
        """

        :param tx:
        :return:
        """
        tx['from'] = self.account.address
        # self.eth_node.eth.call(tx)
        tx['nonce'] = self.web3_eth.eth.get_transaction_count(
            self.account.address)
        # if self.local:
        #     tx.pop('maxFeePerGas')
        signed_tx = self.web3_eth.eth.account.sign_transaction(
            tx, self.account.key)
        tx_hash = self.web3_eth.eth.send_raw_transaction(
            signed_tx.raw_transaction)
        time.sleep(30)
        tx_receipt = self.web3_eth.eth.wait_for_transaction_receipt(tx_hash)
        if tx_receipt.status == 1:
            print('TX successful')
            return True, tx_hash.hex()
        else:
            print('TX reverted')
            return False, tx_hash.hex()

if __name__ == '__main__':
    while True:
        tt = TransactionBuilder("","")
        account_new,mnemonic = tt.web3_eth.eth.account.create_with_mnemonic()
        print(account_new.address)
        print(Web3.to_wei("0.1","ether"))
        tx=tt.create_ERC20_tx("0x4E0f369514C9245a6650b828bF942B95996668C6",account_new.address,Web3.to_wei("0.1","ether"))
        tt.send_tx(tx)
        time.sleep(60)

