#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import subprocess
import json
import os

from constants import BTC, BTCTEST, ETH
from pprint import pprint

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware


# In[2]:


# Connect Web3 to interact with local Ethereum node (luisnet4)
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER', 'http://localhost:8545')))
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


# In[3]:


# Call latest block number in the local Blockchain (luisnet4)
w3.eth.blockNumber


# In[4]:


# Get current balance from luisnet4 node1 account
w3.eth.getBalance("0x4D7aB3B4b8100A3C001932DA5030Fc5Ce04D3672")


# In[36]:


# Get current balance from wallet's first address
#w3.eth.getBalance("0x3De0A2fD4A90f9A160ebb2B8711192D1F0eB339D")
w3.eth.getBalance("0xd171309493a7Cfa5f92011d8E5f29Cf746959276")
#w3.eth.getBalance("0x24C41a1f343162817F2EebDBcD71a695Df0f930d")


# In[6]:


# Navigate to parent folder where 'wallet' directory is located
os.chdir(r'/Users/luisaguilar/Fintech_Bootcamp/wallet')


# In[7]:


# Set Ethereum gas strategy
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)


# In[8]:


# Set mnemonic phrase as an environment variable
mnemonic = os.getenv('MNEMONIC', 'three coach coin blade parade spray keen brick athlete clerk stadium blur art south claw')


# In[10]:


# Use the 'subprocess' library to call the './derive' script.
# Set the 'wait()' function to ensure it properly waits for the process.
# Pass the following flags into the shell command as variables: 'mnemonic', 'coin', and 'numderive'
# Set format to JSON and parse output using json.loads(output)

#Create 'coin', 'mnemonic', and 'depth' objects. Set 'depth' to derive 3 child keys.
coin = 'ETH'
mnemonic = 'mnemonic'
depth = '3'

command = './derive -g --mnemonic="mnemonic" -- cols=path,address --format=json --numderive={depth} --coin={coin}'

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

(output, err) = p.communicate()


# In[11]:


# Wrap all previous parameters into a function "derive_wallets"

def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):
    command = f'php derive -g --mnemonic="{mnemonic}" --coin={coin}  --numderive={depth} --format=json'

    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# In[12]:


# Create an object called 'coins' that derives the ETH and BTCTEST wallets with the 'derive_wallets' function.

coins = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST),
}


# In[13]:


pprint(coins)


# In[14]:


# Select child accounts using the 'coins' object: coins['cointype'][index]['privkey']
# Use child key addresses to send money

coins['btc-test'][1]['privkey']


# In[15]:


# Create a function {priv_key_to_account} to convert the 'privkey' string in a child key to an account object that bit or web3.py can use to transact
# This function needs the following parameters: 'coin' (from constants.py), 'priv_key' (to pass the 'privkey' string), 

def priv_key_to_account(coin, priv_key):
    # Check the coin.
    # For 'ETH' return 'Account.privateKeyToAccount(priv_key)' to return an account object from the private key string. 
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    # For 'BTCTEST' return 'PrivateKeyTestnet(priv_key)' to convert the private key string into a WIF object in Bitcoin format.
    if coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


# In[16]:


# Create a 'priv_key' object using the 'coins' object to pull the coin's 'privkey' address
priv_key = coins['eth'][0]['privkey']


# In[17]:


# Create an 'account' signers object for the 'ETH' 'privkey' using the 'priv_key_to_account' function.
account = priv_key_to_account(ETH, priv_key)


# In[18]:


# View the 'account' object
account


# In[19]:


# Import 'Account' from 'eth_account' and create a new 'account_one' signers object for the 'ETH' 'privkey' using the 'Account.from_key' fuction.

from eth_account import Account
account_one = Account.from_key(priv_key)


# In[20]:


# View the 'account_one' object
account_one


# In[21]:


# Print the 'account' 'address'
print(account.address)


# In[22]:


# Print the 'account_one' 'address' (should be the same)
print(account_one.address)


# In[23]:


# View the coin type
coin


# In[24]:


# State the 'amount' to send
amount = 0.01


# In[25]:


# state the 'to' recipient address
to = "0xd171309493a7Cfa5f92011d8E5f29Cf746959276"


# In[26]:


# Build a 'create_tx' to create a raw, unsigned transaction that contains all metadata needed to transact.
# The function needs the following parameters: 
    # 'coin' (from constants.py), 
    # 'account' (object from priv_key_to_account), 
    # 'to' (recipient address), 
    # 'amount' (amount to send) 

def create_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }


# In[27]:


def send_tx(account, recipient, amount):
    tx = create_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()


# In[28]:


private_key = coins['eth'][0]['privkey']


# In[29]:


account_one = Account.from_key(private_key)


# In[30]:


account_one 


# In[35]:


send_tx(account_one, to, 3)


# In[ ]:





# In[ ]:




