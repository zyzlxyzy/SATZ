#!/user/bin/env python3
# -i- coding: UTF-8 -*-i-

import re
import random
import copy


# 1#####################################################################
def read_user(filename):
    user_in = [None] * 3
    with open(filename, 'r') as f:
        user_in[0] = (str(f.readline())).strip('\n')
        user_in[1] = int(f.readline())
        user_in[2] = list((str(f.readline()).strip('\n')))

    if len(user_in[2]) == user_in[1]:
        print('length fit')
    else:
        print('length not fit')
    return user_in
######################################################################


# 2#####################################################################
# output key input name list
def key_inputs(key_no):
    key_input_name = [None] * key_no
    for ki in range(key_no):
        key_input_name[ki] = str('keybit' + str(ki + 1))
    return key_input_name
######################################################################


# 3#####################################################################
# output key wire name list
def antisatwire(userin, outsymbol):
    wirelist = []
    layer1, layer2, layer3 = [], [], []
    for i1 in range(userin[1]):
        wirelist.append('layerone' + str(i1))
        layer1.append('layerone' + str(i1))
    wirelist.append('layertwo1')
    wirelist.append('layertwo2')
    layer2.append('layertwo1')
    layer2.append('layertwo2')
    wirelist.append('layerthree1')
    layer3.append('layerthree1')
    for i2 in outsymbol:
        wirelist.append(i2)

    return wirelist, layer1, layer2, layer3
######################################################################


# 6#####################################################################
def modi_module(filename1, filename2, module_name, input_symbol, key_input_name, output_symbol):
    module_symbol = []
    with open(filename1, 'r') as f1:
        for i1, line in enumerate(f1):
            print(i1, line)
            line_ele = re.split('\W+', line)
            if re.match('^//', line):
                print('comment')
                pass

            elif re.match('^module', line):
                print('module start')
                for e1, ele in enumerate(line_ele):
                    if (e1 == 0) or (e1 == 1) or (ele == ''):
                        pass
                    else:
                        module_symbol.append(ele)
            elif re.match('.*', line):
                for ele in line_ele:
                    if (ele == ''):
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

    print(input_symbol)
    with open(filename2, 'a+') as f2:
        print('module output opened successfully')
        i2 = 1
        f2.write('module ' + module_name + ' (')
        for l1 in input_symbol:
            if i2 == 1:
                f2.write(l1)
            elif (i2 > 9) and (i2 % 10 == 1):
                f2.write(',' + '\n' + l1)
            else:
                f2.write(',' + l1)
            i2 += 1
        f2.write(',' + '\n\n')

        newout = []
        for o1 in range(len(output_symbol)):
            newout.append('antisat' + output_symbol[o1])
        newout = key_input_name + newout
        print(newout)

        i3 = 1
        for l2 in newout:
            if i3 == 1:
                f2.write(l2)
            elif (i3 > 9) and (i3 % 10 == 1):
                f2.write(',' + '\n' + l2)
            else:
                f2.write(',' + l2)
            i3 += 1
        f2.write(');' + '\n\n\n')
        print('module list output finished')
        print(i1 + 1)

    return i1 + 1
######################################################################


# filename1 is the name of netlist file
# filename2 is the name of output file
# key_input_name is the list of key input name
# ln is the end line number after reading of module finished
# 4#####################################################################
def modi_input(filename1, filename2, key_input_name, ln):
    input_symbol = []
    with open(filename1, 'r') as f1:
        for read_line, line in enumerate(f1):
            line_ele = re.split('\W+', line)
            if read_line < ln:
                pass
            elif re.match('^//', line):
                print('comment')
                pass

            elif re.match('^input', line):
                print('input start')
                for ele in line_ele:
                    if (ele == 'input') or (ele == ''):
                        pass
                    else:
                        input_symbol.append(ele)
            elif re.match('.*', line):
                for ele in line_ele:
                    if (ele == ''):
                        pass
                    else:
                        input_symbol.append(ele)
                if re.match('.*;$', line):
                    print('input finished')
                    break
                else:
                    pass
            else:
                print('empty')
                pass

    with open(filename2, 'a+') as f2:
        print('input opened successfully')
        i1 = 1
        f2.write('input  ')
        for l in input_symbol:
            if (i1 > 9) and (i1 % 10 == 0):
                f2.write(l + ',' + '\n')
            else:
                f2.write(l + ',')
            i1 += 1
        f2.write('\n')

        i2 = 1
        for l1 in key_input_name:
            if (i2 == 1):
                f2.write(l1)
            elif (i2 > 9) and (i2 % 10 == 1):
                f2.write(',' + '\n' + l1)
            else:
                f2.write(',' + l1)
            i2 += 1
        f2.write(';' + '\n\n\n')
        print('input list finished')

    return read_line + 1, input_symbol
######################################################################


# 5#####################################################################
def modi_output(filename1, filename2, ln):
    output_symbol = []
    with open(filename1, 'r') as f1:
        for i1, line in enumerate(f1):
            line_ele = re.split('\W+', line)
            if i1 < ln:
                pass
            elif re.match('^//', line):
                print('comment')
                pass

            elif re.match('^output', line):
                print('output start')
                for ele in line_ele:
                    if (ele == 'output') or (ele == ''):
                        pass
                    else:
                        output_symbol.append(ele)
            elif re.match('.*', line):
                for ele in line_ele:
                    if ele == '':
                        pass
                    else:
                        output_symbol.append(ele)
                if re.match('.*;$', line):
                    print('output finish')
                    break
                else:
                    pass
            else:
                print('empty')
                pass

    newout = []
    for o1 in range(len(output_symbol)):
        newout.append('antisat' + output_symbol[o1])

    with open(filename2, 'a+') as f2:
        print('output opened successfully')
        i2 = 1
        f2.write('output ')
        for l1 in newout:
            if i2 == 1:
                f2.write(l1)
            elif (i2 > 9) and (i2 % 10 == 1):
                f2.write(',' + '\n' + l1)
            else:
                f2.write(',' + l1)
            i2 += 1
        f2.write(';' + '\n\n\n')
        print('output list finished')

    return i1 + 1, output_symbol, newout
######################################################################
###输出的是output_symbol列表，每个元素就是每个output的名字
###output output_symbol list containing all the output names


# 7#####################################################################
def modi_wire(filename1, filename2, ln, wirelist):
    wire_symbol = []
    with open(filename1, 'r') as f1:
        for read_line, line in enumerate(f1):
            line_ele = re.split('\W+', line)
            if read_line < ln:
                pass
            elif re.match('^//', line):
                print('comment')
                pass

            elif re.match('^wire', line):
                print('wire start')
                for ele in line_ele:
                    if (ele == 'wire') or (ele == ''):
                        pass
                    else:
                        wire_symbol.append(ele)
            elif re.match('.*', line):
                for ele in line_ele:
                    if (ele == ''):
                        pass
                    else:
                        wire_symbol.append(ele)
                if re.match('.*;$', line):
                    print('wire finished')
                    break
                else:
                    pass
            else:
                print('empty')
                pass

    # wire_symbol += wirelist
    with open(filename2, 'a+') as f2:
        print('wire opened successfully')
        i1 = 1
        f2.write('wire  ')
        for l in wire_symbol:
            if (i1 > 9) and (i1 % 10 == 0):
                f2.write(l + ',' + '\n')
            else:
                f2.write(l + ',')
            i1 += 1
        f2.write('\n')

        i2 = 1
        # for l1 in key_gate_name:
        for l1 in wirelist:
            if i2 == 1:
                f2.write(l1)
            elif (i2 > 9) and (i2 % 10 == 1):
                f2.write(',' + '\n' + l1)
            else:
                f2.write(',' + l1)
            i2 += 1
        f2.write(';' + '\n\n\n')
        print('wire list finished')

    return read_line + 1, wire_symbol
######################################################################


# 8#####################################################################
def write_gate(filename2, gate_list):
    with open(filename2, 'a+') as f:
        for g1 in gate_list:
            f.write(g1)
        f.write('\n' + 'endmodule')
######################################################################


# 9#####################################################################
def read_gate(filename, ln):
    gate_symbol = []
    gate_data = []
    gate_temp = []
    gate_no = 0
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            line_ele = re.split('\W+', line)
            if i < ln:
                pass
            elif re.match('^endmodule', line):
                print('read over')
                break
            elif re.match('^[a-zA-Z]', line):
                '''if i<3000 and i >2950:
                    print(line_ele)
                else:
                    pass'''
                gate_temp1 = []
                gate_symbol.append(line)
                for ele in line_ele:
                    if ele == '':
                        pass
                    else:
                        gate_temp.append(ele)
                        # if i<3000 and i>2950:
                        #    print(str(gate_temp))
                        # else:
                        #    pass
                # print(gate_temp)
                gate_temp1.append(gate_temp[0])
                gate_temp1.append(gate_temp[1])
                gate_temp1.append(gate_temp[2])
                gate_temp1.append([])
                for g1 in range(3, len(gate_temp)):
                    gate_temp1[3].append(gate_temp[g1])
                gate_data.append(gate_temp1)
                gate_no += 1
                gate_temp = []
    return gate_no, gate_symbol, gate_data
#######################################################################
###生成两个list，gate_symbol的每个元素直接就是gate那一行
###gate_data的每个元素也是一个list，第0个元素为gate类型
###第1个为gate名，第2个元素为output，第3个元素为一个list，input list

###gate_symbol的每个元素是自带一个\n的，因为是直接提取的line


# need list layer1


def modi_gate(userin, keynamelist, layer1, layer2, layer3, originout, input_symbol, output_symbol, gate_symbol):
    antisatgate = []
    andin = ''
    nandin = ''

    temp1 = int(userin[1] // 2)
    for i1 in range(temp1):
        antisatgate.append(
            'xor antileft' + str(i1) + ' (' + layer1[i1] + ', ' + keynamelist[i1] + ', ' + input_symbol[i1] + ');\n')
        andin += ', ' + layer1[i1]
    for i2 in range(temp1):
        antisatgate.append(
            'xor antiright' + str(i2) + ' (' + layer1[-i2-1] + ', ' + keynamelist[-i2-1] + ', ' + input_symbol[i2] + ');\n')
        nandin += ', ' + layer1[-i2-1]

    antisatgate.append('and antiand(' + layer2[0] + andin + ');\n')
    antisatgate.append('nand antinand(' + layer2[1] + nandin + ');\n')
    antisatgate.append('and antiall('+layer3[0] + ', ' + layer2[1] + ', ' + layer2[0] + ');\n')

    for o1 in range(len(output_symbol)):
        antisatgate.append('xor out'+str(o1)+'('+output_symbol[o1]+', '+layer3[0]+', '+originout[o1]+');\n')

    newtxt = gate_symbol + antisatgate

    return newtxt


def unill(userfile, filein, fileout, inputs, outputs, wires, gates):
    userin = read_user(userfile)
    print(userin)

    keynamelist = key_inputs(userin[1])
    print(keynamelist)

    # keywirelist = key_points(userin[1])
    # print(keywirelist)

    wirelist, layer1, layer2, layer3 = antisatwire(userin, outputs)

    readline1 = modi_module(filein, fileout, userin[0][:-2], inputs, keynamelist, outputs)

    readline2, input_symbol = modi_input(filein, fileout, keynamelist, readline1)
    # print(input_symbol[10])
    readline3, originout, newout = modi_output(filein, fileout, readline2)

    readline4, wire_symbol = modi_wire(filein, fileout, readline3, wirelist)

    gate_no, gate_symbol, gate_data = read_gate(filein, readline4)

    # print(gate_symbol[3])
    # print(gate_data[10])
    keygatelist = modi_gate(userin, keynamelist, layer1, layer2, layer3, originout, input_symbol, newout, gate_symbol)

    write_gate(fileout, keygatelist)

# def antisat(userin, keynamelist, keywirelist, gate_symbol, gate_data, input_symbol):
