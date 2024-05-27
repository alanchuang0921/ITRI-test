from OCC.Core.gp import gp_Pnt
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir,gp_Circ, gp_Ax2, gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,BRepBuilderAPI_MakeFace
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Display.SimpleGui import init_display
import numpy as np
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp_Trsf,gp_Pnt,gp_Vec
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.IGESControl import IGESControl_Reader
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Extend.DataExchange import write_iges_file
import os
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Extend.DataExchange import read_iges_file

def grinding_area(point_start,point_end,normal_vector):
    #根據起始、終點生成線段
    point_s=gp_Pnt(float(point_start[0]),float(point_start[1]), float(point_start[2]))
    point_e=gp_Pnt(float(point_end[0]),float(point_end[1]), float(point_end[2]))
    aSegment = GC_MakeSegment(point_s, point_e )
    anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
    aWire = BRepBuilderAPI_MakeWire(anEdge.Edge())

    #input
    #normal_vector
    magnitude = np.linalg.norm(normal_vector)# 將法向量除以其範數以得到單位法向量
    normal_vector = normal_vector/ magnitude

    #two point_position
    tan_vector=point_start-point_end

    #direction_1
    dir_1= np.cross(normal_vector, tan_vector)
    magnitude = np.linalg.norm(dir_1)# 將向量除以其範數以得到單位向量
    dir_1 = dir_1/ magnitude

    # 定義截面為方形
    # 定義方形的四個頂點
    depth=2#每次研磨深度
    width=20#研磨寬度
    point_1=point_start+normal_vector*depth+dir_1*width
    point_2=point_start+normal_vector*depth-dir_1*width
    point_3=point_start-normal_vector*depth-dir_1*width
    point_4=point_start-normal_vector*depth+dir_1*width
    p1 = gp_Pnt(point_1[0], point_1[1], point_1[2])
    p2 = gp_Pnt(point_2[0], point_2[1], point_2[2])
    p3 = gp_Pnt(point_3[0], point_3[1], point_3[2])
    p4 = gp_Pnt(point_4[0], point_4[1], point_4[2])

    # 使用這些頂點創建方形的邊緣
    edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()

    # 使用這些邊緣創建方形的線框
    square_wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

    # 將線框轉換為面，作為截面
    F = BRepBuilderAPI_MakeFace(square_wire, True)
    S=BRepOffsetAPI_MakePipe(aWire.Wire(), F.Shape())#第一个参数轨迹线,第二个参数是轮廟

    return S.Shape()

def zoom(model,m_center,mag):
    t1 = gp_Trsf()
    #物件質心位置,單位mm
    t1.SetScale(m_center, mag)

    # 对形状进行缩放
    scaled_box = BRepBuilderAPI_Transform(model, t1, True).Shape()


    # display, start_display, add_menu, add_function_to_menu = init_display()
    # display.DisplayShape(scaled_box, update=True, color=rgb_color(0, 0, 0))
    # display.DisplayShape(model, update=True, color=rgb_color(1, 0, 0))
    # start_display()
    return scaled_box

def grind(model,S):
    # 创建一个几何切割对象
    cut_algo = BRepAlgoAPI_Cut(model,S)
    # 执行几何切割操作
    cut_result = cut_algo.Shape()
    return cut_result


def calculate_surface_area(shape):
    # 將 shape 轉換為 TopoDS_Shape
    topods_shape = TopoDS_Shape(shape)

    # 初始化表面屬性
    surface_props = GProp_GProps()

    # 計算表面屬性
    brepgprop_SurfaceProperties(topods_shape, surface_props)
    
    # 獲取表面積
    surface_area = surface_props.Mass()

    return surface_area



points = []  # 创建一个空列表来存储解析后的reward值
with open(r"C:\alan\ITRI\trajectory\simple_1.txt", "r") as file:
    for line in file:
        # 输出每一行内容，以确保正确读取
        print("Line:", line)
        try:
            # 从每一行中解析出8个值
            face, trajc, x, y, z, rx, ry, rz = line.split()
            # 将解析后的值作为一个元组添加到rewards列表中
            points.append((face, trajc, x, y, z, rx, ry, rz))
        except ValueError:
            # 如果发生拆包错误，输出错误信息
            print("Error: Unable to unpack values from line:", line)

max_value_a = max(int(point[0]) for point in points)
# print("Maximum value of point[1]:", max_value_a)
max_value_b = max(int(point[1]) for point in points)

for a in range(1, max_value_a+1): 
    same_surface_points = [point for point in points if float(point[0]) ==  a]#提取同一面上的點
    # same_surface_points=[point for point in points if point[0] == '2']#提取同一面上的點
    for b in range(1, max_value_b+1): 
        same_path_points = [point for point in same_surface_points if float(point[1]) ==  b]#提取同一路徑上的點
        #same_path_points = [point for point in same_surface_points if point[1] == '1']#提取同一路徑上的點
        for i, point in enumerate(same_path_points):
            point = [float(item) for item in point]  # 将字符串转换为浮点数
            # print("Current Point:", point)
            
            point_end=np.array((point[2],point[3],point[4]))
            # print(point_end)
            normal_vector=np.array((point[5],point[6],point[7]))
            if i > 0:
                previous_point = [float(item) for item in same_path_points[i - 1]]  # 获取前一个 point 的信息
                # print("Previous Point:", previous_point)
                point_start=np.array((previous_point[2],previous_point[3],previous_point[4]))
                print(point_start)
                S=grinding_area(point_start,point_end,normal_vector)#生成研磨範圍

                if i==1:
                    path_result=S
                    # all_result = all_result.Shape()
                else:
                    path_result = BRepAlgoAPI_Fuse(path_result,S)
                    path_result = path_result.Shape()
        if b==1:
            surface_result=path_result
            # all_result = all_result.Shape()
        else:
            surface_result = BRepAlgoAPI_Fuse(path_result,surface_result)
            surface_result = surface_result.Shape()
    if a==1:
        all_grind_area=surface_result
        # all_result = all_result.Shape()
    else:
        all_grind_area = BRepAlgoAPI_Fuse(all_grind_area,surface_result)
        all_grind_area = all_grind_area.Shape()

#讀取模型
iges_file =  r"C:\alan\ITRI\model\simple_1.igs"
model = read_iges_file(iges_file)
display, start_display, add_menu, add_function_to_menu = init_display()
display.DisplayShape(model, update=True)[0]
start_display()

layer_n=5
# point_start=np.array((-40,50,0))
# point_end=np.array((40,50,0))
# normal_vector=np.array((0,1,0))
# S=grinding_area(point_start,point_end,normal_vector)#生成研磨範圍
m_center= gp_Pnt(0,0,0)#質心位置
#simple_1:m_center=(0,0,0)
#simple_2:m_center=(0,-2.2,-2.2)
#simple_3:m_center=(-0.36,-0.76,-0.36)
#complex_3:m_center= gp_Pnt(0, 0, 61.5)

i=0
while i<layer_n:
    mag=1-i*0.01
    Model=zoom(model,m_center,mag)
    cut_result=grind(Model,all_grind_area)
    
    surface_origin = calculate_surface_area(Model)
    surface_cut_result=calculate_surface_area(cut_result)


    if i==0:
        all_result=cut_result
        # all_result = all_result.Shape()
    else:
        all_result = BRepAlgoAPI_Fuse(all_result,cut_result)
        all_result = all_result.Shape()

    iges_file_path=os.path.join(r"C:\alan\ITRI\cut_result",f'layer_{i}.igs' )
    write_iges_file(cut_result, iges_file_path)


    # if surface_origin== surface_cut_result:
    #     break

    i=i+1

iges_file_path=os.path.join(r"C:\alan\ITRI\cut_result\all.igs" )
write_iges_file(all_result, iges_file_path)