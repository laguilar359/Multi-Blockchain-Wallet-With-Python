{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Imports\n",
    "import subprocess\n",
    "import json\n",
    "import os\n",
    "\n",
    "from constants import BTC, BTCTEST, ETH\n",
    "from pprint import pprint\n",
    "\n",
    "from bit import PrivateKeyTestnet\n",
    "from bit.network import NetworkAPI\n",
    "\n",
    "from web3 import Web3, middleware, Account\n",
    "from web3.gas_strategies.time_based import medium_gas_price_strategy\n",
    "from web3.middleware import geth_poa_middleware"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Connect Web3 to interact with local Ethereum node (luisnet4)\n",
    "w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER', 'http://localhost:8545')))\n",
    "w3 = Web3(Web3.HTTPProvider(\"http://127.0.0.1:8545\"))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "7163"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Call latest block number in the local Blockchain (luisnet4)\n",
    "w3.eth.blockNumber"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "904625697166532776746648320380374280053671755200316676551260884061821325312"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Get current balance from luisnet4 node1 account\n",
    "w3.eth.getBalance(\"0x4D7aB3B4b8100A3C001932DA5030Fc5Ce04D3672\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "3028"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Get current balance from wallet's first address\n",
    "#w3.eth.getBalance(\"0x3De0A2fD4A90f9A160ebb2B8711192D1F0eB339D\")\n",
    "w3.eth.getBalance(\"0xd171309493a7Cfa5f92011d8E5f29Cf746959276\")\n",
    "#w3.eth.getBalance(\"0x24C41a1f343162817F2EebDBcD71a695Df0f930d\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Navigate to parent folder where 'wallet' directory is located\n",
    "os.chdir(r'/Users/luisaguilar/Fintech_Bootcamp/wallet')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set Ethereum gas strategy\n",
    "w3.eth.setGasPriceStrategy(medium_gas_price_strategy)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set mnemonic phrase as an environment variable\n",
    "mnemonic = os.getenv('MNEMONIC', 'three coach coin blade parade spray keen brick athlete clerk stadium blur art south claw')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use the 'subprocess' library to call the './derive' script.\n",
    "# Set the 'wait()' function to ensure it properly waits for the process.\n",
    "# Pass the following flags into the shell command as variables: 'mnemonic', 'coin', and 'numderive'\n",
    "# Set format to JSON and parse output using json.loads(output)\n",
    "\n",
    "#Create 'coin', 'mnemonic', and 'depth' objects. Set 'depth' to derive 3 child keys.\n",
    "coin = 'ETH'\n",
    "mnemonic = 'mnemonic'\n",
    "depth = '3'\n",
    "\n",
    "command = './derive -g --mnemonic=\"mnemonic\" -- cols=path,address --format=json --numderive={depth} --coin={coin}'\n",
    "\n",
    "p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)\n",
    "\n",
    "(output, err) = p.communicate()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Wrap all previous parameters into a function \"derive_wallets\"\n",
    "\n",
    "def derive_wallets(coin=BTC, mnemonic=mnemonic, depth=3):\n",
    "    command = f'php derive -g --mnemonic=\"{mnemonic}\" --coin={coin}  --numderive={depth} --format=json'\n",
    "\n",
    "    p = subprocess.Popen(\n",
    "        command,\n",
    "        stdout=subprocess.PIPE,\n",
    "        shell=True)\n",
    "    (output, err) = p.communicate()\n",
    "    p_status = p.wait()\n",
    "    return json.loads(output)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create an object called 'coins' that derives the ETH and BTCTEST wallets with the 'derive_wallets' function.\n",
    "\n",
    "coins = {\n",
    "    ETH: derive_wallets(coin=ETH),\n",
    "    BTCTEST: derive_wallets(coin=BTCTEST),\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'btc-test': [{'address': 'mtgb9hthmFpY1zidrYmZ24eTF87aBA147h',\n",
      "               'index': 0,\n",
      "               'path': \"m/44'/1'/0'/0/0\",\n",
      "               'privkey': 'cVAgDoahzo5Ucdv8ioxxubvmE6LfU3ZQgJ21UvY4eC1xi6WkvnXe',\n",
      "               'pubkey': '0339b281b12687c70a024ef409229b55d404533b4e9a475dc9d3883c0172913fb6',\n",
      "               'pubkeyhash': '906c250da82c2bd3edf9bcbbbb29f2188065f9d2',\n",
      "               'xprv': 'tprv8kmimjp9GYq9EvcrxozEhxzk9jGwaC73BSiy3ATqwwikM4YgH7685zQLzX7xzXAmhXxf5LZbpbqtSGX3fcNFbfVJdxuEYPrA5tDRRQgwPRm',\n",
      "               'xpub': 'tpubDHTkv9rPQvWp8PeerTeq7NeriknsjXHwkkKkKgW9NDX9BYoSuVuiGV2DAejLNv85zVm31akUTVk6Z8MyhECbWDzQ3Qir4GoRCXfBgKk8GxA'},\n",
      "              {'address': 'mxwSU31v1NtbUi6Pc5bN9BgmmAGw13JdvX',\n",
      "               'index': 1,\n",
      "               'path': \"m/44'/1'/0'/0/1\",\n",
      "               'privkey': 'cRG5vrAkkq3ZkTmT2mmqCgbxd8niBdXx3ocDMd1771oSzJDvqXiC',\n",
      "               'pubkey': '02f4468eae06b195a4f83cc63d680d015d512af60288977e0283fd4299bfcde24b',\n",
      "               'pubkeyhash': 'bf1ba366dd65a4824c22f497bbff1fae89007841',\n",
      "               'xprv': 'tprv8kmimjp9GYq9FvSyaAKU2MY38GBpiMHEsjgMtnLaMhyZQPzAiEM6ZTC8z9vdTsJVRQDcoCvLeWEHiPWWLpiGMjoYcffLhXJXNbJawYjKTof',\n",
      "               'xpub': 'tpubDHTkv9rPQvWp9PUmToz4RmC9hHhksgU9T3H9BJNsmymxEtEwLdAgjwp1AHtm7kbkbHvsC3zA3cjHi6DAFtGCvFMgY961mo7mg5ABBu21126'},\n",
      "              {'address': 'n2QTqdWK96XyJ7o8LXqoCjNbmtrFNFbNb6',\n",
      "               'index': 2,\n",
      "               'path': \"m/44'/1'/0'/0/2\",\n",
      "               'privkey': 'cUMUWn4yukMK41LpebaCmnbH26XCQn9EDoSK753FxSNxQC77i5TU',\n",
      "               'pubkey': '03c486d31c700f8342f6dac13fffaab4d44c492637042659ae2922846c89077101',\n",
      "               'pubkeyhash': 'e5206464e15c29f28f54678782a909be5954f6cc',\n",
      "               'xprv': 'tprv8kmimjp9GYq9JExZDMjKjYhzHGQwQHVmMh2cRP5BLMAgCbw7fNgDssZJCujBDau2t2PEzddu8QApnrgnhzktN4LT8BXEM7HDSrxMHM6XasY',\n",
      "               'xpub': 'tpubDHTkv9rPQvWpBhzM71Pv8xN6rHvsZcgfvzdPhu7Ukcy536BtHmVp4NBAP4aP5Laycoz7Shaprf1xgAyBrZdGuoDWUFcrPc3UuiqRTBcQnxt'}],\n",
      " 'eth': [{'address': '0x3De0A2fD4A90f9A160ebb2B8711192D1F0eB339D',\n",
      "          'index': 0,\n",
      "          'path': \"m/44'/60'/0'/0/0\",\n",
      "          'privkey': '0x82d63adc8be924a92ef77c6e3286c4e80eaebad63ba2b91c27801a62ba2f9410',\n",
      "          'pubkey': '02c93d99b9686cabed081f1eb262b81a435ae2816ba940e0fea550a36603d8077b',\n",
      "          'pubkeyhash': 'a90e4da9a141168d3e0ac3821015190a79df729c',\n",
      "          'xprv': 'xprvA3W3uzhjas8mpZrqS7oW9ar2SWxLGhwcPFT7S2j7VM8e9PbaYcfSJo4aDdsjd7yi9iPcKkvxg7TzmeNJniz84Y4rYgTaarwiMk66gZNwj3P',\n",
      "          'xpub': 'xpub6GVQKWEdREh533wJY9LWWinkzYnpgAfTkUNiER8j3gfd2Bvj69ygrbP44uSWSEu9BwzQ2mboHQp17puXxT3y9xnXCt256vtjkzV2caX1xeT'},\n",
      "         {'address': '0xc5557310a53b90f18E926431B1896c29Df0dcc1a',\n",
      "          'index': 1,\n",
      "          'path': \"m/44'/60'/0'/0/1\",\n",
      "          'privkey': '0xf0c147a367c5732f750e0dc072540f71ec3e3a87fafee9e7516982861e9e259e',\n",
      "          'pubkey': '0299b67384c634d60ac57d9efc57a93b3a2d87b9eb63e3025652de882c269f2480',\n",
      "          'pubkeyhash': '8703eefc2cdcf91b844d7ec8090d2e89d092de58',\n",
      "          'xprv': 'xprvA3W3uzhjas8msDSBJH94x7mqj53hfhCweGzWNRqsHamAi3MrZh4cDT4VywH5UH7UboqUbVazKeEn9gLy7TgeMbtWSuyYk852kBG75GZmB4r',\n",
      "          'xpub': 'xpub6GVQKWEdREh55hWeQJg5KFiaH6tC59vo1Vv7ApFUqvJ9aqh17ENrmFNyqBeWXxBLL8hxPeeUw4A8HfovbNetZcGkNj6p1VoJiDt4UJ3L9RU'},\n",
      "         {'address': '0x926841419b49910D80fCEa75d587BE3aefFf560e',\n",
      "          'index': 2,\n",
      "          'path': \"m/44'/60'/0'/0/2\",\n",
      "          'privkey': '0x356c8dd425cf9714114bf73751c13d1ad34f4012e2ac37e564b0aaee238a0d2a',\n",
      "          'pubkey': '02fb003f8b9fd2e765b5c64b7f47832bc46ff818807e7903262c03a29d2b983f6a',\n",
      "          'pubkeyhash': '53c13c213c11034e676536944ec4f2cb5fb0b3c0',\n",
      "          'xprv': 'xprvA3W3uzhjas8mvbJ4eX1qKPXK7osvsQXSezDFvPW3dEpbJZ35xaJXxBdpPcrXDrqror7a2McmYr5HbL5Xiag834qfBkvhY5YvLKe3MPxFbch',\n",
      "          'xpub': 'xpub6GVQKWEdREh595NXkYYqgXU3fqiRGsFJ2D8rimufBaMaBMNEW7cnVyxJEuPJW5HNqmbaVUfxVVhvPxd4SmjitFxyEY2YJHeF2GXfz5Q8yRb'}]}\n"
     ]
    }
   ],
   "source": [
    "pprint(coins)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'cRG5vrAkkq3ZkTmT2mmqCgbxd8niBdXx3ocDMd1771oSzJDvqXiC'"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Select child accounts using the 'coins' object: coins['cointype'][index]['privkey']\n",
    "# Use child key addresses to send money\n",
    "\n",
    "coins['btc-test'][1]['privkey']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a function {priv_key_to_account} to convert the 'privkey' string in a child key to an account object that bit or web3.py can use to transact\n",
    "# This function needs the following parameters: 'coin' (from constants.py), 'priv_key' (to pass the 'privkey' string), \n",
    "\n",
    "def priv_key_to_account(coin, priv_key):\n",
    "    # Check the coin.\n",
    "    # For 'ETH' return 'Account.privateKeyToAccount(priv_key)' to return an account object from the private key string. \n",
    "    if coin == ETH:\n",
    "        return Account.privateKeyToAccount(priv_key)\n",
    "    # For 'BTCTEST' return 'PrivateKeyTestnet(priv_key)' to convert the private key string into a WIF object in Bitcoin format.\n",
    "    if coin == BTCTEST:\n",
    "        return PrivateKeyTestnet(priv_key)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a 'priv_key' object using the 'coins' object to pull the coin's 'privkey' address\n",
    "priv_key = coins['eth'][0]['privkey']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create an 'account' signers object for the 'ETH' 'privkey' using the 'priv_key_to_account' function.\n",
    "account = priv_key_to_account(ETH, priv_key)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<eth_account.signers.local.LocalAccount at 0x7fedcd03d290>"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# View the 'account' object\n",
    "account"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import 'Account' from 'eth_account' and create a new 'account_one' signers object for the 'ETH' 'privkey' using the 'Account.from_key' fuction.\n",
    "\n",
    "from eth_account import Account\n",
    "account_one = Account.from_key(priv_key)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<eth_account.signers.local.LocalAccount at 0x7fedcd043750>"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# View the 'account_one' object\n",
    "account_one"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0x3De0A2fD4A90f9A160ebb2B8711192D1F0eB339D\n"
     ]
    }
   ],
   "source": [
    "# Print the 'account' 'address'\n",
    "print(account.address)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0x3De0A2fD4A90f9A160ebb2B8711192D1F0eB339D\n"
     ]
    }
   ],
   "source": [
    "# Print the 'account_one' 'address' (should be the same)\n",
    "print(account_one.address)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'ETH'"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# View the coin type\n",
    "coin"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "# State the 'amount' to send\n",
    "amount = 0.01"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "# state the 'to' recipient address\n",
    "to = \"0xd171309493a7Cfa5f92011d8E5f29Cf746959276\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Build a 'create_tx' to create a raw, unsigned transaction that contains all metadata needed to transact.\n",
    "# The function needs the following parameters: \n",
    "    # 'coin' (from constants.py), \n",
    "    # 'account' (object from priv_key_to_account), \n",
    "    # 'to' (recipient address), \n",
    "    # 'amount' (amount to send) \n",
    "\n",
    "def create_tx(account, recipient, amount):\n",
    "    gasEstimate = w3.eth.estimateGas(\n",
    "        {\"from\": account.address, \"to\": recipient, \"value\": amount}\n",
    "    )\n",
    "    return {\n",
    "        \"from\": account.address,\n",
    "        \"to\": recipient,\n",
    "        \"value\": amount,\n",
    "        \"gasPrice\": w3.eth.gasPrice,\n",
    "        \"gas\": gasEstimate,\n",
    "        \"nonce\": w3.eth.getTransactionCount(account.address),\n",
    "    }"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'0x2fdda731d83a911c6e2468aa39b12b5375c00099d3a98c8e060e4fb1bb0474b2'"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def send_tx(account, recipient, amount):\n",
    "    tx = create_tx(account, recipient, amount)\n",
    "    signed_tx = account.sign_transaction(tx)\n",
    "    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)\n",
    "    #print(result.hex())\n",
    "    return result.hex()\n",
    "\n",
    "send_tx(account_one, to , 1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "private_key = coins['eth'][0]['privkey']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "account_one = Account.from_key(private_key)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<eth_account.signers.local.LocalAccount at 0x7fedcd02f450>"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "account_one "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
