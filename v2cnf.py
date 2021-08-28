# !/usr/bin/env python3
# -i- coding:UTF-8 -*-i-


# keylist, inputlist = v2cnf.findkey(ori, key)
def findkey(ori, key):
    keylist = []
    inputlist = []
    for k in key:
        if k not in ori:
            keylist.append(k)
        else:
            inputlist.append(k)
    return keylist, inputlist


# dictall = v2cnf.makedic(outputlist, keylist, inputlist, wirelist)
def makedic(outputlist, keylist, inputlist, wirelist):
    listall = outputlist + keylist + inputlist + wirelist
    dictall = {}
    for i in range(1, len(listall)+1):
        dictall[listall[i-1]] = i
    return dictall


def net2cnf(gatedata, dictall):
    gatecnf = ''
    if gatedata[0] == 'xor':
        if len(gatedata[3]) != 2:
            print('xor input bit number error!')
        else:
            gatecnf += str(-dictall[gatedata[2]])+' '+str(-dictall[gatedata[3][0]])+' '+str(-dictall[gatedata[3][1]])+' 0\n'
            gatecnf += str(-dictall[gatedata[2]]) + ' ' + str(dictall[gatedata[3][0]]) + ' ' + str(
                dictall[gatedata[3][1]]) + ' 0\n'
            gatecnf += str(dictall[gatedata[2]]) + ' ' + str(-dictall[gatedata[3][0]]) + ' ' + str(
                dictall[gatedata[3][1]]) + ' 0\n'
            gatecnf += str(dictall[gatedata[2]]) + ' ' + str(dictall[gatedata[3][0]]) + ' ' + str(
                -dictall[gatedata[3][1]]) + ' 0\n'

    elif gatedata[0] == 'xnor':
        if len(gatedata[3]) != 2:
            print('xnor input bit number error!')
        else:
            gatecnf += str(dictall[gatedata[2]])+' '+str(dictall[gatedata[3][0]])+' '+str(
                dictall[gatedata[3][1]])+' 0\n'
            gatecnf += str(-dictall[gatedata[2]]) + ' ' + str(-dictall[gatedata[3][0]]) + ' ' + str(
                dictall[gatedata[3][1]]) + ' 0\n'
            gatecnf += str(dictall[gatedata[2]]) + ' ' + str(-dictall[gatedata[3][0]]) + ' ' + str(
                -dictall[gatedata[3][1]]) + ' 0\n'
            gatecnf += str(-dictall[gatedata[2]]) + ' ' + str(dictall[gatedata[3][0]]) + ' ' + str(
                -dictall[gatedata[3][1]]) + ' 0\n'

    elif gatedata[0] == 'and':
        andtxt = ''
        for a1 in gatedata[3]:
            gatecnf += str(-dictall[gatedata[2]])+' '+str(dictall[a1]) + ' 0\n'
            andtxt += str(-dictall[a1]) + ' '
        gatecnf += andtxt + str(dictall[gatedata[2]]) + ' 0\n'

    elif gatedata[0] == 'or':
        ortxt = ''
        for a1 in gatedata[3]:
            gatecnf += str(dictall[gatedata[2]]) + ' ' + str(-dictall[a1]) + ' 0\n'
            ortxt += str(dictall[a1]) + ' '
        gatecnf += ortxt + str(-dictall[gatedata[2]]) + ' 0\n'

    elif gatedata[0] == 'nand':
        nandtxt = ''
        for a1 in gatedata[3]:
            gatecnf += str(dictall[gatedata[2]])+' '+str(dictall[a1]) + ' 0\n'
            nandtxt += str(-dictall[a1]) + ' '
        gatecnf += nandtxt + str(-dictall[gatedata[2]]) + ' 0\n'

    elif gatedata[0] == 'nor':
        nortxt = ''
        for a1 in gatedata[3]:
            gatecnf += str(-dictall[gatedata[2]])+' '+str(-dictall[a1]) + ' 0\n'
            nortxt += str(dictall[a1]) + ' '
        gatecnf += nortxt + str(dictall[gatedata[2]]) + ' 0\n'

    elif gatedata[0] == 'not':
        gatecnf += str(-dictall[gatedata[2]])+' '+str(-dictall[gatedata[3][0]]) + ' 0\n'
        gatecnf += str(dictall[gatedata[2]]) + ' ' + str(dictall[gatedata[3][0]]) + ' 0\n'

    elif gatedata[0] == 'buf':
        gatecnf += str(-dictall[gatedata[2]])+' '+str(dictall[gatedata[3][0]]) + ' 0\n'
        gatecnf += str(dictall[gatedata[2]]) + ' ' + str(-dictall[gatedata[3][0]]) + ' 0\n'

    else:
        print('unknown type error')
    return gatecnf


def unicnf(ori, key, wirelist, gatedata, cnffilename):
    cnftxt = 'p cnf '+str(len(wirelist))+' '+str(len(gatedata))+'\n'+'-1 0\n'
    keylist, inputlist = findkey(ori.inputlist, key.inputlist)
    dictall = makedic(['Finalout'], keylist, inputlist, wirelist)
    for g in gatedata:
        cnftxt += net2cnf(g, dictall)

    with open(cnffilename, 'a+') as f:
        f.write(cnftxt)







