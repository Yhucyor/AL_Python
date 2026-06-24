import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json 

from core.bfs import BFS1, BFS2
from core.puzzle import ma_tran_puzzle
def UIPuzzle():
    root = tk.Tk()
    root.title("BFS Puzzle 3x3")
    root.geometry("460x300+50+50")
    #I. <=== Thêm giao diện 
    #1. Thêm frame bên trái chứa Puzzle
    puzzle_frame = tk.Frame(root, bg = "lightgray", bd = 1, relief = "groove")
    puzzle_frame.grid(row = 0, column = 0, padx = 15, pady = 15, sticky = "nw")
    #2. Thêm Label tên ma trận
    puzzle_label = tk.Label(puzzle_frame, text = "<=== Trò chơi Puzzle 8 (3x3) ===>", font = ("Helvetica", 12, "bold"))
    puzzle_label.grid(row = 0)
    #3. Thêm các ô của ma trận
    grid_matrix = tk.Frame(puzzle_frame, bg = "lightgray")
    grid_matrix.grid(row = 1, column = 0)
    label_1 = tk.Label(grid_matrix, text = "1", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_2 = tk.Label(grid_matrix, text = "2", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_3 = tk.Label(grid_matrix, text = "3", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_4 = tk.Label(grid_matrix, text = "4", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_5 = tk.Label(grid_matrix, text = "5", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_6 = tk.Label(grid_matrix, text = "6", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_7 = tk.Label(grid_matrix, text = "7", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_8 = tk.Label(grid_matrix, text = "8", width = 6, height = 3, bd = 2, bg = "#228BE6", fg = "white", font = ("Helvetica", 10, "bold"))  
    label_empty = tk.Label(grid_matrix, text = "", width = 6, height = 3, bd = 2) 
    list_label = [label_empty, label_1, label_2, label_3, label_4, label_5, label_6, label_7, label_8]  
    def ve_ma_tran():
        for i in range(3): 
            for j in range(3):
                list_label[ma_tran_puzzle[i][j]].grid(row = i + 1, column = j, padx = 2, pady = 2, sticky = "nsew")
    ve_ma_tran()

    #4. Thêm ô nhập ma trận vào
    ma_tran_frame = tk.Frame(puzzle_frame, bg = "white")
    nhap_label = tk.Label(ma_tran_frame, text = "Nhập ma trận mới ở đây: ")
    nhap_label.grid(row = 0, column = 0, padx = 3, pady = 3, sticky = "w")

    def doi_ma_tran():
        global ma_tran_puzzle
        try:
            str_ma_tran = ma_tran_text.get("1.0", tk.END).strip()
            tmp_ma_tran = json.loads(str_ma_tran)
            if len(tmp_ma_tran) == 3 and all(len(r) == 3 for r in tmp_ma_tran):
                so = set(i for row in tmp_ma_tran for i in row)
                if so == set(range(9)):
                    ma_tran_puzzle =tmp_ma_tran
                    ve_ma_tran()
                    messagebox.showinfo("Thông báo", "Đổi ma trận thành công!")
                    return 
            raise ValueError
        except :
            messagebox.showinfo("Lỗi!", "Định dạng ma trận!")

    btn_doi = tk.Button(ma_tran_frame, text = "Đổi", command = doi_ma_tran)
    btn_doi.grid(row = 0, column = 1, sticky = "w")
    chuoi_hien_thi = json.dumps(ma_tran_puzzle)
    chuoi_hien_thi = chuoi_hien_thi.replace("], [", "], \n[")
    ma_tran_text = tk.Text(ma_tran_frame,width = 25, height = 3)
    ma_tran_text.grid(row = 1, column = 0, padx = 3, pady = 3, sticky = "nsew")
    ma_tran_text.insert("1.0", chuoi_hien_thi)
    
    ma_tran_frame.grid(row = 2, column = 0)
   

    #II. <=== Thêm bên bảng điều khiển ===>
    dashboard_frame = tk.Frame(root, bg = "lightgray", bd = 1, relief = "groove")
    dashboard_frame.grid(row = 0, column = 1, padx = 15, pady = 15, sticky = "nsew")
    #1. Thêm nhãn 
    bfs_label = tk.Label(dashboard_frame, text = "Chế độ BFS: ", fg="#1D4ED8", font=("Helvetica", 10, "bold"))
    bfs_label.grid(row = 0, column = 0, padx = 3, pady = 3, sticky = "nw")

    #2. Thêm Combo Box
    list_bfs = ["BFS1", "BFS2"]
    bfs_combobox = ttk.Combobox(dashboard_frame, values = list_bfs, state = "readonly",width = 5)
    bfs_combobox.current(0)
    bfs_combobox.grid(row = 0, column = 1, sticky = "nw")
    
    #3. Nút giải 
    tam_dung_giai = False
    def di_chuyen_tung_buoc(buoc_di, index = 0, chuoi_hien_tai = "Bắt dầu: "):
        global ma_tran_puzzle
        if tam_dung_giai:
            root.after(100, lambda: di_chuyen_tung_buoc(buoc_di, index, chuoi_hien_tai))
            return
        if index >= len(buoc_di):
            txt_duong_di.delete("1.0", tk.END)
            txt_duong_di.insert("1.0", chuoi_hien_tai + " --> END")
            return 
        huong = buoc_di[index]
        x, y = 0, 0
        for i in range(3):
            for j in range(3):
                if ma_tran_puzzle[i][j] == 0:
                    x, y = i, j
        dxy =  {"U":[-1, 0], "D": [1, 0], "R": [0, -1], "L": [0, 1]}
        new_x = x + dxy[huong][0]
        new_y = y + dxy[huong][1]
        ma_tran_puzzle[x][y], ma_tran_puzzle[new_x][new_y] = ma_tran_puzzle[new_x][new_y], ma_tran_puzzle[x][y]
        ve_ma_tran()

        #Chỉnh đường đi
        chuoi_hien_tai = chuoi_hien_tai + " -->" + huong
        txt_duong_di.delete("1.0", tk.END)
        txt_duong_di.insert("1.0", chuoi_hien_tai)

        #Thời gian
        try: 
            giay = float(txt_toc_do.get().strip())
            mili_giay = int(giay*1000)
        except:
            mili_giay = 500
        root.after(mili_giay, lambda: di_chuyen_tung_buoc(buoc_di, index + 1, chuoi_hien_tai))

    def giai_ma_tran():
        che_do = bfs_combobox.get()
        txt_duong_di.delete("1.0", tk.END)
        
        if che_do == "BFS1":
            sol = BFS1(ma_tran_puzzle)
        else:
            sol = BFS2(ma_tran_puzzle)
        
        if sol:
            txt_duong_di.insert("1.0", f"Bat dau:")
            buoc_di = []
            for i in sol.split("-->"):
                if i in ["U", "D", "L", "R"]:
                    buoc_di.append(i)
            di_chuyen_tung_buoc(buoc_di, 0, "Bắt đầu")
        else:
            txt_duong_di.insert("1.0", "Không tìm thấy đường đi")

    btn_giai = tk.Button(dashboard_frame, text = "Giải Ma Trận", command = giai_ma_tran, bg="#28A745", fg="white", font=("Helvetica", 10))
    btn_giai.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "nsew")
  
    #4. Tạm dừng thực hiện:
    def tam_dung():
        nonlocal tam_dung_giai
        tam_dung_giai = not(tam_dung_giai)
        if tam_dung_giai == True:
            btn_tam_dung.config(text = "Tiếp tục giải")
        else:
            btn_tam_dung.config(text = "Tạm dừng giải")

    btn_tam_dung = tk.Button(dashboard_frame, text = "Tạm dừng giải", command = tam_dung)
    btn_tam_dung.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "nsew")

    #5. Tốc độ giải: 
    label_toc_do = tk.Label(dashboard_frame, text = "  Tốc độ đi: ")
    label_toc_do.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "w")
    txt_toc_do = tk.Text(dashboard_frame, width = 4, height = 1)
    txt_toc_do.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "nsew")
    txt_toc_do.insert("1.0", "0.5")
    #6. Đường đi
    label_duong_di = tk.Label(dashboard_frame, text = "Đường đi: ", fg="purple", font=("Helvetica", 10))
    label_duong_di.grid(row = 4, column = 0, columnspan = 2, sticky = "nsew", padx = 5)

    #7. Thêm frame đương đi để kết hợp với scroll_ball
    duong_di_frame = tk.Frame(dashboard_frame)

    txt_duong_di = tk.Text(duong_di_frame, width = 15, height = 7)
    txt_duong_di.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

    scroll_ball = tk.Scrollbar(duong_di_frame, orient = tk.VERTICAL, command = txt_duong_di.yview)
    scroll_ball.pack(side = tk.RIGHT, fill = tk.Y)
    txt_duong_di.config(yscrollcommand = scroll_ball.set)

    duong_di_frame.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 4)
    root.resizable(False, False)
    tk.mainloop()
