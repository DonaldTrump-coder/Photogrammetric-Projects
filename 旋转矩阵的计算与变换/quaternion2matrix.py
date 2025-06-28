import numpy as np

def quat2mat(quat:np.ndarray):
    w=quat[0]
    x=quat[1]
    y=quat[2]
    z=quat[3]
    mat=np.zeros([3,3])
    mat[0,0]=1-2*y*y-2*z*z
    mat[0,1]=2*x*y-2*w*z
    mat[0,2]=2*x*z+2*w*y
    mat[1,0]=2*x*y+2*w*z
    mat[1,1]=1-2*x*x-2*z*z
    mat[1,2]=2*y*z-2*w*x
    mat[2,0]=2*x*z-2*w*y
    mat[2,1]=2*y*z+2*w*x
    mat[2,2]=1-2*x*x-2*y*y
    return mat

if __name__ == "__main__":
    quat=np.array([0.82236317,0.20056212,0.39190384,0.36042341])
    print(quat2mat(quat))