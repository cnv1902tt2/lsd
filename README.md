# Hướng Dẫn Deploy Lên Vercel

## 📋 Chuẩn Bị

### Bước 1: Chạy Script Python để tạo file JSON
```bash
python extract_questions.py
```
Script sẽ tạo các file:
- `de_1_questions.json`
- `de_2_questions.json`
- ... (cho đến de_8)

### Bước 2: Cấu Trúc Thư Mục
Đảm bảo thư mục của bạn có:
```
De Thi/
├── quiz_practice.html (file giao diện chính)
├── de_1_questions.json
├── de_2_questions.json
├── de_3_questions.json
├── de_4_questions.json
├── de_5_questions.json
├── de_6_questions.json
├── de_7_questions.json
├── de_8_questions.json
├── de_1 (file HTML gốc)
├── de_2 (file HTML gốc)
├── ... (các file khác)
└── extract_questions.py
```

## 🚀 Deploy Lên Vercel

### Phương Án 1: Deploy Qua GitHub (Khuyến Nghị)

#### 1. Tạo Git Repository
```bash
cd "d:\De Thi"
git init
git add .
git commit -m "Initial commit"
```

#### 2. Push Lên GitHub
- Tạo repository mới trên GitHub (ví dụ: `quiz-practice`)
- Push code lên:
```bash
git remote add origin https://github.com/YOUR_USERNAME/quiz-practice.git
git branch -M main
git push -u origin main
```

#### 3. Deploy Trên Vercel
1. Truy cập [vercel.com](https://vercel.com)
2. Đăng nhập/Đăng ký (có thể dùng GitHub)
3. Click "Add New Project"
4. Import repository từ GitHub
5. Cấu hình:
   - **Framework Preset**: Other (hoặc để trống)
   - **Root Directory**: `./` (hoặc để trống)
   - **Build Command**: để trống
   - **Output Directory**: `./`
6. Click "Deploy"

### Phương Án 2: Deploy Trực Tiếp (Không Qua Git)

#### 1. Cài Đặt Vercel CLI
```bash
npm install -g vercel
```

#### 2. Login Vercel
```bash
vercel login
```

#### 3. Deploy
```bash
cd "d:\De Thi"
vercel
```

Làm theo hướng dẫn:
- Set up and deploy? → **Yes**
- Which scope? → Chọn account của bạn
- Link to existing project? → **No**
- What's your project's name? → Nhập tên (ví dụ: `quiz-practice`)
- In which directory is your code located? → `./`
- Want to override the settings? → **No**

#### 4. Deploy Production
```bash
vercel --prod
```

## ⚙️ Lưu Ý Quan Trọng

### Đổi Tên File HTML
Vercel sẽ tự động tìm file `index.html` làm trang chủ. Bạn có 2 lựa chọn:

**Cách 1: Đổi tên file**
```bash
# Đổi tên quiz_practice.html thành index.html
ren quiz_practice.html index.html
```

**Cách 2: Tạo file index.html redirect**
Tạo file `index.html` mới:
```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=quiz_practice.html">
</head>
<body>
    <p>Redirecting...</p>
</body>
</html>
```

### Cấu Hình vercel.json (Tùy Chọn)
Nếu muốn cấu hình chi tiết, tạo file `vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/quiz_practice.html" }
  ]
}
```

## 🔗 Sau Khi Deploy

Vercel sẽ cung cấp URL:
- **Preview URL**: `https://your-project-xxx.vercel.app`
- **Production URL**: `https://your-project.vercel.app`

### Cập Nhật Sau Deploy
```bash
# Nếu dùng Git
git add .
git commit -m "Update"
git push

# Nếu dùng Vercel CLI
vercel --prod
```

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi: Không tải được file JSON
- Đảm bảo các file JSON đã được upload
- Kiểm tra đường dẫn trong code

### Lỗi: 404 Not Found
- Đảm bảo có file `index.html` hoặc cấu hình redirect
- Kiểm tra file `vercel.json`

### Lỗi: CORS
- Vercel tự động xử lý CORS cho static files
- Nếu vẫn lỗi, thêm headers trong `vercel.json`

## 📱 Kiểm Tra Responsive
Sau khi deploy, kiểm tra trên:
- Desktop
- iPhone 11 (414x896)
- iPad
- Các thiết bị khác

## 🎉 Hoàn Tất!
Website của bạn đã sẵn sàng và có thể truy cập từ bất kỳ đâu!
