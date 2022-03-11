#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:04:19 2022

@author: victor
"""

import numpy as np

class AES:
    
    def __init__(self, m, key):
        self.m = m
        self.key = np.matrix([hex(ord(c)) for c in key]).reshape(4,4)
        self.state = np.matrix([hex(ord(c)) for c in m]).reshape(4,4)
        self.keys = np.zeros((10,4,4))
        
    def expand_key(self):
        pass
    
    def add_round_key(self, nround):
        
        for i in range(4):
            for j in range(4):
                self.state[i,j] = hex(int(self.state[i,j], 0) ^ int(self.keys[nround,i,j], 0))
        
    
    def sub_bytes(self):
        pass
    
    def shift_rows(self):
        # Shift right the row i, i times, from i=1..n
        # Where n is the dim of the matrix, in this case n=4
        for i in range(1,4):
            self.state[i] = np.roll(self.state[i], i, axis=1)
    
    def mix_columns(self):
        pass
    
    def decode_state(self):
        return
    
    def encrypt(self):
        
        self.expand_key()
        self.add_round_key(0)
        
        for i in range(1,9):
            self.sub_bytes()
            self.shift_rows()
            self.mix_columns()
            self.add_round_key(i)
        
        self.sub_bytes()
        self.shift_rows()
        self.add_round_key(9)
        
        return self.decode_state()