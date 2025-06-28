import numpy as np
import csv

#测量值矩阵、测量值改正数等类似的矩阵元素说明：
#x1
#x2
#x3
#x4
#y1
#y2
#y3
#y4

class adjustment:

    def __init__(self,f,x0,y0):
        self.f=f
        self.x0=x0
        self.y0=y0

    def input_from_csv(self,file):
        num=int(input("输入控制点数："))
        self.num=num
        self.data=np.zeros([num,7])
        file=open(file,'r',encoding='utf-8')
        reader=csv.reader(file)
        i=0
        for row in reader:
            for n in range(7):
                self.data[i,n]=row[n]
            i+=1
        file.close()

    def input(self):
        num=int(input("输入控制点数："))
        self.num=num
        self.data=np.zeros([num,7])
        for i in range(num):
            self.data[i,0]=float(input(f"第{i+1}个点的左片x："))
            self.data[i,1]=float(input(f"第{i+1}个点的左片y："))
            self.data[i,2]=float(input(f"第{i+1}个点的右片x："))
            self.data[i,3]=float(input(f"第{i+1}个点的右片y："))
            self.data[i,4]=float(input(f"第{i+1}个点的地面摄影测量坐标X："))
            self.data[i,5]=float(input(f"第{i+1}个点的地面摄影测量坐标Y："))
            self.data[i,6]=float(input(f"第{i+1}个点的地面摄影测量坐标Z："))
    
    def setup(self):
        self.Delta_left=np.zeros([6,1]) #左片未知数改正矩阵
        self.Delta_right=np.zeros([6,1]) #右片未知数改正矩阵
        self.V_left=np.zeros([2*self.num,1]) #左片观测值改正矩阵
        self.V_right=np.zeros([2*self.num,1])
        self.A_left=np.zeros([2*self.num,6])
        self.A_right=np.zeros([2*self.num,6])
        self.L_left=np.zeros([2*self.num,1])
        self.L_right=np.zeros([2*self.num,1])
        self.phi_left=0
        self.phi_right=0
        self.omiga_left=0
        self.omiga_right=0
        self.kappa_left=0
        self.kappa_right=0
        Xsum=Ysum=0
        for i in range(self.num):
            Xsum+=self.data[i,4]
            Ysum+=self.data[i,5]
        self.X_left=self.X_right=Xsum/self.num
        self.Y_left=self.Y_right=Ysum/self.num
        self.Z_left=self.Z_right=1500
        self.R_left=np.zeros([3,3])
        self.R_right=np.zeros([3,3])
        self.x_left=np.zeros([2*self.num,1])
        self.x_right=np.zeros([2*self.num,1])
        self.left_stop=False
        self.right_stop=False

    def get_rot(self): #构造旋转矩阵
        if self.left_stop is False:
            self.R_left[0,0]=np.cos(self.phi_left)*np.cos(self.kappa_left)-np.sin(self.phi_left)*np.sin(self.omiga_left)*np.sin(self.kappa_left)
            self.R_left[0,1]=-np.cos(self.phi_left)*np.sin(self.kappa_left)-np.sin(self.phi_left)*np.sin(self.omiga_left)*np.cos(self.kappa_left)
            self.R_left[0,2]=-np.sin(self.phi_left)*np.cos(self.omiga_left)
            self.R_left[1,0]=np.cos(self.omiga_left)*np.sin(self.kappa_left)
            self.R_left[1,1]=np.cos(self.omiga_left)*np.cos(self.kappa_left)
            self.R_left[1,2]=-np.sin(self.omiga_left)
            self.R_left[2,0]=np.sin(self.phi_left)*np.cos(self.kappa_left)+np.cos(self.phi_left)*np.sin(self.omiga_left)*np.sin(self.kappa_left)
            self.R_left[2,1]=-np.sin(self.phi_left)*np.sin(self.kappa_left)+np.cos(self.phi_left)*np.sin(self.omiga_left)*np.cos(self.kappa_left)
            self.R_left[2,2]=np.cos(self.phi_left)*np.cos(self.omiga_left)

        if self.right_stop is False:
            self.R_right[0,0]=np.cos(self.phi_right)*np.cos(self.kappa_right)-np.sin(self.phi_right)*np.sin(self.omiga_right)*np.sin(self.kappa_right)
            self.R_right[0,1]=-np.cos(self.phi_right)*np.sin(self.kappa_right)-np.sin(self.phi_right)*np.sin(self.omiga_right)*np.cos(self.kappa_right)
            self.R_right[0,2]=-np.sin(self.phi_right)*np.cos(self.omiga_right)
            self.R_right[1,0]=np.cos(self.omiga_right)*np.sin(self.kappa_right)
            self.R_right[1,1]=np.cos(self.omiga_right)*np.cos(self.kappa_right)
            self.R_right[1,2]=-np.sin(self.omiga_right)
            self.R_right[2,0]=np.sin(self.phi_right)*np.cos(self.kappa_right)+np.cos(self.phi_right)*np.sin(self.omiga_right)*np.sin(self.kappa_right)
            self.R_right[2,1]=-np.sin(self.phi_right)*np.sin(self.kappa_right)+np.cos(self.phi_right)*np.sin(self.omiga_right)*np.cos(self.kappa_right)
            self.R_right[2,2]=np.cos(self.phi_right)*np.cos(self.omiga_right)

    def get_obs_cal(self): #计算观测值的计算值
        if self.left_stop is False:
            for i in range(self.num):
                self.x_left[i,0]=(-self.f)*((self.R_left[0,0]*(self.data[i,4]-self.X_left)+self.R_left[1,0]*(self.data[i,5]-self.Y_left)+self.R_left[2,0]*(self.data[i,6]-self.Z_left))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left)))+self.x0
            for i in range(self.num):
                self.x_left[i+self.num,0]=(-self.f)*((self.R_left[0,1]*(self.data[i,4]-self.X_left)+self.R_left[1,1]*(self.data[i,5]-self.Y_left)+self.R_left[2,1]*(self.data[i,6]-self.Z_left))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left)))+self.y0

        if self.right_stop is False:
            for i in range(self.num):
                self.x_right[i,0]=(-self.f)*((self.R_right[0,0]*(self.data[i,4]-self.X_right)+self.R_right[1,0]*(self.data[i,5]-self.Y_right)+self.R_right[2,0]*(self.data[i,6]-self.Z_right))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right)))+self.x0
            for i in range(self.num):
                self.x_right[i+self.num,0]=(-self.f)*((self.R_right[0,1]*(self.data[i,4]-self.X_right)+self.R_right[1,1]*(self.data[i,5]-self.Y_right)+self.R_right[2,1]*(self.data[i,6]-self.Z_right))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right)))+self.y0

    def get_L(self): #构建平差使用的系数矩阵L
        if self.left_stop is False:
            self.L_left[0:self.num]=self.data[0:self.num,0:1]-self.x_left[0:self.num]
            self.L_left[self.num:2*self.num]=self.data[0:self.num,1:2]-self.x_left[self.num:2*self.num]
        if self.right_stop is False:
            self.L_right[0:self.num]=self.data[0:self.num,2:3]-self.x_right[0:self.num]
            self.L_right[self.num:2*self.num]=self.data[0:self.num,3:4]-self.x_right[self.num:2*self.num]
    
    def get_A(self): #构建平差使用的系数矩阵A
        if self.left_stop is False:
            for i in range(self.num):
                self.A_left[i,0]=(self.R_left[0,0]*self.f+self.R_left[0,2]*(self.data[i,0]-self.x0))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left))
                self.A_left[i,1]=(self.R_left[1,0]*self.f+self.R_left[1,2]*(self.data[i,0]-self.x0))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left))
                self.A_left[i,2]=(self.R_left[2,0]*self.f+self.R_left[2,2]*(self.data[i,0]-self.x0))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left))
                self.A_left[i,3]=(self.data[i,1]-self.y0)*np.sin(self.omiga_left)-(((self.data[i,0]-self.x0)/self.f)*((self.data[i,0]-self.x0)*np.cos(self.kappa_left)-(self.data[i,1]-self.y0)*np.sin(self.kappa_left))+self.f*np.cos(self.kappa_left))*np.cos(self.omiga_left)
                self.A_left[i,4]=-self.f*np.sin(self.kappa_left)-((self.data[i,0]-self.x0)/self.f)*((self.data[i,0]-self.x0)*np.sin(self.kappa_left)+(self.data[i,1]-self.y0)*np.cos(self.kappa_left))
                self.A_left[i,5]=self.data[i,1]-self.y0
            for i in range(self.num):
                self.A_left[i+self.num,0]=(self.R_left[0,1]*self.f+self.R_left[0,2]*(self.data[i,1]-self.y0))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left))
                self.A_left[i+self.num,1]=(self.R_left[1,1]*self.f+self.R_left[1,2]*(self.data[i,1]-self.y0))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left))
                self.A_left[i+self.num,2]=(self.R_left[2,1]*self.f+self.R_left[2,2]*(self.data[i,1]-self.y0))/(self.R_left[0,2]*(self.data[i,4]-self.X_left)+self.R_left[1,2]*(self.data[i,5]-self.Y_left)+self.R_left[2,2]*(self.data[i,6]-self.Z_left))
                self.A_left[i+self.num,3]=-(self.data[i,0]-self.x0)*np.sin(self.omiga_left)-(((self.data[i,1]-self.y0)/self.f)*((self.data[i,0]-self.x0)*np.cos(self.kappa_left)-(self.data[i,1]-self.y0)*np.sin(self.kappa_left))-self.f*np.cos(self.kappa_left))*np.cos(self.omiga_left)
                self.A_left[i+self.num,4]=-self.f*np.cos(self.kappa_left)-((self.data[i,1]-self.y0)/self.f)*((self.data[i,0]-self.x0)*np.sin(self.kappa_left)+(self.data[i,1]-self.y0)*np.cos(self.kappa_left))
                self.A_left[i+self.num,5]=-(self.data[i,0]-self.x0)

        if self.right_stop is False:
            for i in range(self.num):
                self.A_right[i,0]=(self.R_right[0,0]*self.f+self.R_right[0,2]*(self.data[i,2]-self.x0))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right))
                self.A_right[i,1]=(self.R_right[1,0]*self.f+self.R_right[1,2]*(self.data[i,2]-self.x0))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right))
                self.A_right[i,2]=(self.R_right[2,0]*self.f+self.R_right[2,2]*(self.data[i,2]-self.x0))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right))
                self.A_right[i,3]=(self.data[i,3]-self.y0)*np.sin(self.omiga_right)-((((self.data[i,2]-self.x0)/self.f)*((self.data[i,2]-self.x0)*np.cos(self.kappa_right)-(self.data[i,3]-self.y0)*np.sin(self.kappa_right))+self.f*np.cos(self.kappa_right))*np.cos(self.omiga_right))
                self.A_right[i,4]=-self.f*np.sin(self.kappa_right)-(((self.data[i,2]-self.x0)/self.f)*((self.data[i,2]-self.x0)*np.sin(self.kappa_right)+(self.data[i,3]-self.y0)*np.cos(self.kappa_right)))
                self.A_right[i,5]=self.data[i,3]-self.y0
            for i in range(self.num):
                self.A_right[i+self.num,0]=(self.R_right[0,1]*self.f+self.R_right[0,2]*(self.data[i,3]-self.y0))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right))
                self.A_right[i+self.num,1]=(self.R_right[1,1]*self.f+self.R_right[1,2]*(self.data[i,3]-self.y0))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right))
                self.A_right[i+self.num,2]=(self.R_right[2,1]*self.f+self.R_right[2,2]*(self.data[i,3]-self.y0))/(self.R_right[0,2]*(self.data[i,4]-self.X_right)+self.R_right[1,2]*(self.data[i,5]-self.Y_right)+self.R_right[2,2]*(self.data[i,6]-self.Z_right))
                self.A_right[i+self.num,3]=-(self.data[i,2]-self.x0)*np.sin(self.omiga_right)-(((self.data[i,3]-self.y0)/self.f)*((self.data[i,2]-self.x0)*np.cos(self.kappa_right)-(self.data[i,3]-self.y0)*np.sin(self.kappa_right))-self.f*np.cos(self.kappa_right))*np.cos(self.omiga_right)
                self.A_right[i+self.num,4]=-self.f*np.cos(self.kappa_right)-((self.data[i,3]-self.y0)/self.f)*((self.data[i,2]-self.x0)*np.sin(self.kappa_right)+(self.data[i,3]-self.y0)*np.cos(self.kappa_right))
                self.A_right[i+self.num,5]=-(self.data[i,2]-self.x0)

    def get_Delta(self):
        if self.left_stop is False:
            self.Delta_left=np.linalg.inv(self.A_left.T @ self.A_left) @ self.A_left.T @ self.L_left
        if self.right_stop is False:
            self.Delta_right=np.linalg.inv(self.A_right.T @ self.A_right) @ self.A_right.T @ self.L_right

    def update(self):
        if self.left_stop is False:
            self.X_left+=self.Delta_left[0,0]
            self.Y_left+=self.Delta_left[1,0]
            self.Z_left+=self.Delta_left[2,0]
            self.phi_left+=self.Delta_left[3,0]
            self.omiga_left+=self.Delta_left[4,0]
            self.kappa_left+=self.Delta_left[5,0]

        if self.right_stop is False:
            self.X_right+=self.Delta_right[0,0]
            self.Y_right+=self.Delta_right[1,0]
            self.Z_right+=self.Delta_right[2,0]
            self.phi_right+=self.Delta_right[3,0]
            self.omiga_right+=self.Delta_right[4,0]
            self.kappa_right+=self.Delta_right[5,0]

        #for i in range(self.num):
            #self.data[i,0]+=self.V_left[i,0]
            #self.data[i,1]+=self.V_left[i+self.num,0]
            #self.data[i,2]+=self.V_right[i,0]
            #self.data[i,3]+=self.V_right[i+self.num,0]

    def get_V(self):
        self.V_left=self.A_left @ self.Delta_left - self.L_left
        self.V_right=self.A_right @ self.Delta_right - self.L_right

    def get_variations(self):
        self.delta_left=0.001*np.sqrt((self.V_left.T @ self.V_left)/(2*self.num-6))
        self.delta_right=0.001*np.sqrt((self.V_right.T @ self.V_right)/(2*self.num-6))
        self.variation_mat_left=1000*1000*self.delta_left*self.delta_left*np.linalg.inv(self.A_left.T @ self.A_left)
        self.variation_mat_right=1000*1000*self.delta_right*self.delta_right*np.linalg.inv(self.A_right.T @ self.A_right)
    
    def forward(self):
        self.get_rot()
        self.get_obs_cal()
        self.get_L()
        self.get_A()

    def backward(self):
        self.get_Delta()
        self.get_V()
        self.update()

    def whether_to_stop(self):
        stop=True
        for item in self.Delta_left:
            if np.abs(item) > 0.001:
                stop=False
                break
        if stop is True:
            self.left_stop=True

        stop=True
        for item in self.Delta_right:
            if np.abs(item) > 0.001:
                stop=False
                break
        if stop is True:
            self.right_stop=True

    def judge_accuracy(self):
        self.get_V()
        self.get_variations()