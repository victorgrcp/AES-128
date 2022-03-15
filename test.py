#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 15:15:30 2022

@author: victor
"""

from main import AES
import numpy as np

state = ['0xdb', '0xf2', '0x1','0xc6', 
         '0x13', '0xa', '0x1', '0xc6', 
         '0x53', '0x22', '0x1', '0xc6', 
         '0x45', '0x5c', '0x1', '0xc6']

key = '0000000000000000'


def test_mixCol(aes):
    out = ['0x8e', '0x4d', '0xa1', '0xbc',
           '0x9f', '0xdc', '0x58', '0x9d',
           '0x1', '0x1', '0x1', '0x1',
           '0xc6', '0xc6', '0xc6', '0xc6']
    print('\nTest mixCol')
    aes.mix_columns()
    for i in range(4):
        col = aes.state[0+i:13+i:4]
        print(f'{i+1} Fila: {col == out[4*i:4*(i+1)]}')

def test_subByte(aes):
    out = ['0xb9','0x89','0x7c','0xb4',
           '0x7d','0x67','0x7c','0xb4',
           '0xed','0x93','0x7c','0xb4',
           '0x6e','0x4a','0x7c','0xb4']
    aes.sub_bytes()
    print('\nTest SubBytes')
    for i in range(4):
        print( aes.state[4*i:4*(1+i)] == out[4*i:4*(1+i)])
    
if __name__ == '__main__':
    
    aes = AES(state, key, inHex=True)
    
    test_subByte(aes)
    aes.state = np.array(state)
    
    test_mixCol(aes)
    
    aes.muestra_state()