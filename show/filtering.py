import numpy
from numpy import *

def filtering(leadingwordlist,userscore):
    leadingwordnumber = len(leadingwordlist)
    stringlist = []

    for index in range(0,leadingwordnumber):
        #leadingwordlist[index]-->string
        leadingwordstring  =  ' 你好'
        stringlist.append(leadingwordstring)
   # stringlist.append('你好123456')
    #stringlist.append('你好12345678')
    #stringlist.append('你好1234567890')

    for i in range(0,leadingwordnumber):
        for j in range(i,leadingwordnumber):
            if(len(stringlist[i])<len(stringlist[j])):
                temp = leadingwordlist[i]
                tempstring = stringlist[i]
                stringlist[i] = stringlist[j]
                leadingwordlist[i] = leadingwordlist[j]
                stringlist[j] = tempstring
                leadingwordlist[j] = temp

    if(leadingwordnumber == 0):
        return -1
    elif(leadingwordnumber == 1 ):
        return leadingwordlist[0]
    elif(leadingwordnumber > 1):
        divide = 1/leadingwordnumber
        for k in range(0,leadingwordnumber):
            if(userscore>=k*divide and userscore < (k+1)*divide):
                return leadingwordlist[k]

    
if __name__ == "__main__":
    A = [1,2,3,4]
    B = 0.3
    i = filtering(A,B)
    print(i)