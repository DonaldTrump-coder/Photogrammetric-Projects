import numpy as np

def mat2ang_XYZ(mat:np.ndarray):
    alpha=np.atan2(mat[2,1],mat[2,2])
    beta=np.arcsin(-mat[2,0])
    gamma=np.atan2(mat[1,0],mat[0,0])
    return alpha, beta, gamma

def mat2ang_ZYX(mat:np.ndarray):
    psi=np.atan2(mat[0,1],mat[0,0])
    theta=np.arcsin(-mat[0,2])
    phi=np.atan2(mat[1,2],mat[2,2])
    return psi, theta, phi

def mat2ang_ZYZ(mat:np.ndarray):
    alpha=np.atan2(mat[2,1],-mat[2,0])
    beta=np.arccos(mat[2,2])
    gamma=np.atan2(mat[1,2],mat[0,2])
    return alpha, beta, gamma

def mat2ang_YXZ(mat:np.ndarray):
    phi=np.atan2(-mat[2,0],mat[2,2])
    omiga=np.arcsin(mat[2,1])
    kappa=np.atan2(-mat[0,1],mat[1,1])
    return phi,omiga,kappa

if __name__ == "__main__":
    mat=np.array([[0.4330127, -0.43559574, 0.78914913], 
                  [0.75, 0.65973961, -0.04736717], 
                  [-0.5, 0.61237244, 0.61237244]])
    print(mat2ang_ZYZ(mat))