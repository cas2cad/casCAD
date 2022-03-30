import sys
import os
sys.path.append('..')
sys.path.append('.')
import unittest
from cascad.experiment.token_sender import ERC20TokenWorld

class TestAgent(unittest.TestCase):

    def test_token_world(self):
        erc20_token_world  = ERC20TokenWorld(0.5, 10, 10)
        print(erc20_token_world.next_id())
        erc20_token_world.run()

        
if __name__ == '__main__':
    unittest.main()
    pass