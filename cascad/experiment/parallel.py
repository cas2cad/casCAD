import os
import shutil
import json


class ParallelExecutor(object):
    def __init__(self, actual_word, word_generator):
        self.actual_word = actual_word
        self.word_generator = word_generator

        
    def run(self):
        pass
