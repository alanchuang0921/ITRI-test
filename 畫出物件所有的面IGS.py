# # ## 將物件中所有面都畫出來
# import time
# from OCC.Display.SimpleGui import init_display
# from OCC.Core.IGESControl import IGESControl_Reader
# from OCC.Core.TopExp import TopExp_Explorer
# from OCC.Core.TopoDS import topods_Face
# from OCC.Core.TopAbs import TopAbs_FACE

# # 初始化 3D 顯示環境
# display, start_display, add_menu, add_function_to_menu = init_display()

# # IGS檔案路徑
# file_path = r"C:\alan\ITRI\model\cylinder.IGS"

# # 讀取檔案
# reader = IGESControl_Reader()
# status = reader.ReadFile(file_path)
# if status == 1:  # 確認文件是否存在
#     reader.TransferRoots()
#     shape = reader.Shape()

#     # 找所有的面
#     explorer = TopExp_Explorer(shape, TopAbs_FACE)
#     while explorer.More():
#         face = topods_Face(explorer.Current())

#         # 清除當前顯示
#         display.EraseAll()

#         # 顯示目前的面
#         display.DisplayShape(face, update=True)
#         display.FitAll()

#         time.sleep(2)  # 暫停兩秒

#         # 移動到下一個面
#         explorer.Next()
# else:
#     print("Failed to read the file.")

# # 啟動 OCC 視窗
# start_display()


## 將物件中所有面畫出來並儲存
import os
import time
from OCC.Display.SimpleGui import init_display
from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods_Face
from OCC.Core.TopAbs import TopAbs_FACE

display, start_display, add_menu, add_function_to_menu = init_display()

file_path = r"C:\alan\ITRI\model\cube.IGS"

# 影像的保存路徑
image_directory = r"C:\alan\ITRI\images"
if not os.path.exists(image_directory):
    os.makedirs(image_directory)


reader = IGESControl_Reader()
status = reader.ReadFile(file_path)
if status == 1:  
    reader.TransferRoots()
    shape = reader.Shape()

    index = 1
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face = topods_Face(explorer.Current())

        display.EraseAll()

        display.DisplayShape(face, update=True, color='BLUE', transparency=0.5)  # 可以調整顏色和透明度
        display.FitAll()

        time.sleep(2)  # 暫停兩秒

        # 儲存每個面的影像
        image_path = os.path.join(image_directory, f'face_{index}.png')
        display.View.Dump(image_path)
        print(f'Saved image of face {index} to {image_path}')

        # 移動到下一個面
        index += 1
        explorer.Next()
else:
    print("Failed to read the file.")
start_display()

# ## 去計算每個面的一些資訊(面積，上下界，面的類型)
# import os
# import time
# from OCC.Display.SimpleGui import init_display
# from OCC.Core.IGESControl import IGESControl_Reader
# from OCC.Core.TopExp import TopExp_Explorer
# from OCC.Core.TopoDS import topods_Face
# from OCC.Core.TopAbs import TopAbs_FACE
# from OCC.Core.BRepTools import breptools_UVBounds
# from OCC.Core.GeomLProp import GeomLProp_SLProps
# from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
# from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
# from OCC.Core.GProp import GProp_GProps
# from OCC.Core.gp import gp_Pnt

# file_path = r"C:\alan\ITRI\model\cylinder.IGS"

# reader = IGESControl_Reader()
# status = reader.ReadFile(file_path)
# if status == 1: 
#     reader.TransferRoots()
#     shape = reader.Shape()

#     index = 1
#     explorer = TopExp_Explorer(shape, TopAbs_FACE)
#     while explorer.More():
#         face = topods_Face(explorer.Current())
        
#         adaptor_surface = BRepAdaptor_Surface(face, True)
#         surface_type = adaptor_surface.GetType()              # 獲取面的類型
    
#         # 獲取面的邊界
#         u_min, u_max, v_min, v_max = adaptor_surface.FirstUParameter(), adaptor_surface.LastUParameter(), adaptor_surface.FirstVParameter(), adaptor_surface.LastVParameter()
    
#         # 計算面積
#         gprops = GProp_GProps()                             # 用於獲取面的質量等信息
#         brepgprop_SurfaceProperties(face, gprops)           # 計算面的面積
#         area = gprops.Mass()                                # 獲取面的面積

#         print(f"Face {index}:")
#         print(f"  Type: {surface_type}")
#         print(f"  Bounds in U: {u_min} to {u_max}")
#         print(f"  Bounds in V: {v_min} to {v_max}")
#         print(f"  Area: {area}")

#         index += 1
#         explorer.Next()