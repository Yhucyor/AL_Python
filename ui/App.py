import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json 
import threading
import inspect

#Thêm thuật toán 
from core.Algorithm import ALGORITHM_GROUPS
from core import globals as g

def UIPuzzle():
    root = tk.Tk()
    root.title("Puzzle 3x3")
    #root.geometry("460x570+50+50")
    #I. <=== Thêm giao diện 
    main_frame = tk.Frame(root, bg = "lightgray")
    main_frame.pack(padx = 5, pady = 5, fill = tk.BOTH, expand = False)

    #1. Thêm frame bên trái chứa Puzzle
    puzzle_frame = tk.Frame(main_frame, bg = "lightgray", bd = 1, relief = "groove")
    puzzle_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nsew")
    main_frame.grid_columnconfigure(1, weight=1)

    #2. Thêm Label tên ma trận
    puzzle_label = tk.Label(puzzle_frame, text = "<=== Trò chơi Puzzle 8 (3x3) ===>", font = ("Helvetica", 12, "bold"))
    puzzle_label.grid(row = 0)
    
    #3. Thêm các ô của ma trận
    # Canvas scrollable for multiple matrices
    canvas_matrix = tk.Canvas(puzzle_frame, bg="lightgray", width=360, height=210, bd=0, highlightthickness=0)
    canvas_matrix.grid(row=1, column=0, sticky="nsew", pady=5)
    scrollbar_matrix = tk.Scrollbar(puzzle_frame, orient=tk.HORIZONTAL, command=canvas_matrix.xview)
    scrollbar_matrix.grid(row=2, column=0, sticky="ew")
    canvas_matrix.config(xscrollcommand=scrollbar_matrix.set)
    
    grid_matrix_container = tk.Frame(canvas_matrix, bg="lightgray")
    frame_id = canvas_matrix.create_window((0, 0), window=grid_matrix_container, anchor="nw")
    
    def on_frame_configure(event):
        canvas_width = canvas_matrix.winfo_width()
        canvas_height = canvas_matrix.winfo_height()
        frame_width = grid_matrix_container.winfo_reqwidth()
        frame_height = grid_matrix_container.winfo_reqheight()
        
        if frame_width < canvas_width:
            x_pos = canvas_width // 2
            y_pos = canvas_height // 2
            canvas_matrix.itemconfigure(frame_id, anchor="center")
            canvas_matrix.configure(scrollregion=(0, 0, canvas_width, canvas_height))
        else:
            x_pos = 0
            y_pos = (canvas_height - frame_height) // 2 if frame_height < canvas_height else 0
            canvas_matrix.itemconfigure(frame_id, anchor="nw")
            canvas_matrix.configure(scrollregion=(0, 0, frame_width, max(canvas_height, frame_height)))
        
        canvas_matrix.coords(frame_id, x_pos, y_pos)

    grid_matrix_container.bind("<Configure>", on_frame_configure)
    canvas_matrix.bind("<Configure>", lambda e: on_frame_configure(None))

    def ve_ma_tran():
        for widget in grid_matrix_container.winfo_children():
            widget.destroy()
            
        matrices = g.ma_tran_puzzle
        # Xác định 1 ma trận hay danh sách ma trận
        if matrices and isinstance(matrices[0][0], int):
            matrices = [matrices] 
        
        # Nếu chỉ có 1 ma trận, thêm padding để center
        if len(matrices) == 1:
            # Thêm frame wrapper để center
            for idx, matrix in enumerate(matrices):
                frame_single = tk.Frame(grid_matrix_container, bg="lightgray", padx=10, pady=5)
                frame_single.grid(row=0, column=0)
                grid_matrix_container.grid_columnconfigure(0, weight=1)
                
                for i in range(3):
                    for j in range(3):
                        val = matrix[i][j]
                        text_val = str(val) if val != 0 else ""
                        lbl = tk.Label(frame_single, text=text_val, width=4, height=2, bd=3, relief="ridge", font=("Arial",14,"bold"))
                        lbl.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
        else:
            # Nhiều ma trận thì xếp ngang
            for idx, matrix in enumerate(matrices):
                frame_single = tk.Frame(grid_matrix_container, bg="lightgray", padx=10, pady=5)
                frame_single.grid(row=0, column=idx)
                for i in range(3):
                    for j in range(3):
                        val = matrix[i][j]
                        text_val = str(val) if val != 0 else ""
                        lbl = tk.Label(frame_single, text=text_val, width=4, height=2, bd=3, relief="ridge", font=("Arial",14,"bold"))
                        lbl.grid(row=i, column=j, padx=3, pady=3, sticky="nsew")
                    
        grid_matrix_container.update_idletasks()
        canvas_matrix.config(scrollregion=canvas_matrix.bbox("all"))
        
        # Force update để center ngay
        canvas_matrix.update_idletasks()
        on_frame_configure(None)

    ve_ma_tran()

   #4. Thêm ô nhập ma trận vào
    ma_tran_frame = tk.Frame(puzzle_frame, bg="white")
    ma_tran_frame.grid(row=3, column=0, pady=5)
    
    nhap_label = tk.Label(ma_tran_frame, text="Nhập Start:")
    nhap_label.grid(row=0, column=0, padx=3, pady=3, sticky="w")
    
    nhap_goal_label = tk.Label(ma_tran_frame, text="Nhập Goal:")
    nhap_goal_label.grid(row=0, column=1, padx=3, pady=3, sticky="w")

    def doi_ma_tran():
        try:
            str_ma_tran = ma_tran_text.get("1.0", tk.END).strip()
            tmp_ma_tran = json.loads(str_ma_tran)
            
            str_goal = goal_ma_tran_text.get("1.0", tk.END).strip()
            tmp_goal = json.loads(str_goal)
            
            #Chọn 1 phần hay mù 
            selected_env = env_combobox.get()
            is_blind = "Unobservable" in selected_env or "Partially Observable" in selected_env
            is_multiple_start = isinstance(tmp_ma_tran[0][0], list) if tmp_ma_tran else False
            is_multiple_goal = isinstance(tmp_goal[0][0], list) if tmp_goal else False
            
            if not is_blind:
                if is_multiple_start or is_multiple_goal:
                    messagebox.showerror("Lỗi!", "Môi trường này chỉ chấp nhận 1 ma trận!")
                    return
            else:
                loai_mu = loai_mu_var.get()
                if loai_mu == "Mù Start":
                    if is_multiple_goal:
                        messagebox.showerror("Lỗi!", "Trường hợp Mù Start, chỉ chấp nhận 1 ma trận Goal!")
                        return
                    if not is_multiple_start:
                        tmp_ma_tran = [tmp_ma_tran]
                elif loai_mu == "Mù Goal":
                    if is_multiple_start:
                        messagebox.showerror("Lỗi!", "Trường hợp Mù Goal, chỉ chấp nhận 1 ma trận Start!")
                        return
                    if not is_multiple_start:
                        tmp_ma_tran = [tmp_ma_tran]
            
            g.ma_tran_puzzle = tmp_ma_tran
            g.goal_ma_tran = tmp_goal
            ve_ma_tran()
            messagebox.showinfo("Thông báo", "Đổi ma trận thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi!", f"Định dạng ma trận sai!\n{e}")

    btn_doi = tk.Button(ma_tran_frame, text = "Đổi", command = doi_ma_tran)
    btn_doi.grid(row = 0, column = 2, sticky = "w")
    
    def load_test_data():
        try:
            import os
            file_path = os.path.join(os.getcwd(), "test_data.json")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            start_data = data.get("start")
            goal_data = data.get("goal")
            
            if start_data is not None and goal_data is not None:
                ma_tran_text.delete("1.0", tk.END)
                goal_ma_tran_text.delete("1.0", tk.END)
                
                ma_tran_text.insert("1.0", json.dumps(start_data).replace("], [", "],\n ["))
                goal_ma_tran_text.insert("1.0", json.dumps(goal_data).replace("], [", "],\n ["))
                
                doi_ma_tran()
            else:
                messagebox.showerror("Lỗi!", "File test_data.json không chứa 'start' hoặc 'goal'")
        except FileNotFoundError:
            messagebox.showerror("Lỗi!", "Không tìm thấy file test_data.json ở thư mục gốc!")
        except Exception as e:
            messagebox.showerror("Lỗi!", f"Lỗi đọc file: {e}")
    
    btn_load = tk.Button(ma_tran_frame, text="Tải File Test", command=load_test_data)
    btn_load.grid(row=0, column=3, sticky="w", padx=5)            

    #Hiển thị ma trận bắt đầu 
    chuoi_hien_thi = json.dumps(g.ma_tran_puzzle).replace("], [", "],\n [")
    ma_tran_text = tk.Text(ma_tran_frame, width=18, height=4)
    ma_tran_text.grid(row=1, column=0, padx=3, pady=3, sticky="nsew")
    ma_tran_text.insert("1.0", chuoi_hien_thi)
    
    #Hiển thị ma trận Goal 
    chuoi_goal = json.dumps(g.goal_ma_tran).replace("], [", "],\n [")
    goal_ma_tran_text = tk.Text(ma_tran_frame, width=18, height=4)
    goal_ma_tran_text.grid(row=1, column=1, padx=3, pady=3, sticky="nsew")
    goal_ma_tran_text.insert("1.0", chuoi_goal)
   

    #II. <=== Thêm bên bảng điều khiển ===>
    dashboard_frame = tk.Frame(main_frame, bg = "lightgray", bd = 1, relief = "groove")
    dashboard_frame.grid(row = 0, column = 1, padx = 11, pady = 5, sticky = "nsew")
    
    #1. Thêm nhãn môi trường 
    env_label = tk.Label(dashboard_frame, text="Môi trường: ")
    env_label.grid(row=0, column=0, padx=1, pady=2, sticky="nw")
    #Thêm phần combobox để chọn các loại môi trường 
    list_envs = list(ALGORITHM_GROUPS.keys())
    env_combobox = ttk.Combobox(dashboard_frame, values=list_envs, state="readonly", width=22)
    env_combobox.current(0)
    env_combobox.grid(row=1, column=0, columnspan=2, padx=1, pady=2, sticky="nw")    
    
    #2. Thêm nhãn thuật toán
    bfs_label = tk.Label(dashboard_frame, text="Thuật toán: ")
    bfs_label.grid(row=2, column=0, padx=1, pady=2, sticky="nw")    
    bfs_combobox = ttk.Combobox(dashboard_frame, state="readonly", width=22)
    bfs_combobox.grid(row=3, column=0, columnspan=2, padx=1, pady=2, sticky="nw")

    #3. Bên mù - kiểu như bên nào được cho và bên nào không được cho
    loai_mu_frame = tk.Frame(dashboard_frame, bg="lightgray")
    loai_mu_var = tk.StringVar(value="Mù Start")
    #Cái này sẽ set ma trận sao để test tuật toán 
    def on_loai_mu_change():
        loai_mu = loai_mu_var.get()
        selected_env = env_combobox.get() # Kiểm tra môi trường hiện tại

        if "Unobservable" in selected_env:
            if loai_mu == "Mù Start":
                # Unobservable Mù Start: 2 Start, 1 Goal
                g.ma_tran_puzzle = [
                    [[1, 2, 3], [4, 0, 5], [7, 8, 6]],
                    [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
                ]
                g.goal_ma_tran = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            else:
                # Unobservable Mù Goal: 1 Start, 2 Goal
                g.ma_tran_puzzle = [[[1, 2, 3], [4, 0, 5], [7, 8, 6]]]
                g.goal_ma_tran = [
                    [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
                    [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
                ]
        elif "Partially Observable" in selected_env:
            # Partially Observable dùng số -1 để biểu thị ô bị mù (ẩn)
            if loai_mu == "Mù Start":
                # Start có ô ẩn (-1), Goal bình thường
                g.ma_tran_puzzle = [[1, 2, 3], [4, -1, -1], [7, 8, 6]]
                g.goal_ma_tran = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            else:
                # Start bình thường, Goal có ô ẩn (-1)
                g.ma_tran_puzzle = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
                g.goal_ma_tran = [[1, 2, 3], [4, -1, -1], [7, 8, 0]]
        
        # Cập nhật hiển thị lên UI
        ma_tran_text.delete("1.0", tk.END)
        goal_ma_tran_text.delete("1.0", tk.END)
        chuoi_hien_thi = json.dumps(g.ma_tran_puzzle).replace("], [", "],\n [")
        ma_tran_text.insert("1.0", chuoi_hien_thi)
        chuoi_goal = json.dumps(g.goal_ma_tran).replace("], [", "],\n [")
        goal_ma_tran_text.insert("1.0", chuoi_goal)
        ve_ma_tran()

    #Thêm một số nút chọn để chọn  loại mù bên nào 
    rb_mu_start = tk.Radiobutton(loai_mu_frame, text="Mù Start", variable=loai_mu_var, value="Mù Start", bg="lightgray", command=on_loai_mu_change)
    rb_mu_start.pack(side=tk.LEFT)
    rb_mu_goal = tk.Radiobutton(loai_mu_frame, text="Mù Goal", variable=loai_mu_var, value="Mù Goal", bg="lightgray", command=on_loai_mu_change)
    rb_mu_goal.pack(side=tk.LEFT)

    #4. Cập nhật thuật toán
    def update_algorithms(event=None):
        selected_env = env_combobox.get()
        algos = list(ALGORITHM_GROUPS[selected_env].keys())
        bfs_combobox.config(values=algos)
        if algos:
            bfs_combobox.current(0)
            
        if "Unobservable" in selected_env or "Partially Observable" in selected_env:
            log_frame.config(text="Log - Belief State")
            loai_mu_frame.grid(row=4, column=0, columnspan=2, sticky="nw")
            
            on_loai_mu_change() 
        else:
            log_frame.config(text="Log - State")
            loai_mu_frame.grid_remove()
            if isinstance(g.ma_tran_puzzle[0][0], list) or isinstance(g.goal_ma_tran[0][0], list) or any(-1 in row for row in g.ma_tran_puzzle) if not isinstance(g.ma_tran_puzzle[0][0], list) else False:
                # Reset lại ma trận thường nếu quay về Fully Observable
                g.ma_tran_puzzle = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
                g.goal_ma_tran = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
                ma_tran_text.delete("1.0", tk.END)
                goal_ma_tran_text.delete("1.0", tk.END)
                chuoi_hien_thi = json.dumps(g.ma_tran_puzzle).replace("], [", "],\n [")
                ma_tran_text.insert("1.0", chuoi_hien_thi)
                chuoi_goal = json.dumps(g.goal_ma_tran).replace("], [", "],\n [")
                goal_ma_tran_text.insert("1.0", chuoi_goal)
                ve_ma_tran()
    
    #Thay đổi nội dung 
    env_combobox.bind("<<ComboboxSelected>>", update_algorithms)

    #5. Giải ma trận
    is_solving = {"value": False} 
    def run_solver(env_name, algo_name):
        is_solving["value"] = True
        g.tk_da_duyet = 0
        g.tk_sinh_ra = 0

        try:
            solver_func = ALGORITHM_GROUPS[env_name][algo_name]
            sig = inspect.signature(solver_func)
            if 'goal_matrix' in sig.parameters:
                sol = solver_func(g.ma_tran_puzzle, goal_matrix=g.goal_ma_tran)
            else:
                sol = solver_func(g.ma_tran_puzzle)

            root.after(0, lambda: update_after_solve(sol))
        except Exception as e:
            import traceback
            err_msg = traceback.format_exc()
            def handle_err():
                log_text_frame.insert(tk.END, f"\nLỖI THUẬT TOÁN:\n{err_msg}\n")
                txt_duong_di.insert(tk.END, "Thuật toán bị lỗi! Vui lòng xem log.")
                btn_giai.config(state=tk.NORMAL)
            root.after(0, handle_err)

    def update_after_solve(sol):
        if sol:
            root.after(0, lambda: so_buoc.config(text=f"Số bước đi: {len(sol)-1}"))
            root.after(0, lambda: do_sau.config(text=f"Độ sâu: {len(sol)-1}"))
            root.after(0, lambda: da_duyet.config(text=f"Đã duyệt: {g.tk_da_duyet}"))
            root.after(0, lambda: sinh_ra.config(text=f"Sinh ra: {g.tk_sinh_ra}"))

            try:
                import inspect
                sig = inspect.signature(sol[-1].isGoal)
                if 'goal_matrix' in sig.parameters:
                    gm = g.goal_ma_tran
                    if gm and isinstance(gm[0][0], int):
                        gm = [gm]
                    is_g = sol[-1].isGoal(gm)
                else:
                    is_g = sol[-1].isGoal()
                    
                if not is_g:
                    root.after(0, lambda: log_text_frame.insert(tk.END, "Không tìm thấy đích! Bị kẹt.\n"))
            except Exception:
                pass
                
            root.after(0, lambda: di_chuyen_tung_buoc(sol, 0, "Bắt đầu"))
        else:
            root.after(0, lambda: txt_duong_di.insert(tk.END, "Không tìm thấy đường đi!"))
            root.after(0, lambda: log_text_frame.insert(tk.END, "Không tìm thấy đường đi!\n"))
            root.after(0, lambda: btn_giai.config(state=tk.NORMAL))


    def giai_ma_tran():
        btn_giai.config(state=tk.DISABLED)
        txt_duong_di.delete("1.0", tk.END)
        log_text_frame.delete("1.0", tk.END)
        
        # Header log đẹp hơn
        log_text_frame.insert(tk.END, "="*70 + "\n")
        log_text_frame.insert(tk.END, f"  ĐANG GIẢI: {bfs_combobox.get()}\n")
        log_text_frame.insert(tk.END, "="*70 + "\n")
        
        def fmt_log(mat):
            if isinstance(mat[0][0], list):
                # Nhiều ma trận (belief state)
                res = ""
                for i, m in enumerate(mat):
                    res += f"\n    State {i+1}:\n"
                    for row in m:
                        res += f"      {' '.join(str(x) for x in row)}\n"
                return res
            else:
                # Một ma trận đơn
                res = "\n"
                for row in mat:
                    res += f"    {' '.join(str(x) for x in row)}\n"
                return res
        
        start_str = fmt_log(g.ma_tran_puzzle)
        goal_str = fmt_log(g.goal_ma_tran)
        log_text_frame.insert(tk.END, f"\n  Start:{start_str}")
        log_text_frame.insert(tk.END, f"\n  Goal:{goal_str}\n")

        thread = threading.Thread(target=run_solver, args=(env_combobox.get(), bfs_combobox.get()), daemon=True)
        thread.start()

    btn_giai = tk.Button(dashboard_frame, text="Giải Ma Trận", command=giai_ma_tran)
    btn_giai.grid(row=5, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")      
    
    #6. Tạm dừng thực hiện:
    tam_dung_giai = False
    def tam_dung():
        nonlocal tam_dung_giai 
        tam_dung_giai = not(tam_dung_giai)
        if tam_dung_giai == True:
            btn_tam_dung.config(text = "Tiếp tục giải")
        else:
            btn_tam_dung.config(text = "Tạm dừng giải")

    btn_tam_dung = tk.Button(dashboard_frame, text = "Tạm dừng giải", command = tam_dung)
    btn_tam_dung.grid(row = 6, column = 0, columnspan = 2, padx = 3, pady = 3, sticky = "nsew")

    #7. Tốc độ giải: 
    label_toc_do = tk.Label(dashboard_frame, text = "  Tốc độ di: ")
    label_toc_do.grid(row = 7, column = 0, padx = 3, pady = 3, sticky = "w")
    txt_toc_do = tk.Text(dashboard_frame, width = 4, height = 1)
    txt_toc_do.grid(row = 7, column = 1, padx = 3, pady = 3, sticky = "nsew")
    txt_toc_do.insert("1.0", "0.5")

    #8. Reset lại chương trình:
    def reset_UI():
        nonlocal tam_dung_giai
        nonlocal last_parent_ma_tran
        btn_giai.config(state=tk.NORMAL)
        is_solving["value"] = False
        g.tk_da_duyet = 0
        g.tk_sinh_ra = 0
        last_parent_ma_tran = None
        loai_mu_var.set("Mù Start")         
        if "Unobservable" in env_combobox.get():
            on_loai_mu_change()
        else:
            g.ma_tran_puzzle = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
            g.goal_ma_tran = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
            ve_ma_tran()
            ma_tran_text.delete("1.0", tk.END)
            chuoi_hien_thi = json.dumps(g.ma_tran_puzzle).replace("], [", "],\n [")
            ma_tran_text.insert("1.0", chuoi_hien_thi)
            goal_ma_tran_text.delete("1.0", tk.END)
            chuoi_goal = json.dumps(g.goal_ma_tran).replace("], [", "],\n [")
            goal_ma_tran_text.insert("1.0", chuoi_goal)

        txt_duong_di.delete("1.0", tk.END)
        log_text_frame.delete("1.0", tk.END)
        so_buoc.config(text="Số bước đi: 0")
        da_duyet.config(text="Đã duyệt: 0")
        sinh_ra.config(text="Sinh ra: 0")
        do_sau.config(text="Độ sâu: 0")
        tam_dung_giai = False
        btn_tam_dung.config(text="Tạm dừng giải")
        txt_toc_do.delete("1.0", tk.END)
        txt_toc_do.insert("1.0", "0.5")

    btn_reset = tk.Button(dashboard_frame, text="Reset", command=reset_UI, bg="white")
    btn_reset.grid(row=8, column=0, columnspan=2, padx=5, pady=3, sticky="nsew")
    
    #10. Thêm bảng thống kê 
    thong_ke_frame = tk.LabelFrame(dashboard_frame, text = "Thống kê thuật toán")
    thong_ke_frame.grid(row = 9, column = 0, columnspan = 2, padx = 3, pady = 3, sticky = "nsew")
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
    do_sau = tk.Label(thong_ke_frame, text = "Độ sâu: 0", bg="lightgray")
    do_sau.pack(anchor = "w", padx = 3, pady = 3)

    #III. Thêm Log State:
    log_frame = tk.LabelFrame(root, text = "Log - State")
    log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=5, pady=5)
    #1. Thêm văn bản Log State 
    log_text_frame = tk.Text(log_frame, height=8, width=75, font=("Courier New", 9))
    log_text_frame.pack(fill = tk.BOTH, expand = False, padx = 1, pady = 1)

    last_parent_ma_tran = None 
    def ghi_log_state(parent_ma_tran, child_ma_tran, buoc, hanh_dong, cost):
        nonlocal last_parent_ma_tran
        stt = str(buoc)
        
        def get_rows(m):
            if isinstance(m[0][0], int):
                # Format với khoảng cách cố định giữa các số
                row1 = " ".join(f"{x:1}" for x in m[0])
                row2 = " ".join(f"{x:1}" for x in m[1])
                row3 = " ".join(f"{x:1}" for x in m[2])
                return [row1, row2, row3]
            else:
                row1 = " | ".join(" ".join(f"{x:1}" for x in state[0]) for state in m)
                row2 = " | ".join(" ".join(f"{x:1}" for x in state[1]) for state in m)
                row3 = " | ".join(" ".join(f"{x:1}" for x in state[2]) for state in m)
                return [row1, row2, row3]
        
        p_rows = get_rows(parent_ma_tran)
        c_rows = get_rows(child_ma_tran)
        
        if hanh_dong == "Bắt đầu: ":
            # Header với khoảng cách "==" giữa các cột
            log_text_frame.insert(tk.END, f"{'STT':<9}  {'Parent':<20}  {'Child':<20}  {'Action':<20}  {'Cost':<9}\n")
            log_text_frame.insert(tk.END, "=" * 84 + "\n")
            log_text_frame.insert(tk.END, f"{stt:<9}  {p_rows[0]:<20}  {c_rows[0]:<20}  {'Start':<20}  {cost:<9}\n")
            log_text_frame.insert(tk.END, f"{'':9}  {p_rows[1]:<20}  {c_rows[1]:<20}  {'':20}  {'':6}\n")
            log_text_frame.insert(tk.END, f"{'':9}  {p_rows[2]:<20}  {c_rows[2]:<20}  {'':20}  {'':6}\n")
        else:
            if last_parent_ma_tran == parent_ma_tran:
                # Không hiển thị lại parent nếu giống
                log_text_frame.insert(tk.END, f"{stt:<9}  {'':20}  {c_rows[0]:<20}  {hanh_dong:<20}  {cost:<9}\n")
                log_text_frame.insert(tk.END, f"{'':9}  {'':20}  {c_rows[1]:<20}  {'':20}  {'':6}\n")
                log_text_frame.insert(tk.END, f"{'':9}  {'':20}  {c_rows[2]:<20}  {'':20}  {'':6}\n")
            else:
                log_text_frame.insert(tk.END, f"{stt:<9}  {p_rows[0]:<20}  {c_rows[0]:<20}  {hanh_dong:<20}  {cost:<9}\n")
                log_text_frame.insert(tk.END, f"{'':9}  {p_rows[1]:<20}  {c_rows[1]:<20}  {'':20}  {'':6}\n")
                log_text_frame.insert(tk.END, f"{'':9}  {p_rows[2]:<20}  {c_rows[2]:<20}  {'':20}  {'':6}\n")
            
        last_parent_ma_tran = [i[:] for i in parent_ma_tran] if isinstance(parent_ma_tran[0][0], int) else parent_ma_tran[:]
        log_text_frame.insert(tk.END, "-" * 84 + "\n")
            
        log_text_frame.see(tk.END)
        log_text_frame.update_idletasks()      
    
    def di_chuyen_tung_buoc(danh_sach_node, index = 0, chuoi_hien_tai = None):
        if not is_solving["value"]:
            return
        if tam_dung_giai:
            root.after(100, lambda: di_chuyen_tung_buoc(danh_sach_node, index, chuoi_hien_tai))
            return
        if index >= len(danh_sach_node):
            txt_duong_di.delete("1.0", tk.END)
            if isinstance(chuoi_hien_tai, list):
                txt_duong_di.insert("1.0", "\n".join([c + "END" for c in chuoi_hien_tai]))
            else:
                txt_duong_di.insert("1.0", (chuoi_hien_tai or "") + "END")

            try:
                import inspect
                sig = inspect.signature(danh_sach_node[-1].isGoal)
                if 'goal_matrix' in sig.parameters:
                    gm = g.goal_ma_tran
                    if gm and isinstance(gm[0][0], int):
                        gm = [gm]
                    is_g = danh_sach_node[-1].isGoal(gm)
                else:
                    is_g = danh_sach_node[-1].isGoal()
            except Exception as e:
                is_g = True
            if is_g:
                txt_duong_di.insert(tk.END, "\n ==== FINISH === \n")
            else:
                txt_duong_di.insert(tk.END, "\n ==== THẤT BẠI: KẸT TẠI CỰC TRỊ ĐỊA PHƯƠNG === \n")
            
            txt_duong_di.see(tk.END)
            btn_giai.config(state=tk.NORMAL)
            return 

        node_hien_tai = danh_sach_node[index]
        g.ma_tran_puzzle = node_hien_tai.ma_tran
        if isinstance(g.ma_tran_puzzle[0][0], int):
            g.ma_tran_puzzle = [i[:] for i in g.ma_tran_puzzle]
        else:
            g.ma_tran_puzzle = [m for m in g.ma_tran_puzzle]
            
        ve_ma_tran()

        hanh_dong = node_hien_tai.action
        chi_phi = node_hien_tai.cost

        if index == 0:
            ghi_log_state(g.ma_tran_puzzle, g.ma_tran_puzzle, 0, "Bắt đầu: ", chi_phi)
            # Kiểm tra xem có phải belief state không (nhiều ma trận)
            if isinstance(g.ma_tran_puzzle[0][0], list) and len(g.ma_tran_puzzle) > 1:
                # Belief state - khởi tạo đường đi cho mỗi state
                chuoi_hien_tai = [f"State {i+1}: Start" for i in range(len(g.ma_tran_puzzle))]
            else:
                # Single state
                chuoi_hien_tai = "Start"
        else:
            parent_node = danh_sach_node[index - 1]
            ghi_log_state(parent_node.ma_tran, node_hien_tai.ma_tran, index, hanh_dong, chi_phi)

            # Kiểm tra xem có phải belief state không
            if isinstance(chuoi_hien_tai, list):
                # Belief state - cập nhật đường đi cho tất cả states vì action áp dụng cho tất cả
                new_chuoi_hien_tai = []
                for i_state, s in enumerate(chuoi_hien_tai):
                    # Nếu ma trận tại state này không đổi so với parent -> không đi được
                    if parent_node.ma_tran[i_state] == node_hien_tai.ma_tran[i_state]:
                        new_chuoi_hien_tai.append(s + f" --(--)--> ")
                    else:
                        new_chuoi_hien_tai.append(s + f" --({hanh_dong}, C:{chi_phi})--> ")
                chuoi_hien_tai = new_chuoi_hien_tai
            else:
                # Single state
                if parent_node.ma_tran == node_hien_tai.ma_tran:
                    chuoi_hien_tai += f" --(--)--> "
                else:
                    chuoi_hien_tai += f" --({hanh_dong}, C:{chi_phi})--> "

        txt_duong_di.delete("1.0", tk.END)
        if isinstance(chuoi_hien_tai, list):
            txt_duong_di.insert("1.0", "\n".join(chuoi_hien_tai))
        else:
            txt_duong_di.insert("1.0", chuoi_hien_tai)
            
        txt_duong_di.see(tk.END)
        try: 
            giay = float(txt_toc_do.get().strip())
            mili_giay = int(giay*1000)
        except:
            mili_giay = 500
        root.after(mili_giay, lambda: di_chuyen_tung_buoc(danh_sach_node, index + 1, chuoi_hien_tai))

    #2. Đường đi
    duong_di_frame = tk.Frame(log_frame)
    duong_di_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
    label_duong_di = tk.Label(duong_di_frame, text = "Đường đi: ")
    label_duong_di.pack(padx = 0, pady = 2, anchor = "w")

    #3. Thêm frame đương đi để kết hợp với scroll_ball
    txt_duong_di = tk.Text(duong_di_frame, height=5, width=75, font=("Courier New", 9))
    txt_duong_di.pack(side = tk.LEFT, fill = tk.X, expand = True)

    scroll_ball = tk.Scrollbar(duong_di_frame, orient = tk.VERTICAL, command = txt_duong_di.yview)
    scroll_ball.pack(side = tk.RIGHT, fill = tk.Y)
    txt_duong_di.config(yscrollcommand = scroll_ball.set)

    update_algorithms()
    root.resizable(False, False)
    tk.mainloop()