import numpy as np

def ang2mat_XYZ(angle:np.ndarray):
    alpha=angle[0]
    beta=angle[1]
    gamma=angle[2]
    mat=np.zeros([3,3])
    mat[0,0]=np.cos(gamma)*np.cos(beta)
    mat[0,1]=np.cos(gamma)*np.sin(beta)*np.sin(alpha)-np.sin(gamma)*np.cos(alpha)
    mat[0,2]=np.cos(gamma)*np.sin(beta)*np.cos(alpha)+np.sin(gamma)*np.sin(alpha)
    mat[1,0]=np.sin(gamma)*np.cos(beta)
    mat[1,1]=np.sin(gamma)*np.sin(beta)*np.sin(alpha)+np.cos(gamma)*np.cos(alpha)
    mat[1,2]=np.sin(gamma)*np.sin(beta)*np.cos(alpha)-np.cos(gamma)*np.sin(alpha)
    mat[2,0]=-np.sin(beta)
    mat[2,1]=np.cos(beta)*np.sin(alpha)
    mat[2,2]=np.cos(beta)*np.cos(alpha)
    return mat

def ang2mat_ZYX(angle:np.ndarray):
    psi=angle[0]
    theta=angle[1]
    phi=angle[2]
    mat=np.zeros([3,3])
    mat[0,0]=np.cos(theta)*np.cos(psi)
    mat[0,1]=np.cos(theta)*np.sin(psi)
    mat[0,2]=-np.sin(theta)
    mat[1,0]=np.sin(phi)*np.sin(theta)*np.cos(psi)-np.cos(phi)*np.sin(psi)
    mat[1,1]=np.sin(phi)*np.sin(theta)*np.sin(psi)+np.cos(phi)*np.cos(psi)
    mat[1,2]=np.sin(phi)*np.cos(theta)
    mat[2,0]=np.cos(phi)*np.sin(theta)*np.cos(psi)+np.sin(phi)*np.sin(psi)
    mat[2,1]=np.cos(phi)*np.sin(theta)*np.sin(psi)-np.sin(phi)*np.cos(psi)
    mat[2,2]=np.cos(phi)*np.cos(theta)
    return mat

def ang2mat_ZYZ(angle:np.ndarray):
    alpha=angle[0]
    beta=angle[1]
    gamma=angle[2]
    mat=np.zeros([3,3])
    mat[0,0]=np.cos(gamma)*np.cos(beta)*np.cos(alpha)-np.sin(gamma)*np.sin(alpha)
    mat[0,1]=-np.cos(gamma)*np.cos(beta)*np.sin(alpha)-np.sin(gamma)*np.cos(alpha)
    mat[0,2]=np.cos(gamma)*np.sin(beta)
    mat[1,0]=np.sin(gamma)*np.cos(beta)*np.cos(alpha)+np.cos(gamma)*np.sin(alpha)
    mat[1,1]=-np.sin(gamma)*np.cos(beta)*np.sin(alpha)+np.cos(gamma)*np.cos(alpha)
    mat[1,2]=np.sin(gamma)*np.sin(beta)
    mat[2,0]=-np.sin(beta)*np.cos(alpha)
    mat[2,1]=np.sin(beta)*np.sin(alpha)
    mat[2,2]=np.cos(beta)
    return mat

if __name__ == "__main__":
    angle=np.array([0.88607712,0.91173829,-0.05995117])
    print(ang2mat_ZYZ(angle))
    print(ang2mat_XYZ(np.array([0.78539816,0.52359878,1.04719755])))
    print(ang2mat_ZYX(np.array([-0.78837192,-0.90942244,-0.07719656])))