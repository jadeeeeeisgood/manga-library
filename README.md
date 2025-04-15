# Manga Library

Ứng dụng quản lý thư viện manga đơn giản được viết bằng Python và Tkinter.

## Tính năng

- Quản lý tài khoản người dùng (đăng ký, đăng nhập, đổi mật khẩu)
- Xem thông tin cá nhân và thống kê
- Thêm manga mới vào thư viện
- Tìm kiếm manga từ MyAnimeList API
- Xem danh sách top manga
- Tìm kiếm và lọc manga theo nhiều tiêu chí
- Quản lý danh sách manga yêu thích
- Xem chi tiết thông tin manga
- Hỗ trợ hiển thị ảnh bìa manga

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Các thư viện phụ thuộc (xem `requirements.txt`)

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/yourusername/manga-library.git
cd manga-library
```

2. Tạo và kích hoạt môi trường ảo (tùy chọn nhưng khuyến khích):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt các thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Chạy ứng dụng:
```bash
python main.py
```

2. Đăng nhập với tài khoản mặc định:
- Username: admin
- Password: admin1

3. Hoặc đăng ký tài khoản mới từ giao diện đăng nhập

## Cấu trúc thư mục

```
manga_library/
├── assets/             # Tài nguyên ứng dụng
│   └── cache/         # Cache cho ảnh manga
├── data/              # Dữ liệu ứng dụng
│   ├── users.json     # Thông tin người dùng
│   └── manga_collection.json  # Bộ sưu tập manga
├── src/               # Mã nguồn
│   ├── auth/          # Xử lý xác thực
│   ├── gui/           # Giao diện người dùng
│   ├── models/        # Các model dữ liệu
│   └── utils/         # Tiện ích
├── main.py            # Điểm vào ứng dụng
└── requirements.txt   # Các thư viện phụ thuộc
```

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request.

## Giấy phép

[MIT License](LICENSE)
