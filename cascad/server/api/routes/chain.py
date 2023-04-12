from  flask import Flask
from flask import render_template, Blueprint
from web3 import Web3
from web3.middleware import geth_poa_middleware
from cascad.settings import  CCHAIN_RPC

w3 = Web3(Web3.HTTPProvider(CCHAIN_RPC))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

chain = Blueprint('chain', __name__ , template_folder='templates', static_folder='static')

@chain.route('/chain')
def index():
    latest_block_number = w3.eth.get_block('latest').number
    # return render(request, 'chain/index.html', {'block_numbers': range(1, latest_block_number + 1)})
    block_numbers = range(latest_block_number - 9, latest_block_number + 1)
    blocks = [__get_block(block_number) for block_number in block_numbers]
    latest_block = w3.eth.get_block('latest')

    latest_block_number = latest_block.number
    difficulty = latest_block.difficulty
    block_gas_limit = latest_block.gasLimit
    block_gas_used = latest_block.gasUsed
    block_hash = latest_block.hash.hex()
    parent_hash = latest_block.parentHash.hex()
    miner = w3.eth.get_block(latest_block.number - 1).miner
    hashrate = w3.eth.hashrate
    total_difficulty = w3.eth.get_block(0).difficulty

    return render_template('chain/index.html', blocks=blocks,latest_block_number=latest_block_number,
                                            difficulty=difficulty,
                                            block_gas_limit=block_gas_limit,
                                            block_gas_used=block_gas_used,
                                            hashrate=hashrate,
                                            miner=miner,
                                            total_difficulty=total_difficulty)


def __get_block(block_number):
    return w3.eth.get_block(block_number)


@chain.route('/chain/block/<int:block_number>')
def block(block_number):
    block = w3.eth.getBlock(block_number)
    # 获取区块中的所有交易
    transactions = block.transactions
    # 渲染模板
    return render_template('chain/block.html', block=block, transactions=transactions)