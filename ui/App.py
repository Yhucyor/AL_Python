import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json 
import threading
#Thêm thuật toán 
from core.Algorithm import BFS1, BFS2, DFS, IDS, UCS, Greedy_Search, A_Star, IDA, SHC, SHC_Highest, stochastics_hill_climbing, random_restart_hill_climbing, local_beam_search

from core import globals as g

def UIPuzzle():
    root = tk.Tk()
    root.title("Puzzle 3x3")
    root.geometry("460x570+50+50")
    #I. <=== Thêm giao diện 
    main_frame = tk.Frame(root, bg = "lightgray")
    main_frame.pack(padx = 5, pady = 5, fill = tk.BOTH, expand = True)
    #1. Thêm frame bên trái chứa Puzzle
    puzzle_frame = tk.Frame(main_frame, bg = "lightgray", bd = 1, relief = "groove")
    puzzle_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nsew")
    #2. Thêm Label tên ma trận
    puzzle_label = tk.Label(puzzle_frame, text = "<=== Trò chơi Puzzle 8 (3x3) ===>", font = ("Helvetica", 12, "bold"))
    puzzle_label.grid(row = 0)
    #3. Thêm các ô của ma trận
    grid_matrix = tk.Frame(puzzle_frame, bg = "lightgray")
    grid_matrix.grid(row = 1, column = 0)
    label_1 = tk.Label(grid_matrix, text = "1", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_2 = tk.Label(grid_matrix, text = "2", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_3 = tk.Label(grid_matrix, text = "3", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_4 = tk.Label(grid_matrix, text = "4", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_5 = tk.Label(grid_matrix, text = "5", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_6 = tk.Label(grid_matrix, text = "6", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_7 = tk.Label(grid_matrix, text = "7", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_8 = tk.Label(grid_matrix, text = "8", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold"))  
    label_empty = tk.Label(grid_matrix, text = "", width = 6, height = 3, bd = 2, relief="ridge", font=("Arial",14,"bold")) 
    list_label = [label_empty, label_1, label_2, label_3, label_4, label_5, label_6, label_7, label_8]  
    def ve_ma_tran():
        for i in range(3): 
            for j in range(3):
                list_label[g.ma_tran_puzzle[i][j]].grid(row = i + 1, column = j, padx = 2, pady = 2, sticky = "nsew")
    ve_ma_tran()

    #4. Thêm ô nhập ma trận vào
    ma_tran_frame = tk.Frame(puzzle_frame, bg = "white")
    nhap_label = tk.Label(ma_tran_frame, text = "Nhập ma trận mới ở đây: ")
    nhap_label.grid(row = 0, column = 0, padx = 3, pady = 3, sticky = "w")

    def doi_ma_tran():
        try:
            str_ma_tran = ma_tran_text.get("1.0", tk.END).strip()
            tmp_ma_tran = json.loads(str_ma_tran)
            if len(tmp_ma_tran) == 3 and all(len(r) == 3 for r in tmp_ma_tran):
                so = set(i for row in tmp_ma_tran for i in row)
                if so == set(range(9)):
                    g.ma_tran_puzzle = tmp_ma_tran
                    ve_ma_tran()
                    messagebox.showinfo("Thông báo", "Đổi ma trận thành công!")
                    return 
            raise ValueError
        except :
            messagebox.showinfo("Lỗi!", "Định dạng ma trận!")

    btn_doi = tk.Button(ma_tran_frame, text = "Đổi", command = doi_ma_tran)
    btn_doi.grid(row = 0, column = 1, sticky = "w")
    chuoi_hien_thi = json.dumps(g.ma_tran_puzzle)
    chuoi_hien_thi = chuoi_hien_thi.replace("], [", "], \n[")
    ma_tran_text = tk.Text(ma_tran_frame,width = 25, height = 3)
    ma_tran_text.grid(row = 1, column = 0, padx = 3, pady = 3, sticky = "nsew")
    ma_tran_text.insert("1.0", chuoi_hien_thi)
    
    ma_tran_frame.grid(row = 2, column = 0)
   

    #II. <=== Thêm bên bảng điều khiển ===>
    dashboard_frame = tk.Frame(main_frame, bg = "lightgray", bd = 1, relief = "groove")
    dashboard_frame.grid(row = 0, column = 1, padx = 11, pady = 5, sticky = "nsew")
    #1. Thêm nhãn 
    bfs_label = tk.Label(dashboard_frame, text = "Chế độ: ")
    #bfs_label.grid(row = 0, column = 0, padx = 1, pady = 7, sticky = "nw")

    #2. Thêm Combo Box
    #Thêm thuật toán 
    list_bfs = ["Breadth-First Search 1", "Breadth-First Search 2", "Depth-First Search", "Iterative Deepening Search", "Uniform Cost Search", "Greedy Best-First Search", "A* Search", "Iterative Deepening A*", "Simple Hill Climbing", "Steepest-Ascent Hill Climbing",
                "Stochastic Hill Climbing", "Random-Restart Hill Climbing", "Local Beam Search"]
    bfs_combobox = ttk.Combobox(dashboard_frame, values = list_bfs, state = "readonly",width = 21)
    bfs_combobox.current(0)
    bfs_combobox.grid(row = 0, column = 0, columnspan = 2,  padx = 1, pady = 7, sticky = "nw")
    
    #3. Nút giải 
    # Bên trong UIPuzzle
    is_solving = {"value": False} 
    def run_solver(che_do):
        is_solving["value"] = True
        g.tk_da_duyet = 0
        g.tk_sinh_ra = 0

        solvers = {"Breadth-First Search 1": BFS1, "Breadth-First Search 2": BFS2, "Depth-First Search": DFS, "Iterative Deepening Search": IDS, "Uniform Cost Search": UCS, "Greedy Best-First Search": Greedy_Search, "A* Search": A_Star, "Iterative Deepening A*": IDA, "Simple Hill Climbing": SHC, "Steepest-Ascent Hill Climbing": SHC_Highest,
                   "Stochastic Hill Climbing": stochastics_hill_climbing, "Random-Restart Hill Climbing": random_restart_hill_climbing, "Local Beam Search": local_beam_search}        
        sol = solvers[che_do](g.ma_tran_puzzle)

        # Cập nhật GUI sau khi xong
        root.after(0, lambda: update_after_solve(sol, che_do))

    def update_after_solve(sol, che_do):
        if sol:
            root.after(0, lambda: so_buoc.config(text=f"Số bước đi: {len(sol)-1}"))
            root.after(0, lambda: do_sau.config(text=f"Độ sâu: {len(sol)-1}"))
            root.after(0, lambda: da_duyet.config(text=f"Đã duyệt: {g.tk_da_duyet}"))
            root.after(0, lambda: sinh_ra.config(text=f"Sinh ra: {g.tk_sinh_ra}"))
            root.after(0, lambda: di_chuyen_tung_buoc(sol, 0, "Bắt đầu"))
        else:
            root.after(0, lambda: txt_duong_di.insert(tk.END, "Không tìm thấy đường đi!"))
            root.after(0, lambda: log_text_frame.insert(tk.END, "Không tìm thấy đường đi!\n"))

    def giai_ma_tran():
        btn_giai.config(state=tk.DISABLED)

        txt_duong_di.delete("1.0", tk.END)
        log_text_frame.delete("1.0", tk.END)
        log_text_frame.insert(tk.END, f" ĐANG GIẢI {bfs_combobox.get()}...\n")

        # Chạy trên thread riêng
        thread = threading.Thread(target=run_solver, args=(bfs_combobox.get(),), daemon=True)
        thread.start()

    btn_giai = tk.Button(dashboard_frame, text = "Giải Ma Trận", command = giai_ma_tran)
    btn_giai.grid(row = 1, column = 0, columnspan = 2, padx = 3, pady = 7, sticky = "nsew")
  
    #4. Tạm dừng thực hiện:
    tam_dung_giai = False
    def tam_dung():
        nonlocal tam_dung_giai 
        tam_dung_giai = not(tam_dung_giai)
        if tam_dung_giai == True:
            btn_tam_dung.config(text = "Tiếp tục giải")
        else:
            btn_tam_dung.config(text = "Tạm dừng giải")

    btn_tam_dung = tk.Button(dashboard_frame, text = "Tạm dừng giải", command = tam_dung)
    btn_tam_dung.grid(row = 2, column = 0, columnspan = 2, padx = 3, pady = 7, sticky = "nsew")

    #5. Tốc độ giải: 
    label_toc_do = tk.Label(dashboard_frame, text = "  Tốc độ di: ")
    label_toc_do.grid(row = 3, column = 0, padx = 3, pady = 7, sticky = "w")
    txt_toc_do = tk.Text(dashboard_frame, width = 4, height = 1)
    txt_toc_do.grid(row = 3, column = 1, padx = 3, pady = 7, sticky = "nsew")
    txt_toc_do.insert("1.0", "0.5")

    #6. Reset lại chương trình:
    def reset_UI():
        nonlocal tam_dung_giai
        nonlocal last_parent_ma_tran
        btn_giai.config(state=tk.NORMAL)
        is_solving["value"] = False
        g.tk_da_duyet = 0
        g.tk_sinh_ra = 0
        last_parent_ma_tran = None 
        g.ma_tran_puzzle = [[1, 2, 3], 
                          [4, 0, 5], 
                          [7, 8, 6]]
        ve_ma_tran()
        ma_tran_text.delete("1.0", tk.END)
        txt_duong_di.delete("1.0", tk.END)
        log_text_frame.delete("1.0", tk.END)
        chuoi_hien_thi = json.dumps(g.ma_tran_puzzle).replace("], [", "], \n[")
        ma_tran_text.insert("1.0", chuoi_hien_thi)
        so_buoc.config(text="Số bước đi: 0")
        da_duyet.config(text="Đã duyệt: 0")
        sinh_ra.config(text="Sinh ra: 0")
        do_sau.config(text="Độ sâu: 0")
        bfs_combobox.current(0)
        tam_dung_giai = False
        btn_tam_dung.config(text="Tạm dừng giải")
        txt_toc_do.delete("1.0", tk.END)
        txt_toc_do.insert("1.0", "0.5")
        

    btn_reset = tk.Button(dashboard_frame, text = "Reset", command = reset_UI, bg = "white")
    btn_reset.grid(row = 4, column = 0, columnspan = 2, padx = 5, pady = 7, sticky = "nsew" )
    
    #7. Bảng thống kê
    thong_ke_frame = tk.LabelFrame(dashboard_frame, text = "Thống kê thuật toán")
    thong_ke_frame.grid(row = 5, column = 0, columnspan = 2, padx = 3, pady = 3, sticky = "nsew")
    #Bước đi
    so_buoc = tk.Label(thong_ke_frame, text ="Số bước đi: 0", bg="lightgray")
    so_buoc.pack(anchor = "w", padx = 3, pady = 3)
    #Đã duyệt 
    da_duyet = tk.Label(thong_ke_frame, text ="Đã duyệt: 0", bg="lightgray")
    da_duyet.pack(anchor = "w", padx = 3, pady = 3)
    #Đã sinh
    sinh_ra = tk.Label(thong_ke_frame, text = "Sinh ra: 0", bg="lightgray")
    sinh_ra.pack(anchor = "w", padx = 3, pady = 3)
    #Độ sâu
    do_sau = tk.Label(thong_ke_frame, text = "Độ sâ: 0", bg="lightgray")
    do_sau.pack(anchor = "w", padx = 3, pady = 3)

    #III. Thêm Log State:
    log_frame = tk.LabelFrame(root, text = "Log - State")
    log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
    #1. Thêm văn bản Log State 
    log_text_frame = tk.Text(log_frame, height = 6)
    log_text_frame.pack(fill = tk.BOTH, expand = True, padx = 1, pady = 1)
    
    last_parent_ma_tran = None 
    def ghi_log_state(parent_ma_tran, child_ma_tran, buoc, hanh_dong, cost):
        nonlocal last_parent_ma_tran
        stt =f"{buoc:<4}"
        if hanh_dong == "Bắt đầu: ":
            log_text_frame.insert(tk.END, f" {'STT':<4}  {'Parent':<13}    {'Child':<12} {'Action':<8} {'Cost'}\n")
            log_text_frame.insert(tk.END, "=" * 55 + "\n")
            for i in range(3):
                if i == 1:
                    log_text_frame.insert(tk.END, f" {stt} {' ':<13}    {str(child_ma_tran[i]):<12} {'Bắt đầu: ':<8}  {cost}\n")
                else:
                    log_text_frame.insert(tk.END, f" {' ':<4} {' ':<13}    {str(child_ma_tran[i]):<12} \n")
        else:
            p0, p1, p2 = str(parent_ma_tran[0]), str(parent_ma_tran[1]), str(parent_ma_tran[2])
            if last_parent_ma_tran == parent_ma_tran:
                p0, p1, p2 = "", "", ""
            log_text_frame.insert(tk.END, f" {' ':<4} {p0:<13}    {str(child_ma_tran[0]):<12}\n")
            log_text_frame.insert(tk.END, f" {stt} {p1:<13}    {str(child_ma_tran[1]):<12}   {hanh_dong:<8} {cost}\n")
            log_text_frame.insert(tk.END, f" {' ':<4} {p2:<13}    {str(child_ma_tran[2]):<12}\n")
            last_parent_ma_tran = [i[:] for i in  parent_ma_tran]

        log_text_frame.insert(tk.END, "-" * 55 + "\n")
            
        log_text_frame.see(tk.END)
        log_text_frame.update_idletasks()     
    
    def di_chuyen_tung_buoc(danh_sach_node, index = 0, chuoi_hien_tai = "Bắt dầu: "):

        if not is_solving["value"]:
            return
        if tam_dung_giai:
            root.after(100, lambda: di_chuyen_tung_buoc(danh_sach_node, index, chuoi_hien_tai))
            return
        if index >= len(danh_sach_node):
            txt_duong_di.delete("1.0", tk.END)
            txt_duong_di.insert("1.0", chuoi_hien_tai + " --> END")
            txt_duong_di.insert(tk.END, "\n ==== FINISH === \n")
            txt_duong_di.see(tk.END)

            btn_giai.config(state=tk.NORMAL)
            return 

        node_hien_tai = danh_sach_node[index]
        g.ma_tran_puzzle = [i[:] for i in node_hien_tai.ma_tran]
        ve_ma_tran()

        hanh_dong = node_hien_tai.action
        chi_phi = node_hien_tai.cost

        if index == 0:
            ghi_log_state(g.ma_tran_puzzle, g.ma_tran_puzzle, 0, "Bắt đầu: ", chi_phi)
        else:
            parent_node = danh_sach_node[index - 1]
            ghi_log_state(parent_node.ma_tran, node_hien_tai.ma_tran, index, hanh_dong, chi_phi)

            chuoi_hien_tai = f"{chuoi_hien_tai} --({hanh_dong}, C:{chi_phi})-->"

        txt_duong_di.delete("1.0", tk.END)
        txt_duong_di.insert("1.0", chuoi_hien_tai)
        txt_duong_di.see(tk.END)
        #Thời gian
        try: 
            giay = float(txt_toc_do.get().strip())
            mili_giay = int(giay*1000)
        except:
            mili_giay = 500
        root.after(mili_giay, lambda: di_chuyen_tung_buoc(danh_sach_node, index + 1, chuoi_hien_tai))

    #2. Đường đi
    duong_di_frame = tk.Frame(log_frame)
    duong_di_frame.pack(expand = True, padx = 5, pady = 5)
    label_duong_di = tk.Label(duong_di_frame, text = "Đường đi: ")
    label_duong_di.pack(padx = 0, pady = 5, anchor = "w")

    #3. Thêm frame đương đi để kết hợp với scroll_ball
    txt_duong_di = tk.Text(duong_di_frame)
    txt_duong_di.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

    scroll_ball = tk.Scrollbar(duong_di_frame, orient = tk.VERTICAL, command = txt_duong_di.yview)
    scroll_ball.pack(side = tk.RIGHT, fill = tk.Y)
    txt_duong_di.config(yscrollcommand = scroll_ball.set)

    root.resizable(False, False)
    tk.mainloop()