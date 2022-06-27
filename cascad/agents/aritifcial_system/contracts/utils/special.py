    """Here are the special value in solidity
    In Solidity there are special variables and functions which always exist globally and are mainly used to provide information about the blockchain. 
    """

class MSG:
    """each call generate one msg
    """
    def __init__(self, data, sender, sig, value):
        self.data = data
        self.sender = sender
        self.sig = sig
        self.value = value

        
class Block:
    """Each block generate one block
    """
    def __init__(self, blockhash, basefee, chainid,coinbase, difficulty, gaslimit, number, timestamp):
        self.blockhash = blockhash
        self.basefee = basefee
        self.chainid = chainid
        self.coinbase = coinbase
        self.difficulty = difficulty
        self.gaslimit = gaslimit
        self.number = number
        self.timestamp = timestamp