#!/user/bin/env python3
# -i- coding: UTF-8 -*-i-
import readverilog
from readverilog import Netlist
import dataprocess
import writefile
import v2cnf
import itertools
import copy
import satattack
import os
import re
import LL_frame as llframe
import antisat


RLL = 1
ANTISAT = 2


def outputsat(modulename1, modulename2, lltype):
    circuit1 = Netlist(modulename1)
    circuit2 = Netlist(modulename2)
    inputlist, outputlist, wirelist, gatelist, gatedata = dataprocess.uniprocess(circuit1, circuit2)
    writefile.uniwrite('resultfiles/sat' + modulename1 + '.v', inputlist, outputlist, wirelist, gatelist)

    v2cnf.unicnf(circuit1, circuit2, wirelist, gatedata, 'resultfiles/sat' + modulename1 + '.cnf')

    #################################################################################
    keylist, inputlist = v2cnf.findkey(ori=circuit1.inputlist, key=circuit2.inputlist)
    rightkey, dipno = satattack.diploop(filename1='resultfiles/sat'+modulename1+'.cnf',
                                        inputlen=len(inputlist), keylen=len(keylist), lltype=lltype)
    print('right key:')
    print(rightkey)
    print('dipno: ')
    print(dipno)
    return rightkey, dipno


def compare(filename1, filename2, filename3):
    input_symbol, output_symbol, wire_symbol, gate_symbol, failflag = llframe.unill('user_in.txt',
                                                                          'verilogfiles/'+filename1+'.v',
                                                                          'verilogfiles/'+filename2+'.v')

    while failflag:
        input_symbol, output_symbol, wire_symbol, gate_symbol, failflag = llframe.unill('user_in.txt',
                                                                                        'verilogfiles/' + filename1 + '.v',
                                                                                        'verilogfiles/' + filename2 + '.v')

    antisat.unill('user_in.txt', 'verilogfiles/'+filename1 + '.v',
                  'verilogfiles/'+filename3 + '.v', input_symbol, output_symbol, wire_symbol,
                  gate_symbol)

    rightkey1, dipno1 = outputsat(filename1, filename2, RLL)
    os.remove('resultfiles/percent.log')
    os.remove('resultfiles/result.cnf')
    os.remove('resultfiles/sat.log')
    os.remove('resultfiles/sat'+filename1+'.cnf')
    os.remove('resultfiles/sat'+filename1+'.v')
    os.remove('resultfiles/temp1.cnf')
    os.remove('verilogfiles/'+filename2+'.v')

    rightkey2, dipno2 = outputsat(filename1, filename3, ANTISAT)
    os.remove('resultfiles/percent.log')
    os.remove('resultfiles/result.cnf')
    os.remove('resultfiles/sat.log')
    os.remove('resultfiles/sat' + filename1 + '.cnf')
    os.remove('resultfiles/sat' + filename1 + '.v')
    os.remove('resultfiles/temp1.cnf')
    os.remove('verilogfiles/' + filename3 + '.v')

    with open('result.log', 'a+') as f:
        f.write(str(rightkey1)+'\n')
        f.write(str(dipno1)+'\n')
        f.write(str(rightkey2) + '\n')
        f.write(str(dipno2) + '\n')
    return dipno1, dipno2


# rllno, antisatno = 0, 0
# k = 1
# for _ in range(k):
#     d1, d2 = compare('c432', 'c432k', 'c432a')
#     rllno += d1
#     antisatno += d2
# print(rllno/k)
# print(antisatno/k)


def compare2(filename1, filename2, filename3):
    input_symbol, output_symbol, wire_symbol, gate_symbol, failflag = llframe.unill('user_in.txt',
                                                                          'verilogfiles/'+filename1+'.v',
                                                                          'verilogfiles/'+filename2+'.v')
    while failflag:
        input_symbol, output_symbol, wire_symbol, gate_symbol, failflag = llframe.unill('user_in.txt',
                                                                                        'verilogfiles/' + filename1 + '.v',
                                                                                        'verilogfiles/' + filename2 + '.v')
    antisat.unill('user_in.txt', 'verilogfiles/'+filename1 + '.v',
                  'verilogfiles/'+filename3 + '.v', input_symbol, output_symbol, wire_symbol,
                  gate_symbol)


compare2('c432', 'c432k', 'c432a')
