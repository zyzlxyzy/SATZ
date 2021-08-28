# !/usr/bin/env python3
# -i- coding: UTF-8 -*-i-

def writegate(filename, gate_list):
    with open(filename, 'a+') as f:
        for g1 in gate_list:
            f.write(g1[0])
        f.write('\n' + 'endmodule')


def writemodule(filename, modulelist):
    with open(filename, 'a+') as f2:
        # 写入module list
        print('module output opened successfully')
        i2 = 1
        f2.write('module ' + filename[:-2] + ' (')
        for l1 in modulelist:
            if i2 == 1:
                f2.write(l1)
            elif (i2 > 9) and (i2 % 10 == 1):
                f2.write(',' + '\n' + l1)
            else:
                f2.write(',' + l1)
            i2 += 1
        f2.write(');' + '\n\n\n')
        print('module list output finished')


def writelist(filename, iow, iowlist):
    with open(filename, 'a+') as f2:
        # 写入input/output/wire list
        print(iow+' opened successfully')
        i1 = 1
        f2.write(iow+'  ')
        for l in iowlist:
            if i1 == 1:
                f2.write(l)
            elif (i1 > 9) and (i1 % 10 == 0):
                f2.write(', '+l+ '\n')
            else:
                f2.write(', '+l)
            i1 += 1
        f2.write(';' + '\n\n\n')
        print(iow+' list finished')


def uniwrite(filename, inputlist, outputlist, wirelist, gatedata):
    writemodule(filename, inputlist+outputlist)
    writelist(filename, 'input', inputlist)
    writelist(filename, 'output', outputlist)
    writelist(filename, 'wire', wirelist)
    writegate(filename, gatedata)


