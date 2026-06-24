# Buổi 4 - Intelligent Agents

## Thông tin sinh viên

- Họ và tên: Nguyễn Trọng Thức
- MSSV: 24110349
- Môn học: Trí Tuệ Nhân Tạo (Artificial Intelligence)

---

## Nội dung buổi học

Buổi 4:
- Bài tập trên lớp: Máy hút bụi và 8 Puzzle Simple Reflex Agent
- Bài tập về nhà: Máy hút bụi Model Based Agent 

### 1. Simple Reflex Agent

Simple Reflex Agent đưa ra quyết định chỉ dựa trên trạng thái hiện tại của môi trường.

#### Bài tập

- Vacuum Cleaner Agent
- 8 Puzzle Agent

##### Vacuum Cleaner Agent

Tập luật:

- Nếu vị trí hiện tại có bụi → Hút bụi.
- Nếu vị trí hiện tại sạch → Di chuyển sang vị trí khác.

##### 8 Puzzle Agent

Tập luật:

1. Xác định vị trí ô trống.
2. Sinh các nước đi hợp lệ:
   - Trái
   - Phải
   - Lên
   - Xuống
3. Hoán đổi ô trống với ô lân cận.

---

### 2. Model Based Agent

Model Based Agent lưu trữ trạng thái môi trường đã quan sát để hỗ trợ quá trình ra quyết định.

#### Bài tập

- Vacuum Cleaner Agent

##### Vacuum Cleaner Agent

Chức năng:

- Quan sát môi trường.
- Lưu trạng thái các ô đã được làm sạch.
- Quyết định hành động dựa trên mô hình nội bộ thay vì chỉ dựa vào cảm nhận hiện tại.

---

## Cấu trúc thư mục

```text
Buoi4/
│
├── Model_Based_Agent/
│   └── Vacuum_Cleaner.ipynb
│
├── Simple_Reflex_Agent/
│   ├── Eight_Puzzle.ipynb
│   └── Vacuum_Cleaner.ipynb
│
└── README.md
```