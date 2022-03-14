#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:04:19 2022

@author: victor
"""

import numpy as np

class AES:
    
    s_box = (
            0x63 ,0x7c ,0x77 ,0x7b ,0xf2 ,0x6b ,0x6f ,0xc5 ,0x30 ,0x01 ,0x67 ,0x2b ,0xfe ,0xd7 ,0xab ,0x76,
            0xca ,0x82 ,0xc9 ,0x7d ,0xfa ,0x59 ,0x47 ,0xf0 ,0xad ,0xd4 ,0xa2 ,0xaf ,0x9c ,0xa4 ,0x72 ,0xc0,
            0xb7 ,0xfd ,0x93 ,0x26 ,0x36 ,0x3f ,0xf7 ,0xcc ,0x34 ,0xa5 ,0xe5 ,0xf1 ,0x71 ,0xd8 ,0x31 ,0x15,
            0x04 ,0xc7 ,0x23 ,0xc3 ,0x18 ,0x96 ,0x05 ,0x9a ,0x07 ,0x12 ,0x80 ,0xe2 ,0xeb ,0x27 ,0xb2 ,0x75,
            0x09 ,0x83 ,0x2c ,0x1a ,0x1b ,0x6e ,0x5a ,0xa0 ,0x52 ,0x3b ,0xd6 ,0xb3 ,0x29 ,0xe3 ,0x2f ,0x84,
            0x53 ,0xd1 ,0x00 ,0xed ,0x20 ,0xfc ,0xb1 ,0x5b ,0x6a ,0xcb ,0xbe ,0x39 ,0x4a ,0x4c ,0x58 ,0xcf,
            0xd0 ,0xef ,0xaa ,0xfb ,0x43 ,0x4d ,0x33 ,0x85 ,0x45 ,0xf9 ,0x02 ,0x7f ,0x50 ,0x3c ,0x9f ,0xa8,
            0x51 ,0xa3 ,0x40 ,0x8f ,0x92 ,0x9d ,0x38 ,0xf5 ,0xbc ,0xb6 ,0xda ,0x21 ,0x10 ,0xff ,0xf3 ,0xd2,
            0xcd ,0x0c ,0x13 ,0xec ,0x5f ,0x97 ,0x44 ,0x17 ,0xc4 ,0xa7 ,0x7e ,0x3d ,0x64 ,0x5d ,0x19 ,0x73,
            0x60 ,0x81 ,0x4f ,0xdc ,0x22 ,0x2a ,0x90 ,0x88 ,0x46 ,0xee ,0xb8 ,0x14 ,0xde ,0x5e ,0x0b ,0xdb,
            0xe0 ,0x32 ,0x3a ,0x0a ,0x49 ,0x06 ,0x24 ,0x5c ,0xc2 ,0xd3 ,0xac ,0x62 ,0x91 ,0x95 ,0xe4 ,0x79,
            0xe7 ,0xc8 ,0x37 ,0x6d ,0x8d ,0xd5 ,0x4e ,0xa9 ,0x6c ,0x56 ,0xf4 ,0xea ,0x65 ,0x7a ,0xae ,0x08,
            0xba ,0x78 ,0x25 ,0x2e ,0x1c ,0xa6 ,0xb4 ,0xc6 ,0xe8 ,0xdd ,0x74 ,0x1f ,0x4b ,0xbd ,0x8b ,0x8a,
            0x70 ,0x3e ,0xb5 ,0x66 ,0x48 ,0x03 ,0xf6 ,0x0e ,0x61 ,0x35 ,0x57 ,0xb9 ,0x86 ,0xc1 ,0x1d ,0x9e,
            0xe1 ,0xf8 ,0x98 ,0x11 ,0x69 ,0xd9 ,0x8e ,0x94 ,0x9b ,0x1e ,0x87 ,0xe9 ,0xce ,0x55 ,0x28 ,0xdf,
            0x8c ,0xa1 ,0x89 ,0x0d ,0xbf ,0xe6 ,0x42 ,0x68 ,0x41 ,0x99 ,0x2d ,0x0f ,0xb0 ,0x54 ,0xbb ,0x16
    )
    
    r_con = (0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36)
    
    def __init__(self, m: str, key: str):
        self.m      = m
        self.c      = ''
        self.key    = np.array([hex(ord(c)) for c in key], dtype='<U4')
        self.state  = np.array([hex(ord(c)) for c in m], dtype='<U4')
        self.keys   = np.empty((10, 16), dtype='<U4')
        
    def expand_key(self):
        
        # Primera iteración usando la key original
        self.keys[0, 0]    = hex(int(self.key[0], 0)  ^ self.sub_byte(self.key[15]) ^ self.r_con[0])
        self.keys[0, 4]    = hex(int(self.key[4], 0)  ^ self.sub_byte(self.key[3]) ^ 0)
        self.keys[0, 8]    = hex(int(self.key[8], 0)  ^ self.sub_byte(self.key[7]) ^ 0)
        self.keys[0, 12]   = hex(int(self.key[12], 0) ^ self.sub_byte(self.key[11]) ^ 0)
        
        for i in range(1, 4):
            self.keys[0, i]      = hex(int(self.key[0 + i], 0)  ^ int(self.keys[0, 0 + i -1], 0))
            self.keys[0, i + 4]  = hex(int(self.key[4 + i], 0)  ^ int(self.keys[0, 4 + i -1], 0))
            self.keys[0, i + 8]  = hex(int(self.key[8 + i], 0)  ^ int(self.keys[0, 8 + i -1], 0))
            self.keys[0, i + 12] = hex(int(self.key[12 + i], 0) ^ int(self.keys[0, 12 + i -1], 0))
        
        # Siguientes iteraciones usando las keys generadas
        for nround in range(1, 10):
            self.keys[nround, 0]    = hex(int(self.keys[nround-1, 0], 0)  ^ self.sub_byte(self.keys[nround-1, 15]) ^ self.r_con[nround])
            self.keys[nround, 4]    = hex(int(self.keys[nround-1, 4], 0)  ^ self.sub_byte(self.keys[nround-1, 3]) ^ 0)
            self.keys[nround, 8]    = hex(int(self.keys[nround-1, 8], 0)  ^ self.sub_byte(self.keys[nround-1, 7]) ^ 0)
            self.keys[nround, 12]   = hex(int(self.keys[nround-1, 12], 0) ^ self.sub_byte(self.keys[nround-1, 11]) ^ 0)
            for i in range(1, 4):
                self.keys[nround, i]      = hex(int(self.keys[nround-1, i], 0)  ^ int(self.keys[nround, i -1], 0))
                self.keys[nround, i + 4]  = hex(int(self.keys[nround-1, 4 + i], 0)  ^ int(self.keys[nround, 4 + i -1], 0))
                self.keys[nround, i + 8]  = hex(int(self.keys[nround-1, 8 + i], 0)  ^ int(self.keys[nround, 8 + i -1], 0))
                self.keys[nround, i + 12] = hex(int(self.keys[nround-1, 12 + i], 0) ^ int(self.keys[nround, 12 + i -1], 0))
    
            
    def add_round_key(self, nround: int):
        for i in range(16):
            self.state[i] = hex(int(self.state[i], 0) ^ int(self.keys[nround, i], 0))
        
    
    def sub_byte(self, index: str):
        return self.s_box[ int(index, 0) ]
    
    def sub_bytes(self):
        # Sustitución de cada valor en hexadecimal por si correspondiente en la tabla de sustitución
        for i in range(16):
            self.state[i] = hex(self.s_box[ int(self.state[i], 0) ])

    def shift_rows(self):
        # Shift right the row i, i times, from i=1..n
        for i in range(1,4):
            self.state[i*4 : (1+i) * 4] = np.roll(self.state[i*4 : (1+i) * 4], i)
    
    def GMUL2(self, x: str):
        # Multiplicacion Galois por 2 
        b = int(x, 0)
        h = (b >> 7) & 1
        out = (b << 1) & 0xff # Haciendo un AND con 0xff, quitamos el bit que haya más a la izquierda del 8o bit
        out ^= h * 0x1b # XOR con 0 o 0x1B dependiendo si el bit más a la izquieda es 0 o 1
        return out
    
    def GMUL3(self, x: str):
        # La multiplicación x3 es simplemente Gmul2(x) XOR x
        return self.GMUL2(x) ^ int(x, 0)
    
    
    def mix_columns(self):
        # Ejecuta el módulo de MixColumns
        for i in range(4):
            
            a1 = hex(self.GMUL2(self.state[i]) ^ self.GMUL3(self.state[4 + i]) ^ int(self.state[8 + i], 0) ^ int(self.state[12 + i], 0))
            a2 = hex(int(self.state[i], 0) ^ self.GMUL2(self.state[4 + i]) ^ self.GMUL3(self.state[8 + i]) ^ int(self.state[12 + i], 0))
            a3 = hex(int(self.state[i], 0) ^ int(self.state[4 + i], 0) ^ self.GMUL2(self.state[8 + i]) ^ self.GMUL3(self.state[12 + i]))
            a4 = hex(self.GMUL3(self.state[i]) ^ int(self.state[4 + i], 0) ^ int(self.state[8 + i], 0) ^ self.GMUL2(self.state[12 + i]))
                
            self.state[i]       = a1
            self.state[4 + i]   = a2
            self.state[8 + i]   = a3
            self.state[12 + i]  = a4
                  
    
    def decode_state(self):
        c = ''
        for i in range(16):
            c += chr(int(self.state[i], 0))
        self.c = c
    
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
        
        self.decode_state()
        return self.c