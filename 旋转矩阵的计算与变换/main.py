import matrix2angle, matrix2quaternion
import numpy as np

input_mat=np.array([[0.4330127, -0.43559574, 0.78914913], 
                  [0.75, 0.65973961, -0.04736717], 
                  [-0.5, 0.61237244, 0.61237244]])

result=matrix2angle.mat2ang_XYZ(input_mat)
resultlist=[]
for item in result:
    resultlist.append(round(float(item),8))
print(f"恢复的XYZ欧拉角：{resultlist}")

result=matrix2angle.mat2ang_ZYZ(input_mat)
resultlist=[]
for item in result:
    resultlist.append(round(float(item),8))
print(f"恢复的ZYZ欧拉角：{resultlist}")

result=matrix2angle.mat2ang_ZYX(input_mat)
resultlist=[]
for item in result:
    resultlist.append(round(float(item),8))
print(f"恢复的ZYX欧拉角：{resultlist}")

result=matrix2quaternion.mat2quat(input_mat)
resultlist=[]
for item in result:
    resultlist.append(round(float(item),8))
print(f"单位四元数：{resultlist}")

result=matrix2angle.mat2ang_YXZ(input_mat)
resultlist=[]
for item in result:
    resultlist.append(round(float(item),8))
print(f"恢复的YXZ欧拉角：{resultlist}")

check1=np.tan(matrix2angle.mat2ang_XYZ(input_mat)[0])/-np.tan(matrix2angle.mat2ang_YXZ(input_mat)[0])
check2=np.sin(matrix2angle.mat2ang_YXZ(input_mat)[1])/-np.sin(matrix2angle.mat2ang_XYZ(input_mat)[1])
print(f"程序验证的两者差值：{round(check1-check2,10)}")