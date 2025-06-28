from forward import forward
import numpy as np
from adjustment import adjustment

adj=adjustment(150,0,0)
adj.input_from_csv("data.csv")
adj.setup()
while adj.left_stop is False or adj.right_stop is False:
    adj.forward()
    adj.backward()
    adj.whether_to_stop()

forwards=forward(5)
forwards.setup("data.txt")
forwards.forward(adj.X_left,adj.Y_left,adj.Z_left,adj.X_right,adj.Y_right,adj.Z_right,adj.phi_left,adj.omiga_left,adj.kappa_left,adj.phi_right,adj.omiga_right,adj.kappa_right)

print(f"点号：1，X:{round(forwards.result[0,0],3)}，Y：{round(forwards.result[1,0],3)}，Z:{round(forwards.result[2,0],3)}")
print(f"点号：2，X:{round(forwards.result[0,1],3)}，Y：{round(forwards.result[1,1],3)}，Z:{round(forwards.result[2,1],3)}")
print(f"点号：3，X:{round(forwards.result[0,2],3)}，Y：{round(forwards.result[1,2],3)}，Z:{round(forwards.result[2,2],3)}")
print(f"点号：4，X:{round(forwards.result[0,3],3)}，Y：{round(forwards.result[1,3],3)}，Z:{round(forwards.result[2,3],3)}")
print(f"点号：5，X:{round(forwards.result[0,4],3)}，Y：{round(forwards.result[1,4],3)}，Z:{round(forwards.result[2,4],3)}")