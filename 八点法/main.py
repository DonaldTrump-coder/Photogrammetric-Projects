from eightpoints import eightpoints
import numpy as np

cal=eightpoints("left.txt","right.txt")
cal.forward()
print(cal.F)
data_left=np.zeros([3,cal.points_num])
data_right=np.zeros([3,cal.points_num])
with open("left.txt") as file:
    text=file.read().split('\n')
    for index in range(cal.points_num):
        point=text[index+1].split(' ')
        data_left[0,index]=float(point[0])
        data_left[1,index]=float(point[1])
        data_left[2,index]=1
with open("right.txt") as file:
    text=file.read().split('\n')
    for index in range(cal.points_num):
        point=text[index+1].split(' ')
        data_right[0,index]=float(point[0])
        data_right[1,index]=float(point[1])
        data_right[2,index]=1
result=[]
for i in range(cal.points_num):
    result.append(round(data_right[:,i].T @ cal.F @data_left[:,i],4))
print(np.array(result))