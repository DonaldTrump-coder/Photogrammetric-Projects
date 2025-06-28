import numpy as np

class forward:
    def __init__(self,points_num):
        self.R_left=np.zeros([3,3])
        self.R_right=np.zeros([3,3])
        self.points_num=int(points_num)
        self.f=0
        self.input_left=np.zeros([3,self.points_num])
        self.input_right=np.zeros([3,self.points_num])
        self.Bx=0
        self.By=0
        self.Bz=0
        self.N1=np.zeros([self.points_num])
        self.N2=np.zeros([self.points_num])
        self.points_left=np.zeros([3,self.points_num])
        self.points_right=np.zeros([3,self.points_num])
        self.result=np.zeros([3,self.points_num])

    def setup(self,file):
        with open(file,'r') as file:
            line_index=0
            for line in file:
                if line_index == 0:
                    paras=line.strip().split(',')
                    self.f=float(paras[0])
                    self.x0=float(paras[1])
                    self.y0=float(paras[2])
                    line_index+=1
                else:
                    data=line.strip().split(',')
                    self.input_left[0,line_index-1]=float(data[0])-self.x0
                    self.input_left[1,line_index-1]=float(data[1])-self.y0
                    self.input_left[2,line_index-1]=-self.f
                    self.input_right[0,line_index-1]=float(data[2])-self.x0
                    self.input_right[1,line_index-1]=float(data[3])-self.y0
                    self.input_right[2,line_index-1]=-self.f
                    line_index+=1

    def get_rot(self,fai_left,omiga_left,kappa_left,fai_right,omiga_right,kappa_right):
        self.R_left[0,0]=np.cos(fai_left)*np.cos(kappa_left)-np.sin(fai_left)*np.sin(omiga_left)*np.sin(kappa_left)
        self.R_left[0,1]=-np.cos(fai_left)*np.sin(kappa_left)-np.sin(fai_left)*np.sin(omiga_left)*np.cos(kappa_left)
        self.R_left[0,2]=-np.sin(fai_left)*np.cos(omiga_left)
        self.R_left[1,0]=np.cos(omiga_left)*np.sin(kappa_left)
        self.R_left[1,1]=np.cos(omiga_left)*np.cos(kappa_left)
        self.R_left[1,2]=-np.sin(omiga_left)
        self.R_left[2,0]=np.sin(fai_left)*np.cos(kappa_left)+np.cos(fai_left)*np.sin(omiga_left)*np.sin(kappa_left)
        self.R_left[2,1]=-np.sin(fai_left)*np.sin(kappa_left)+np.cos(fai_left)*np.sin(omiga_left)*np.cos(kappa_left)
        self.R_left[2,2]=np.cos(fai_left)*np.cos(omiga_left)

        self.R_right[0,0]=np.cos(fai_right)*np.cos(kappa_right)-np.sin(fai_right)*np.sin(omiga_right)*np.sin(kappa_right)
        self.R_right[0,1]=-np.cos(fai_right)*np.sin(kappa_right)-np.sin(fai_right)*np.sin(omiga_right)*np.cos(kappa_right)
        self.R_right[0,2]=-np.sin(fai_right)*np.cos(omiga_right)
        self.R_right[1,0]=np.cos(omiga_right)*np.sin(kappa_right)
        self.R_right[1,1]=np.cos(omiga_right)*np.cos(kappa_right)
        self.R_right[1,2]=-np.sin(omiga_right)
        self.R_right[2,0]=np.sin(fai_right)*np.cos(kappa_right)+np.cos(fai_right)*np.sin(omiga_right)*np.sin(kappa_right)
        self.R_right[2,1]=-np.sin(fai_right)*np.sin(kappa_right)+np.cos(fai_right)*np.sin(omiga_right)*np.cos(kappa_right)
        self.R_right[2,2]=np.cos(fai_right)*np.cos(omiga_right)

    def get_assist(self):
        self.assist_left=self.R_left @ self.input_left
        self.assist_right=self.R_right @ self.input_right

    def get_base(self,X_left,Y_left,Z_left,X_right,Y_right,Z_right):
        self.Bx=X_right-X_left
        self.By=Y_right-Y_left
        self.Bz=Z_right-Z_left
        self.X_left=X_left
        self.Y_left=Y_left
        self.Z_left=Z_left
        self.Y_right=Y_right

    def get_N(self):
        self.N1=(self.Bx*self.assist_right[2,:]-self.Bz*self.assist_right[0,:])/(self.assist_left[0,:]*self.assist_right[2,:]-self.assist_left[2,:]*self.assist_right[0,:]+0.1)
        self.N2=(self.Bx*self.assist_left[2,:]-self.Bz*self.assist_left[0,:])/(self.assist_left[0,:]*self.assist_right[2,:]-self.assist_left[2,:]*self.assist_right[0,:]+0.2)

    def get_points(self):
        for i in range(self.points_num):
            self.points_left[:,i]=self.N1[i]*self.assist_left[:,i]
            self.points_right[:,i]=self.N2[i]*self.assist_right[:,i]

    def get_result(self):
        self.result[0,:]=self.X_left+self.points_left[0,:]
        self.result[2,:]=self.Z_left+self.points_left[2,:]
        self.result[1,:]=(self.Y_left+self.points_left[1,:]+self.Y_right+self.points_right[1,:])*0.5

    def forward(self,X_left,Y_left,Z_left,X_right,Y_right,Z_right,fai_left,omiga_left,kappa_left,fai_right,omiga_right,kappa_right):
        self.get_rot(fai_left,omiga_left,kappa_left,fai_right,omiga_right,kappa_right)
        self.get_assist()
        self.get_base(X_left,Y_left,Z_left,X_right,Y_right,Z_right)
        self.get_N()
        self.get_points()
        self.get_result()

if __name__=="__main__":
    a=forward(4)
    a.get_assist()
    a.get_N()
    print(a.N1.shape)