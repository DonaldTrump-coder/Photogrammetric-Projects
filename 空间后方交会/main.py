import adjustment
import numpy as np

adj=adjustment.adjustment(150,0,0)
adj.input_from_csv("data.csv")
adj.setup()
while adj.left_stop is False or adj.right_stop is False:
    adj.forward()
    adj.backward()
    adj.whether_to_stop()
adj.judge_accuracy()
print(f"左片单位权中误差为：{adj.delta_left[0,0]:.6f}m,右片单位权中误差为：{adj.delta_right[0,0]:.6f}m")
print("左片外方位元素：")
print(f"Xs:{adj.X_left:.6f}m,Ys:{adj.Y_left:.6f}m,Zs:{adj.Z_left:.6f}m,fai:{adj.phi_left:.6f},w:{adj.omiga_left:.6f},k:{adj.kappa_left:.6f}")
print("左片外方位元素的精度：")
print(f"mXs:{np.sqrt(adj.variation_mat_left[0,0]):.6f}m,mYs:{np.sqrt(adj.variation_mat_left[1,1]):.6f}m,mZs:{np.sqrt(adj.variation_mat_left[2,2]):.6f}m,mfai:{np.sqrt(adj.variation_mat_left[3,3]):.6f},mw:{np.sqrt(adj.variation_mat_left[4,4]):.6f},mk:{np.sqrt(adj.variation_mat_left[5,5]):.6f}")
print("右片外方位元素：")
print(f"Xs:{adj.X_right:.6f}m,Ys:{adj.Y_right:.6f}m,Zs:{adj.Z_right:.6f}m,fai:{adj.phi_right:.6f},w:{adj.omiga_right:.6f},k:{adj.kappa_right:.6f}")
print("右片外方位元素的精度：")
print(f"mXs:{np.sqrt(adj.variation_mat_right[0,0]):.6f}m,mYs:{np.sqrt(adj.variation_mat_right[1,1]):.6f}m,mZs:{np.sqrt(adj.variation_mat_right[2,2]):.6f}m,mfai:{np.sqrt(adj.variation_mat_right[3,3]):.6f},mw:{np.sqrt(adj.variation_mat_right[4,4]):.6f},mk:{np.sqrt(adj.variation_mat_right[5,5]):.6f}")