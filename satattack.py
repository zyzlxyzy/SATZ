# !/usr/bin/env python3
# -i- coding: UTF-8 -*-i-


import itertools
import shutil
import os
import re
import copy


RLL = 1
ANTISAT = 2
MINISATPATH = '/opt/homebrew/bin/'


def genkeylist(keylen):
    keylist = [i+2 for i in range(keylen)]
    keynolist = [i for i in range(keylen)]
    allkey = [keylist]
    for i_keylen in range(keylen):
        for i_eachkey in itertools.combinations(keynolist, i_keylen + 1):
            tempkey = copy.deepcopy(keylist)
            for i_keybit in i_eachkey:
                tempkey[i_keybit] = tempkey[i_keybit] * (-1)
            allkey.append(tempkey)
    return allkey


def copyfile_adddip(filename1, filename2, dip, diplist):
    templist = copy.deepcopy(diplist)
    for dno in dip:
        templist[dno] = diplist[dno] * (-1)
    diptxt = ''  # 给temp1.cnf加上DIP的语句
    logtxt = ''
    for i_inputbit in templist:
        diptxt += str(i_inputbit) + ' 0\n'
        logtxt += str(i_inputbit)
    logtxt += '\n'
    shutil.copy(filename1, filename2)
    with open(filename2, 'a+') as f:
        f.write(diptxt)
    writelog1(logtxt)


def addrightkey(keylist):
    keytxt = '\n'
    for k in keylist: keytxt += (str(-k)+' ')
    keytxt += '0\n'
    with open('resultfiles/temp1.cnf', 'a+') as f:
        f.write(keytxt)


# endflag, keylist = attack_read(filename2, keylen)
def attack_read(filename2, keylen):
    keylist, line_ele = [], []
    endflag = 0
    os.system(MINISATPATH+'minisat ' + filename2 + ' resultfiles/result.cnf')
    with open('resultfiles/result.cnf', 'r') as f:
        for lineno, line in enumerate(f):
            if lineno == 0:
                if line[0] == 'U':
                    endflag = 1
                    break
            if lineno == 1:
                line_ele = re.split(' ', line)
    if not endflag:
        keylist = line_ele[1:keylen + 1]
    for k in range(len(keylist)): keylist[k] = int(keylist[k])

    return endflag, keylist


def addwrongkey(wrongkeylist, rightkeylist, keylen):
    allkey = genkeylist(keylen)
    tempwrong = []
    for i_key in allkey:
        if i_key not in rightkeylist:
            tempwrong.append(i_key)

    for i_tempwrong in tempwrong:
        if i_tempwrong not in wrongkeylist:
            wrongkeylist.append(i_tempwrong)

    return wrongkeylist


def writelog1(diptxt):
    with open('resultfiles/sat.log', 'a+') as f:
        f.write(diptxt)


def writelog2(rightkeylist):
    rightkeytxt = ''
    for i_rk in rightkeylist:
        rightkeytxt += 'rightkey: '
        for i_ek in i_rk:
            rightkeytxt += (str(i_ek) + ' ')
        rightkeytxt += '\n'
    with open('resultfiles/sat.log', 'a+') as f:
        f.write(rightkeytxt+'\n')
        f.write(str(len(rightkeylist))+'\n')


def rightkeyleft(wrongkeylist, keylen):
    finalright = []
    allkey = genkeylist(keylen=keylen)
    for i_allkey in allkey:
        if i_allkey not in wrongkeylist:
            finalright.append(i_allkey)
    return finalright


def singledip(wrongkeylist, keylen):
    # 这个函数一共分成几步
    # 1. 通过sat攻击，获得在当前DIP下，所有正确的key
    # 2. 得到包含所有key的list
    # 3. 用所有key的list减去正确key的list，来得到当前DIP排除的错误的key的list
    # 4. 把得到的错误keylist和之前的错误keylist融合起来
    dipdoneflag, keyfinishflag = 0, 0  # dipdoneflag是指当前dip已经不能排除更多错误key，keyfinishflag意思是所有错误key已经被排除
    rightkeylist = []
    while not dipdoneflag:
        dipdoneflag, rightkey = attack_read(filename2='resultfiles/temp1.cnf', keylen=keylen)
        if not dipdoneflag:
            addrightkey(rightkey)
            rightkeylist.append(rightkey)
        elif (dipdoneflag and rightkey) or (not dipdoneflag and not rightkey): print('satattack.singledip error')
    if rightkeylist:
        wrongkeylist = addwrongkey(wrongkeylist=wrongkeylist, rightkeylist=rightkeylist, keylen=keylen)
    writelog2(rightkeylist)
    return wrongkeylist, rightkeylist


def diploop(filename1, inputlen, keylen, lltype):                # 13行
    endflag = 0                                          # 如果endflag=0，之后的dip遍历就会跳出
    diplist = [i + 2 + keylen for i in range(inputlen)]  # 生成cnf格式的diplist比如c17的就是[4,5,6,7,8]
    dipnolist = [i for i in range(inputlen)]
    wrongkeylist = []                                    # 用来存储已经排除的错误的key，如[[2,3], [-2, 3], ...]
    rightkeylist = []
    dipno = 0

    for i_inputlen in range(inputlen):
        if endflag: break
        for i_dip in itertools.combinations(dipnolist, i_inputlen + 1):
            lastwronglen = copy.deepcopy(len(wrongkeylist))
            copyfile_adddip(filename1=filename1, filename2='resultfiles/temp1.cnf', dip=i_dip, diplist=diplist)
            wrongkeylist, rightkeylist = singledip(wrongkeylist=wrongkeylist, keylen=keylen)

            if lltype == RLL: rightkeyno = 1
            elif lltype == ANTISAT: rightkeyno = 2 ** (keylen/2)

            if lastwronglen == 2 ** keylen - rightkeyno:
                endflag = 1
                break
            elif lastwronglen > 2 ** keylen - rightkeyno: print('排除了太多key了')
            dipno += 1
            if lastwronglen != len(wrongkeylist):
                with open('resultfiles/percent.log', 'a+') as f:
                    f.write(str(dipno)+'\n')
                    f.write(str(len(wrongkeylist))+'\n')
                    f.write(str(len(wrongkeylist)/(2**keylen))+'\n\n')
    finalkey = rightkeyleft(wrongkeylist=wrongkeylist, keylen=keylen)

    return finalkey, dipno


'''
def selectkey(filename2, falsekey, keyno, cnftxt):
    endflag = 0
    rightkey = []

    with open('verilogfiles/log.txt', 'a+') as f1:
        f1.write(cnftxt)

    while not endflag:
        os.system('/opt/homebrew/bin/minisat ' + filename2 + ' verilogfiles/result.cnf')
        with open('verilogfiles/result.cnf') as f:
            for lineno, line in enumerate(f):
                if lineno == 0:
                    if line[0] == 'U':
                        endflag = 1
                        break
                if lineno == 1:
                    line_ele = re.split(' ', line)

        if endflag:
            with open('verilogfiles/log.txt', 'a+') as f1:
                f1.write('搞不定了\n')
            break
        else:
            with open('verilogfiles/log.txt', 'a+') as f1:
                f1.write(str(line_ele) + '\n')

            temp1 = []
            temprightkey = line_ele[1: keyno + 1]
            keytxt = ''
            for t in temprightkey:
                keytxt += str(-int(t)) + ' '
                temp1.append(int(t))
            keytxt += '0\n'
            rightkey.append(temp1)

            with open(filename2, 'a+') as f1:
                f1.write(keytxt)

    alllist = allkey(keyno)
    faultno = 0
    for a1 in alllist:
        if (a1 not in rightkey) and (a1 not in falsekey):
            faultno += 1
            falsekey.append(a1)

    return falsekey, faultno


def copycnf(filename1, filename2, diptxt, wrongkeytxt):
    shutil.copy(filename1, filename2)
    with open(filename2, 'a+') as f:
        f.write(diptxt)
        f.write(wrongkeytxt)


# wrongkeylist, keytxt = dataprocess(wrongkeylist, newwrong)
def dataprocess(wrongkeylist, newwrong):
    intkeylist = []
    for n in newwrong:
        intkeylist.append(int(n))
    wrongkeylist.append(intkeylist)

    keytxt = ''
    for i in intkeylist:
        keytxt += str(-i) + ' '
    keytxt += '0\n'

    return wrongkeylist, keytxt
'''
