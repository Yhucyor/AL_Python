from core import globals as g

def solution(node):
    danh_sach_node = []
    node_hien_tai = node
    while node_hien_tai is not None:
        danh_sach_node.append(node_hien_tai)
        node_hien_tai = node_hien_tai.parent
    return danh_sach_node[::-1]


    #Hàm tính chi phí
def manhattan(matrix):
    val = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if matrix[i][j] != 0:
                for ix in range(0, 3):
                    for jy in range(0, 3):
                        if matrix[i][j] == g.goal_ma_tran[ix][jy]:
                            val += abs(i-ix) + abs(j - jy)
    return val