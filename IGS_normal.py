# 讀取檔案並秀出
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_iges_file

shapes = read_iges_file(r"C:\alan\ITRI\model\cube.IGS")
# 初始化 3D 顯示環境
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(shapes, update=True)
start_display()

## 讀取檔案後計算每個面的法向量 以及 最大跟最小曲率
# import os
# from OCC.Core.IGESControl import IGESControl_Reader
# from OCC.Core.TopExp import TopExp_Explorer
# from OCC.Core.TopoDS import topods_Face
# from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
# from OCC.Core.BRepLProp import BRepLProp_SLProps
# from OCC.Core.TopAbs import TopAbs_FACE
# from OCC.Core.gp import gp_Pnt2d

# # IGS檔案路徑
# file_path = r"C:\alan\ITRI\model\AnyConv.com__AnyConv.com__cube.iges"

# # 確認文件是否存在
# if not os.path.exists(file_path):
#     print("檔案路徑錯誤！")
# else:
#     # 讀取檔案
#     reader = IGESControl_Reader()
#     reader.ReadFile(file_path)
#     reader.TransferRoots()          # 使用 TransferRoots 方法轉換模型數據
#     shape = reader.Shape()          # 獲取模型的形狀

#     # 找所有的面
#     explorer = TopExp_Explorer(shape, TopAbs_FACE)
#     while explorer.More():
#         face = topods_Face(explorer.Current())               # 獲取當前的面 explorer.Current()
#         adaptor_surface = BRepAdaptor_Surface(face, True)    # 創建一個物件用於分析面的幾何特性
#         props = BRepLProp_SLProps(adaptor_surface, 2, 0.01)  # 用於獲取面的曲率信息，2 表示計算主曲率，也就是曲面在特定點的最大和最小曲率，0.01控制計算精度
#         u_min, u_max, v_min, v_max = adaptor_surface.FirstUParameter(), adaptor_surface.LastUParameter(), adaptor_surface.FirstVParameter(), adaptor_surface.LastVParameter()
#         u_mid = (u_min + u_max) / 2 
#         v_mid = (v_min + v_max) / 2                          # 計算面的中心點坐標
#         props.SetParameters(u_mid, v_mid)                    # 設置曲率計算的參數，到時候求出法向量就為該點的向量
#         if props.IsCurvatureDefined():                       # 檢查曲率是否被定義
#             max_curvature = props.MaxCurvature()             # 最大曲率
#             min_curvature = props.MinCurvature()             # 最小曲率
#             print("最大曲率:", max_curvature)
#             print("最小曲率:", min_curvature)
#             normal = props.Normal()                          # 計算該點的法向量
#             # 如果面朝向是反的，反轉法向量
#             if face.Orientation() == TopAbs_FACE:            # 檢查面的朝向是否為反向
#                 normal.Reverse()
#             print("法向量:", normal.X(), normal.Y(), normal.Z())
#         explorer.Next()                                      # 進入下一個面

# ## 同樣是計算法向量，不過多了把它畫出來的功能
# import os
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from OCC.Core.IGESControl import IGESControl_Reader
# from OCC.Core.TopExp import TopExp_Explorer
# from OCC.Core.TopoDS import topods_Face
# from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
# from OCC.Core.BRepLProp import BRepLProp_SLProps
# from OCC.Core.TopAbs import TopAbs_FACE
# from OCC.Core.gp import gp_Pnt2d

# # 先創建 figure 準備後續的可視化
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # 檔案路徑
# file_path = r"C:\NTHU\IRTI-Project\my_cylinder.igs"

# # 確認路徑是否存在
# if not os.path.exists(file_path):
#     print("檔案路徑錯誤！")
# else:
#     # 讀取檔案
#     reader = IGESControl_Reader()
#     reader.ReadFile(file_path)
#     reader.TransferRoots()
#     shape = reader.Shape()

#     # 迴圈跑過所有面
#     explorer = TopExp_Explorer(shape, TopAbs_FACE)
#     while explorer.More():
#         face = topods_Face(explorer.Current())
#         adaptor_surface = BRepAdaptor_Surface(face, True)
#         props = BRepLProp_SLProps(adaptor_surface, 2, 0.01)
#         u_min, u_max, v_min, v_max = adaptor_surface.FirstUParameter(), adaptor_surface.LastUParameter(), adaptor_surface.FirstVParameter(), adaptor_surface.LastVParameter()
#         u_mid = (u_min + u_max) / 2
#         v_mid = (v_min + v_max) / 2
#         props.SetParameters(u_mid, v_mid)
#         if props.IsCurvatureDefined():
#             normal = props.Normal()
            
#             if face.Orientation() == TopAbs_FACE:
#                 normal.Reverse()
#             print("法向量:", normal.X(), normal.Y(), normal.Z())

#             # 得到面中心點的值
#             center = adaptor_surface.Value(u_mid, v_mid)
#             # 繪製箭頭
#             ax.quiver(center.X(), center.Y(), center.Z(), normal.X(), normal.Y(), normal.Z(), length=5, color='r')

#         explorer.Next()

# # 設置 X Y Z 軸
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()