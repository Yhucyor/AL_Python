def solution(node):
    danh_sach_node = []
    node_hien_tai = node
    while node_hien_tai is not None:
        danh_sach_node.append(node_hien_tai)
        node_hien_tai = node_hien_tai.parent
    return danh_sach_node[::-1]
