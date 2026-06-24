# Buổi 6 - DFS & IDS Search

## Thông tin sinh viên

* Họ và tên: Nguyễn Trọng Thức
* MSSV: 24110349
* Môn học: Trí Tuệ Nhân Tạo (Artificial Intelligence)
* Bài tập về nhà: Thêm thuật toán DFS và thuật toán IDS và thêm giao diện với hiển thị lịch sử đi từng bước 
---

## Mục tiêu

* Tìm hiểu thuật toán tìm kiếm theo chiều sâu (Depth First Search - DFS).
* Tìm hiểu thuật toán tìm kiếm sâu dần lặp (Iterative Deepening Search - IDS).
* Áp dụng DFS và IDS để giải bài toán 8-Puzzle.
* Thêm lịch sử đường đi của thuật toán 

---

## Nội dung thực hành

### Bài toán 8-Puzzle

8-Puzzle là bài toán gồm 8 ô số và 1 ô trống trên ma trận 3x3.

Agent cần tìm chuỗi hành động để đưa trạng thái ban đầu về trạng thái đích.

### Trạng thái đích

```text
1 2 3
8 0 4
7 6 5
```

---

## Thuật toán DFS

Depth First Search (DFS) là thuật toán tìm kiếm theo chiều sâu.

### Nguyên lý hoạt động

1. Bắt đầu từ trạng thái gốc.
2. Mở rộng một nhánh đến mức sâu nhất có thể.
3. Khi không thể mở rộng tiếp thì quay lui.
4. Tiếp tục cho đến khi tìm được trạng thái đích.

### Ưu điểm

* Tiết kiệm bộ nhớ hơn BFS.
* Cài đặt đơn giản.

### Nhược điểm

* Không đảm bảo tìm được lời giải ngắn nhất.
* Có thể đi sâu vào các nhánh không tối ưu.

---

## Thuật toán IDS

Iterative Deepening Search (IDS) là sự kết hợp giữa DFS và BFS.

### Nguyên lý hoạt động

1. Thực hiện DFS với giới hạn độ sâu.
2. Nếu chưa tìm thấy lời giải thì tăng giới hạn độ sâu.
3. Lặp lại cho đến khi tìm được trạng thái đích.


## Chức năng chương trình

* Hiển thị giao diện bằng Tkinter.
* Nhập trạng thái ban đầu của Puzzle.
* Giải bài toán bằng DFS.
* Giải bài toán bằng IDS.
* Hiển thị từng bước thực hiện.
* Mô phỏng quá trình tìm kiếm trực quan.

---

## Cấu trúc thư mục

```text
Buoi6/
│
├── core/
│   ├── node.py
│   ├── puzzle.py
│   ├── dfs.py
│   └── ids.py
│
├── ui/
│   └── puzzle_ui.py
│
├── main.py
│
└── README.md
```
