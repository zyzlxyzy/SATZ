#!/user/bin/env python3
# -i- coding: UTF-8 -*-i-

import re
import random
import copy
# 验证完成


class Netlist():

    def __init__(self, name):
        self.name = name
        self.inputlist, self.outputlist, self.wirelist, self.gatelist\
            , self.gatedata = Netlist.uni_net(self)
        self.newoutput, self.newwire, self.newgatedata = Netlist.renamelist(self)

    # return module_symbol, i1 + 1
    def read_module(self):
        module_symbol = []
        with open('verilogfiles/'+self.name+'.v', 'r') as f1:
            for i1, line in enumerate(f1):
                line_ele = re.split('\W+', line)
                # line_ele是一个list
                # 比如['module', 'c7552', 'N1', 'N5', 'N9', 'N12', 'N15', 'N18', 'N23', 'N26', 'N29', 'N32', '']
                # 因为其中可能会有''所以之后的判断中要注意''的情况

                if re.match('^//', line):
                    print('comment')
                    pass

                elif re.match('^module', line):
                    print('module start')
                    for e1, ele in enumerate(line_ele):
                        if (e1 == 0) or (e1 == 1) or (ele == ''):
                            # 为什么排除第0个和第1个元素呢
                            # 因为第0个是'module'；第1个是module名，如'c7552'
                            pass
                        else:
                            module_symbol.append(ele)
                    if re.match('.*;$', line):
                        print('module finish')
                        break
                elif re.match('.*', line):
                    for ele in line_ele:
                        if ele == '':
                            pass
                        else:
                            module_symbol.append(ele)
                    if re.match('.*;$', line):
                        print('module finish')
                        break
                    else:
                        pass
                else:
                    print('empty')
                    pass

        return module_symbol, i1 + 1

    # iow_symbol, read_line + 1
    def read_iow(self, ln, iow):
        iow_symbol = []

        with open('verilogfiles/'+self.name+'.v', 'r') as f1:
            for read_line, line in enumerate(f1):
                line_ele = re.split('\W+', line)
                if read_line < ln:
                    pass
                elif re.match('^//', line):
                    print('comment')
                    pass

                elif re.match('^'+iow, line):
                    print(iow+' start')
                    for ele in line_ele:
                        if (ele == iow) or (ele == ''):
                            pass
                        else:
                            iow_symbol.append(ele)
                    if re.match('.*;$', line):
                        print(iow+' finished')
                        break
                elif re.match('.*', line):
                    for ele in line_ele:
                        if ele == '':
                            pass
                        else:
                            iow_symbol.append(ele)
                    if re.match('.*;$', line):
                        print(iow+' finished')
                        break
                    else:
                        pass
                else:
                    print('empty')
                    pass

        return iow_symbol, read_line + 1

    # return gate_symbol, gate_data
    def read_gate(self, ln):
        gate_symbol = []
        gate_data = []
        gate_temp = []

        with open('verilogfiles/'+self.name+'.v', 'r') as f:
            for i, line in enumerate(f):
                line_ele = re.split('\W+', line)
                if i < ln:
                    pass
                elif re.match('^endmodule', line):
                    print('read over')
                    break
                elif re.match('^[a-zA-Z]', line):
                    gate_temp1 = []
                    gate_symbol.append(line)
                    for ele in line_ele:
                        if ele == '':
                            pass
                        else:
                            gate_temp.append(ele)

                    gate_temp1.append(gate_temp[0])
                    gate_temp1.append(gate_temp[1])
                    gate_temp1.append(gate_temp[2])
                    gate_temp1.append([])
                    for g1 in range(3, len(gate_temp)):
                        gate_temp1[3].append(gate_temp[g1])
                    gate_data.append(gate_temp1)
                    gate_temp = []
        return gate_symbol, gate_data

    # return inputlist, outputlist, wirelist, gatelist, gatedata
    def uni_net(self):
        modulelist, l1 = Netlist.read_module(self)
        inputlist, l2 = Netlist.read_iow(self, l1, 'input')
        outputlist, l3 = Netlist.read_iow(self, l2, 'output')
        wirelist, l4 = Netlist.read_iow(self, l3, 'wire')
        gatelist, gatedata = Netlist.read_gate(self, l4)

        return inputlist, outputlist, wirelist, gatelist, gatedata

    # return newoutput, newwire, newgatedata
    def renamelist(self):
        newoutput, newwire, newgatedata = [], [], []
        for o1 in self.outputlist:
            newoutput.append('LL'+o1)
        for w1 in self.wirelist:
            newwire.append('LL'+w1)
        for g1 in self.gatedata:
            inputs = []
            for gg1 in g1[3]:
                if gg1 in self.inputlist:
                    inputs.append(gg1)
                else:
                    inputs.append('LL'+gg1)
            newgatedata.append([g1[0], 'LL'+g1[1], 'LL'+g1[2], inputs])
        return newoutput, newwire, newgatedata


def findkeygate(orilist, addkeylist):
    keylist = []
    for a1 in addkeylist:
        if a1 not in orilist:
            keylist.append(a1)
    return keylist
















