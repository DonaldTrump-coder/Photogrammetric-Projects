import numpy as np

def mat2quat(mat:np.ndarray):
    w=np.sqrt(1+mat[0,0]+mat[1,1]+mat[2,2])/2
    x=(mat[2,1]-mat[1,2])/(4*w)
    y=(mat[0,2]-mat[2,0])/(4*w)
    z=(mat[1,0]-mat[0,1])/(4*w)
    return w, x, y, z

if __name__ == "__main__":
    mat=np.array([[0.4330127, -0.43559574, 0.78914913], 
                  [0.75, 0.65973961, -0.04736717], 
                  [-0.5, 0.61237244, 0.61237244]])
    print(mat2quat(mat))