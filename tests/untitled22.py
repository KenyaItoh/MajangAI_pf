# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 12:30:45 2020

@author: sddbb
"""

#チー
a = 0b1110111000111
#b = 0b1111110000000000
b = 0xFC00
c = (a&b) >> 10
d = c%3
t = int(c/3)

#ポン

a_p = 34411
b_p = 0xFE00
c_p = (a_p&b_p) >> 9
d_p = c_p%3

#加カン

#a_kk = 
b_kk = 0x0060

#暗槓

#a_ak = 0b10100000000000
a_ak = 11264
b_ak = 0xFF00

hai0 = (a_ak&b_ak) >> 8

hai0=(hai0&~3)+3

aaa = 0b00

print(bool(aaa))