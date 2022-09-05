DUET = 'DUET'
USDT = 'USDT'
NAS = 'NAS'
BTC = 'BTC'
ZUSD = 'ZUSD'
ZBTC = 'ZBTC'
ZNAS = 'ZNAS'
REI = 'REI'
STAKE_REWARD = 'STAKE_REWARD'
FARM_REWARD = 'FARM_REWARD'
DAI = 'DAI'
GNO = 'GNO'

DUET_USDT = DUET + '_' + USDT
ZUSD_USDT = ZUSD + '_' + USDT
ZBTC_ZUSD = ZBTC + '_' + ZUSD
ZNAS_ZUSD = ZNAS + '_' + ZUSD

FRACTION = 'fraction' # how many fraction of asset will be process
MAX = 'max' #  refer to all of the token
LAST = 'last' # refer to last generated tokens

MINT1 = 'mint'
MINT2 = 'mint2'
MINT3 = 'mint3'
MINT4 = 'mint4'
SWAP1 = 'swap'
SWAP2 = 'swap2'
STAKE = 'stake'
FARM = 'farm'
IDLE = 'idle'
REDEEM = 'redeem'
FRAMWITHDRAW = 'farm_wthdraw'
STAKEWITHDRAW = 'stake_withdraw'
SANDWICHATTACK = 'sandwich_attack'
ACTION = 'action'

# for spread
SWAP3 = 'swap3'
SWAP4 = 'swap4'

HOLDFOUNDER = 'HOLDFOUNDER'
SELLFOUNDER = 'SELLFOUNDER'
DUETHOLD = 'DUETHOLD'
DUETHOLDANDFARM = 'DUETHOLDANDFRAM'
DUETHOLDANDSTAKE = 'DUETHOLDANDSTAKE'
DASSETHOLD = 'DASSETHOLD'
DASSETHOLDANDFARM = 'DASSETHOLDANDFARM'
SHORTFARMARBITRAGE = 'SHORTFARMARBITRAGE'
SPREAD = 'SPREAD'
BULLISHDUET = 'BULLISHDUET'
BULLISHDASSET = 'BULLISHDASSET'
BEARISHDUET = 'BEARISHDUET'
BEARISHDASSET = 'BEARISHDASSET'
TRADER = 'TRADER'
ALL = 'all'


# for uniswap
PRICES = 'prices'
VALUE = 'value'
CHANGE = 'change'
HISTORY = 'history'
TRADINGVALUE = 'trade_values'
HIGH = 'high'
LOW = 'low'
APY_WITH_REWARD = 'apy_with_reward'
APR_WITH_REWARD = 'apr_with_reward'
UNISWAP_FARM_REWARD = 'uniswap_farm_reward'
LP_AMOUNT = 'lp_amount'
# DAY_7_PRICE = '7_day_price'
# DAY_30_PRICE = '30_day_price'

# for amm
TRADES = 'trades'
LP = 'lp'
FEES = 'fees'
FEEVLUE = 'fees_value'
POOL = 'pool'
APY = 'apy'
APR = 'apr'
POOLVALUE = 'pool_value'
FEEVALUE = 'fee_value'


# for stake
STAKE = 'st'
TOTAL = 'total'
STAKE_TOTAL_REWARD = 'stake_total_reward'
STAKE_APY = 'stake_apy'
STAKE_APR = 'stake_apr'


# models
MINTMODEL = 'mint_model'
REDEEMMODEL = 'redeem_model'
SWAPMODEL = 'swap_model'
FARMINGMODEL = 'farming_model'
STAKINGMODEL = 'staking_model'


# mint redeem
BURNED = 'burned'
MINTED = 'minted'
BURNEDVALUE = 'burned_value'
MINTEDVALUE = 'minted_value'
TOTALBURNED = 'total_burned'
TOTALMINTED = 'total_minted'
TOTALBURNEDVALUE = 'total_burned_value'
TOTALMINTEDVALUE = 'total_minted_value'
TAX = 'tax'
EXPECEDMINTRATE  = 'expected_minted_rate'
EXPECTEDREDEEMRATE = 'expected_redeem_rate'
TAXRATE = 'tax_rate'
THRESHOLD = 'threshold'

# bockchain
TOTALTRAD = 'total_trad'
TRADS = 'trads'

# for omen
PROPOSAL = 'proposal'
MARKET = 'market'
YES_TOKEN = 'yes_token'
NO_TOKEN = 'no_token'
ACCEPT_TOKEN = 'accept_token'

# for vote
VOTE_YES = 'vote_yes'
VOTE_NO = 'vote_no'
VOTE_CONDITION = 'vote_condition'