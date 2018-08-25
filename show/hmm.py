# -*- coding: UTF-8 -*-
import numpy
from numpy import *

class HMM:
    def __init__(self,A,B,Pi):
        self.A=A
        self.B=B
        self.Pi=Pi

    #前向算法
    def forward(self,O):
        row=self.A.shape[0]
        col=len(O)
        alpha=numpy.zeros((row,col))
        #初值
        alpha[:,0]=self.Pi*self.B[:,O[0]]
        #递推
        for t in range(1,col):
            for i in range(row):
                alpha[i,t]=numpy.dot(alpha[:,t-1],self.A[:,i])*self.B[i,O[t]]
        #终止
        return alpha

    #后向算法
    def backward(self,O):
        row=self.A.shape[0]
        col=len(O)
        beta=numpy.zeros((row,col))
        #初值
        beta[:,-1:]=1
        #递推
        for t in reversed(range(col-1)):
            for i in range(row):
                beta[i,t]=numpy.sum(self.A[i,:]*self.B[:,O[t+1]]*beta[:,t+1])
        #终止
        return beta

    #前向-后向算法(Baum-Welch算法):由 EM算法 & HMM 结合形成
    def baum_welch(self,O,e=0.05):

        row=self.A.shape[0]
        col=len(O)

        done=False
        while not done:
            zeta=numpy.zeros((row,row,col-1))
            alpha=self.forward(O)
            beta=self.backward(O)
            #EM算法：由 E-步骤 和 M-步骤 组成
            #E-步骤：计算期望值zeta和gamma
            for t in range(col-1):
                #分母部分
                denominator=numpy.dot(numpy.dot(alpha[:,t],self.A)*self.B[:,O[t+1]],beta[:,t+1])
                for i in range(row):
                    #分子部分以及zeta的值
                    numerator=alpha[i,t]*self.A[i,:]*self.B[:,O[t+1]]*beta[:,t+1]
                    zeta[i,:,t]=numerator/denominator
            gamma=numpy.sum(zeta,axis=1)
            final_numerator=(alpha[:,col-1]*beta[:,col-1]).reshape(-1,1)
            final=final_numerator/numpy.sum(final_numerator)
            gamma=numpy.hstack((gamma,final))
            #M-步骤：重新估计参数Pi,A,B
            newPi=gamma[:,0]
            newA=numpy.sum(zeta,axis=2)/numpy.sum(gamma[:,:-1],axis=1)
            newB=numpy.copy(self.B)
            b_denominator=numpy.sum(gamma,axis=1)
            temp_matrix=numpy.zeros((1,len(O)))
            for k in range(self.B.shape[1]):
                for t in range(len(O)):
                    if O[t]==k:
                        temp_matrix[0][t]=1
                newB[:,k]=numpy.sum(gamma*temp_matrix,axis=1)/b_denominator
            #终止阀值
            if numpy.max(abs(self.Pi-newPi))<e and numpy.max(abs(self.A-newA))<e and numpy.max(abs(self.B-newB))<e:
                done=True 
            self.A=newA
            self.B=newB
            self.Pi=newPi
        return self.Pi


#将字典转化为矩阵
def matrix(X,index1,index2):
    #初始化为0矩阵
    m = numpy.zeros((len(index1),len(index2)))
    for row in X:
        for col in X[row]:
            #转化
            m[index1.index(row)][index2.index(col)]=X[row][col]
    return m

if __name__ == "__main__":  
    #初始化,随机的给参数A,B,Pi赋值
    status = ["掌握该词","未掌握该词"]
    observations = ["答对","答错"]
    A={"掌握该词":{"掌握该词":0.7,"未掌握该词":0.3},"未掌握该词":{"掌握该词":0.25,"未掌握该词":0.75}}
    B={"掌握该词":{"答对":0.6,"答错":0.4},"未掌握该词":{"答对":0.25,"答错":0.75}}
    Pi = [0.5,0.5]
    O = [1,0,1]

    A=matrix(A,status,status)
    B=matrix(B,status,observations)
    hmm=HMM(A,B,Pi)

    list = hmm.baum_welch(O)
    print(list)
    print("%.8f"%list[0])
