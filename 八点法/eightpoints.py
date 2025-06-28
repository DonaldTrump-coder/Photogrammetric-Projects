import numpy as np

class eightpoints:
    def __init__(self,file_left,file_right):
        with open(file_left,'r') as file:
            text=file.read()
            points=text.split('\n')
            points_num=points.__len__()-1
            self.data_left=np.zeros([points_num,3])
            for i in range(points_num):
                point=points[i+1].split(' ')
                self.data_left[i,0]=float(point[0])
                self.data_left[i,1]=float(point[1])
                self.data_left[i,2]=1
        
        with open(file_right,'r') as file:
            text=file.read()
            points=text.split('\n')
            points_num=points.__len__()-1
            self.data_right=np.zeros([points_num,3])
            for i in range(points_num):
                point=points[i+1].split(' ')
                self.data_right[i,0]=float(point[0])
                self.data_right[i,1]=float(point[1])
                self.data_right[i,2]=1
            self.points_num=points_num

    def normalize(self):
        self.x_center_left=np.sum(self.data_left[:,0])/self.points_num
        self.y_center_left=np.sum(self.data_left[:,1])/self.points_num
        self.x_center_right=np.sum(self.data_right[:,0])/self.points_num
        self.y_center_right=np.sum(self.data_right[:,1])/self.points_num

        x_left=self.data_left[:,0]-self.x_center_left
        y_left=self.data_left[:,1]-self.y_center_left
        x_right=self.data_right[:,0]-self.x_center_right
        y_right=self.data_right[:,1]-self.y_center_right

        s_left=np.sqrt(2)/(np.sum(np.sqrt(x_left*x_left+y_left*y_left))/self.points_num)
        s_right=np.sqrt(2)/(np.sum(np.sqrt(x_right*x_right+y_right*y_right))/self.points_num)

        self.normalize_mat_left=np.zeros([3,3])
        self.normalize_mat_right=np.zeros([3,3])
        self.normalize_mat_left[0,0]=s_left
        self.normalize_mat_left[1,1]=s_left
        self.normalize_mat_left[2,2]=1
        self.normalize_mat_left[0,2]=-self.x_center_left*s_left
        self.normalize_mat_left[1,2]=-self.y_center_left*s_left
        self.normalize_mat_right[0,0]=s_right
        self.normalize_mat_right[1,1]=s_right
        self.normalize_mat_right[2,2]=1
        self.normalize_mat_right[0,2]=-self.x_center_right*s_right
        self.normalize_mat_right[1,2]=-self.y_center_right*s_right

        self.data_left=self.normalize_mat_left @ self.data_left.T
        self.data_right=self.normalize_mat_right @ self.data_right.T

    def get_formula(self):
        self.formula_mat=np.zeros([self.points_num,9])
        for i in range(self.points_num):
            self.formula_mat[i,0]=self.data_right[0,i]*self.data_left[0,i]
            self.formula_mat[i,1]=self.data_right[0,i]*self.data_left[1,i]
            self.formula_mat[i,2]=self.data_right[0,i]
            self.formula_mat[i,3]=self.data_right[1,i]*self.data_left[0,i]
            self.formula_mat[i,4]=self.data_right[1,i]*self.data_left[1,i]
            self.formula_mat[i,5]=self.data_right[1,i]
            self.formula_mat[i,6]=self.data_left[0,i]
            self.formula_mat[i,7]=self.data_left[1,i]
            self.formula_mat[i,8]=1

    def SVD_get_F(self):
        _,_,Vt=np.linalg.svd(self.formula_mat)
        F_vec=(Vt.T)[:,-1]
        self.F=np.zeros([3,3])
        self.F[0,0]=F_vec[0]
        self.F[0,1]=F_vec[1]
        self.F[0,2]=F_vec[2]
        self.F[1,0]=F_vec[3]
        self.F[1,1]=F_vec[4]
        self.F[1,2]=F_vec[5]
        self.F[2,0]=F_vec[6]
        self.F[2,1]=F_vec[7]
        self.F[2,2]=F_vec[8]

    def add_constraint(self):
        U,S,Vt=np.linalg.svd(self.F)
        S_mat=np.zeros([3,3])
        S_mat[0,0]=S[0]
        S_mat[1,1]=S[1]
        self.F=U @ S_mat @ Vt

    def back_normalize(self):
        self.F=self.normalize_mat_right.T @ self.F @ self.normalize_mat_left

    def forward(self):
        self.normalize()
        self.get_formula()
        self.SVD_get_F()
        self.add_constraint()
        self.back_normalize()