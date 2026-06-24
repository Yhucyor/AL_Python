ma_tran_puzzle = [[1, 2, 4], 
                  [5, 6, 7], 
                  [8, 3, 0]]

def solution(node):
    duong_di = "END"
    node_hien_tai = node
    while node_hien_tai != "_":
        if node_hien_tai.action != "_":
            duong_di = node_hien_tai.action + "-->" + duong_di
        node_hien_tai = node_hien_tai.parent
    return duong_di 