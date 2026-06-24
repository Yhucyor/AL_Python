# Buổi 5 - Breadth First Search (BFS)

## Thông tin sinh viên

* Họ và tên: Nguyễn Trọng Thức
* MSSV: 24110349
* Môn học: Trí Tuệ Nhân Tạo (Artificial Intelligence)
* Bài tập về nhà: Xây dựng giao diện trực quan UI để mô phỏng trò chơi 
---

## Mục tiêu

* Tìm hiểu thuật toán tìm kiếm theo chiều rộng (Breadth First Search - BFS).
* Áp dụng BFS để giải bài toán 8-Puzzle.
* Xây dựng giao diện trực quan bằng Tkinter.

---

## Nội dung thực hành

### Bài toán 8-Puzzle

8-Puzzle là bài toán gồm 8 ô số và 1 ô trống trên ma trận 3x3.

Agent cần tìm chuỗi hành động để đưa trạng thái ban đầu về trạng thái đích.

Ví dụ trạng thái đích:

```text
1 2 3
8 0 4
7 6 5
```

---

## Thuật toán Breadth First Search (BFS)

Breadth First Search là thuật toán tìm kiếm theo chiều rộng.

### Nguyên lý hoạt động

1. Đưa trạng thái ban đầu vào Frontier.
2. Lấy trạng thái đầu tiên trong Frontier để mở rộng.
3. Kiểm tra trạng thái đích.
4. Sinh các trạng thái con.
5. Thêm các trạng thái chưa được duyệt vào Frontier.
6. Lặp lại cho đến khi tìm được lời giải hoặc Frontier rỗng.

### Ưu điểm

* Đảm bảo tìm được lời giải nếu tồn tại.
* Tìm được lời giải ngắn nhất khi chi phí các bước bằng nhau.

### Nhược điểm

* Tốn nhiều bộ nhớ khi không gian trạng thái lớn.
* Hiệu suất giảm khi độ sâu tìm kiếm tăng.

---

## Chức năng chương trình

* Hiển thị giao diện bằng Tkinter.
* Nhập trạng thái ban đầu của Puzzle.
* Giải bài toán bằng BFS.
* Hiển thị các bước thực hiện.
* Mô phỏng quá trình tìm kiếm trực quan.

---

## Cấu trúc thư mục

```text
Buoi5/
│
├── core/
│   ├── __init__.py
│   ├── bfs.py
│   ├── node.py
│   └── puzzle.py
│
├── ui/
│   ├── __init__.py
│   └── puzzle_ui.py
│
├── main.py
│
└── README.md
---

## Cách chạy chương trình

```bash
python main.py
```

---

## Tài liệu tham khảo

* Stuart Russell & Peter Norvig - Artificial Intelligence: A Modern Approach.
* Giáo trình Trí Tuệ Nhân Tạo.
* Tài liệu thực hành trên lớp.
