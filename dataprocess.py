# !/usr/bin/env python3
# -i- coding:UTF-8 -*-i-


from readverilog import Netlist
# 验证完成


# inputlist = dataprocess.processinput(key)
def processinput(key):
    return key.inputlist


# outputlist = dataprocess.processoutput()
def processoutput():
    return ['Finalout']


# allwire, miterlist = dataprocess.processwire(ori, key)
def processwire(ori, key):
    miterlist = []
    for i in range(len(ori.outputlist)):
        miterlist.append('miter'+str(i))
    allwire = ori.wirelist + key.newwire + ori.outputlist + key.newoutput + miterlist
    return allwire, miterlist


# totalgate, totalgatedata = dataprocess.processgate(ori, key, miterlist)
def processgate(ori, key, miterlist):
    totalgate = []
    totalgatedata = []
    for o in ori.gatedata:
        inputtxt = ''
        for o1 in o[3]:
            inputtxt += ', '+o1
        totalgate.append([o[0]+' '+o[1]+' ('+o[2]+inputtxt+');\n'])
        totalgatedata.append(o)

    for k in key.newgatedata:
        inputtxt = ''
        for k1 in k[3]:
            inputtxt += ', '+k1
        totalgate.append([k[0]+' '+k[1]+' ('+k[2]+inputtxt+');\n'])
        totalgatedata.append(k)

    miterdata = []
    miterinput = ''
    for i in range(len(miterlist)):
        miterdata.append(['xor mitergate'+str(i)+' ('+miterlist[i]+
                          ', '+ori.outputlist[i]+', '+key.newoutput[i]+');\n'])
        totalgatedata.append(['xor', 'mitergate'+str(i), miterlist[i], [ori.outputlist[i], key.newoutput[i]]])

    miterinputdata = []
    for j in miterlist:
        miterinput += str(', '+j)
        miterinputdata.append(j)
    miterdata.append(['or miterfinal (Finalout'+miterinput+');'])

    totalgatedata.append(['or', 'miterfinal', 'Finalout', miterinputdata])
    totalgate += miterdata

    return totalgate, totalgatedata


# inputlist, outputlist, wirelist, gatelist, gatedata = dataprocess.uniprocess(ori, key)
def uniprocess(ori, key):
    inputlist = processinput(key)
    outputlist = processoutput()
    wirelist, miterlist = processwire(ori, key)
    gatelist, gatedata = processgate(ori, key, miterlist)

    return inputlist, outputlist, wirelist, gatelist, gatedata



