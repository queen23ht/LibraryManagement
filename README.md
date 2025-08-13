# 📚 Hệ Thống Quản Lý Thư Viện

## 🎯 Tổng Quan Dự Án

Hệ thống Quản Lý Thư Viện này thể hiện các phương pháp phát triển Python cấp độ cơ bản, bao gồm:

- **Khái niệm OOP nâng cao**: Thừa kế, Đa hình, Đóng gói, Trừu tượng
- **Nguyên tắc SOLID**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Design Patterns**: Strategy, Observer, Factory, Repository, Command patterns
- **Clean Architecture**: Tách biệt mối quan tâm, kiến trúc phân lớp

## ✨ Tính Năng

### Chức Năng Cốt Lõi
- 📖 **Quản lý Sách**: Thêm, cập nhật, xóa, tìm kiếm sách với thông tin chi tiết
- 👥 **Quản lý Thành viên**: Xử lý các loại thành viên khác nhau với đặc quyền khác nhau
- 📋 **Hệ thống Giao dịch**: Mượn, trả, gia hạn sách với tính toán phí phạt tự động
- 💰 **Quản lý Phí phạt**: Tính toán tự động và xử lý thanh toán
- 🔍 **Tìm kiếm Nâng cao**: Tìm kiếm và lọc theo nhiều tiêu chí
- 📊 **Báo cáo & Phân tích**: Thống kê toàn diện và theo dõi sách quá hạn

### Tính Năng Kỹ Thuật
- 🏗️ **Kiến trúc Module**: Tách biệt rõ ràng giữa models, services và utilities
- ✅ **Validation Dữ liệu**: Validation đầu vào toàn diện với validators tùy chỉnh
- 📱 **Giao diện CLI**: Giao diện dòng lệnh thân thiện người dùng
- 💾 **Lưu trữ Dữ liệu**: Lưu trữ dựa trên JSON với tự động save/load
- 🎨 **Định dạng Đầu ra**: Định dạng bảng chuyên nghiệp và tạo báo cáo
- 🔧 **Thiết kế Mở rộng**: Dễ dàng mở rộng với các tính năng mới

## 🏗️ Cấu Trúc Dự Án

```
LibraryManagement/
│
├── models/                 # Mô hình dữ liệu (Tầng Domain)
│   ├── __init__.py
│   ├── base.py            # Các lớp cơ sở trừu tượng
│   ├── book.py            # Entity Sách với logic nghiệp vụ
│   ├── member.py          # Entity Thành viên với thông tin liên lạc
│   └── transaction.py     # Giao dịch với tính toán phí phạt
│
├── services/              # Logic nghiệp vụ (Tầng Service)
│   ├── __init__.py
│   └── library_service.py # Service chính với các thao tác CRUD
│
├── utils/                 # Các hàm tiện ích (Tầng Infrastructure)
│   ├── __init__.py
│   ├── validators.py      # Tiện ích validation đầu vào
│   ├── formatters.py      # Tiện ích định dạng đầu ra
│   └── sorting.py         # Tiện ích sắp xếp và lọc
│
├── tests/                 # Unit tests (tùy chọn)
│   └── __init__.py
│
├── data/                  # Lưu trữ dữ liệu (tự động tạo)
│   ├── books.json
│   ├── members.json
│   └── transactions.json
│
├── main.py               # Điểm vào ứng dụng CLI
├── demo.py               # Demo tính năng
├── test_run.py           # Test chức năng nhanh
├── requirements.txt      # Dependencies dự án
└── README.md            # File này
```

## 🚀 Bắt Đầu

### Yêu Cầu Hệ Thống
- Python 3.8 trở lên
- Không cần dependencies bên ngoài (chỉ sử dụng thư viện chuẩn Python)

### Cài Đặt

1. **Clone hoặc tải dự án**
   ```bash
   git clone <repository-url>
   cd LibraryManagement
   ```

2. **Chạy ứng dụng**
   ```bash
   python3 main.py
   ```

3. **Tùy chọn: Tạo dữ liệu mẫu**
   - Sử dụng tùy chọn "Tạo Dữ liệu Mẫu" trong menu tiện ích
   - Điều này sẽ tạo dữ liệu sách và thành viên mẫu

### Hướng Dẫn Nhanh

1. **Khởi chạy ứng dụng**: `python3 main.py`
2. **Tạo dữ liệu mẫu**: Menu → Tiện ích Hệ thống → Tạo Dữ liệu Mẫu
3. **Thêm sách**: Menu → Quản lý Sách → Thêm Sách Mới
4. **Thêm thành viên**: Menu → Quản lý Thành viên → Thêm Thành viên Mới
5. **Mượn sách**: Menu → Quản lý Giao dịch → Mượn Sách
6. **Xem thống kê**: Menu → Báo cáo & Thống kê → Thống kê Thư viện

## 💡 Các Khái Niệm OOP Được Thể Hiện

### 1. Thừa Kế & Đa Hình
```python
# Entity cơ sở với chức năng chung
class BaseEntity(ABC):
    def __init__(self):
        self._id = str(uuid.uuid4())
        self._created_at = datetime.now()

# Các entity cụ thể thừa kế từ cơ sở
class Book(BaseEntity, Searchable, Validatable):
    # Triển khai cụ thể cho Sách

class Member(BaseEntity, Searchable, Validatable):
    # Triển khai cụ thể cho Thành viên
```

### 2. Đóng Gói
```python
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self._title = title  # Thuộc tính private
        self._status = BookStatus.AVAILABLE
    
    @property
    def title(self) -> str:
        return self._title  # Truy cập có kiểm soát
    
    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Tiêu đề không được để trống")
        self._title = value.strip()
        self._update_timestamp()
```

### 3. Trừu Tượng & Interface
```python
class Searchable(ABC):
    @abstractmethod
    def matches_search(self, query: str) -> bool:
        pass

class Validatable(ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass
```

### 4. Composition (Kết Hợp)
```python
class Member:
    def __init__(self, first_name: str, last_name: str, contact_info: ContactInfo = None):
        self._contact_info = contact_info or ContactInfo()
        # Member "có một" ContactInfo (composition)
```

## 🎨 Các Design Pattern Được Sử Dụng

### Repository Pattern
```python
class LibraryService:
    def __init__(self):
        self._books: Dict[str, Book] = {}
        self._members: Dict[str, Member] = {}
    
    def add_book(self, title: str, author: str, isbn: str) -> Book:
        # Đóng gói logic truy cập dữ liệu
```

### Strategy Pattern
```python
class BookSorter:
    @staticmethod
    def by_title(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        # Các chiến lược sắp xếp khác nhau
    
    @staticmethod
    def by_author(books: List[Book], order: SortOrder = SortOrder.ASC) -> List[Book]:
        # Các thuật toán có thể thay thế
```

### Command Pattern
```python
class Transaction:
    def process_transaction(self, processed_by: str) -> bool:
        # Đóng gói các thao tác giao dịch
```

## 📊 Tính Năng Nổi Bật Cho CV

### Kỹ Năng Kỹ Thuật Được Thể Hiện
- **Thiết kế Hướng Đối Tượng**: Hệ thống phân cấp lớp và mối quan hệ phức tạp
- **Design Patterns**: Nhiều pattern được triển khai phù hợp
- **Cấu trúc Dữ liệu**: Sử dụng hiệu quả dictionaries, lists và custom classes
- **Xử lý Lỗi**: Exception handling và validation toàn diện
- **Tổ chức Code**: Cấu trúc code sạch, modular và dễ bảo trì
- **Tài liệu**: Comments và docstrings đầy đủ
- **Type Hints**: Annotations kiểu Python hiện đại
- **Phát triển CLI**: Giao diện dòng lệnh thân thiện người dùng

### Độ Phức Tạp Logic Nghiệp Vụ
- **Kiến trúc Nhiều Tầng**: Tách biệt mối quan tâm rõ ràng
- **Tính toán Phức tạp**: Tính phí phạt, theo dõi quá hạn
- **Mối quan hệ Dữ liệu**: Kết nối giữa sách, thành viên và giao dịch
- **Quy tắc Nghiệp vụ**: Loại thành viên, giới hạn mượn, chính sách gia hạn
- **Logic Validation**: Validation ISBN, kiểm tra định dạng email
- **Tạo Báo cáo**: Thống kê, báo cáo quá hạn, hoạt động thành viên

### Thực Hành Kỹ Thuật Phần Mềm
- **Nguyên tắc SOLID**: Mỗi lớp có một trách nhiệm duy nhất
- **Nguyên tắc DRY**: Tái sử dụng code qua thừa kế và composition
- **Tách biệt Mối quan tâm**: Models, services và utilities riêng biệt
- **Khả năng Mở rộng**: Dễ dàng thêm tính năng mới mà không sửa code hiện có
- **Khả năng Bảo trì**: Cấu trúc rõ ràng và tài liệu toàn diện

## 🧪 Kiểm Thử Ứng Dụng

### Các Kịch Bản Kiểm Thử Thủ Công

1. **Quản lý Sách**
   - Thêm sách với các thể loại khác nhau
   - Tìm sách theo tiêu đề, tác giả hoặc ISBN
   - Cập nhật thông tin sách
   - Xóa sách (với validation)

2. **Quản lý Thành viên**
   - Tạo thành viên với các loại thành viên khác nhau
   - Kiểm tra hết hạn và gia hạn thành viên
   - Validate thông tin liên lạc

3. **Luồng Giao dịch**
   - Mượn sách (kiểm tra giới hạn và validation)
   - Trả sách (với tính phí phạt)
   - Gia hạn sách (kiểm tra giới hạn gia hạn)
   - Thanh toán phí phạt

4. **Xử lý Lỗi**
   - Thử các thao tác không hợp lệ (mượn sách không có sẵn)
   - Kiểm tra validation (email, ISBN không hợp lệ)
   - Kiểm tra quy tắc nghiệp vụ (vượt giới hạn mượn)

## 🔧 Tùy Chỉnh & Mở Rộng

### Thêm Tính Năng Mới
Thiết kế modular giúp dễ dàng mở rộng:

1. **Loại Entity Mới**: Tạo lớp mới thừa kế từ `BaseEntity`
2. **Validators Bổ sung**: Thêm quy tắc validation mới trong `validators.py`
3. **Báo cáo Tùy chỉnh**: Mở rộng formatters cho loại báo cáo mới
4. **Loại Giao dịch Mới**: Thêm vào enum `TransactionType`

### Tùy Chọn Cấu Hình
- Thời gian mượn (mặc định: 14 ngày)
- Tỷ lệ phí phạt (mặc định: 20,000 VNĐ/ngày)
- Giới hạn thành viên
- Giới hạn gia hạn

## 🎓 Kết Quả Học Tập

Dự án này thể hiện việc biết sử dụng:

1. **Lập trình Python Nâng cao**: Khái niệm OOP phức tạp, decorators, properties
2. **Kiến trúc Phần mềm**: Nguyên tắc clean architecture, design patterns
3. **Mô hình Dữ liệu**: Mối quan hệ phức tạp, triển khai logic nghiệp vụ
4. **Thiết kế Giao diện Người dùng**: Phát triển CLI, trải nghiệm người dùng
5. **Chất lượng Code**: Testing, documentation, maintainability
6. **Phát triển Chuyên nghiệp**: Cấu trúc dự án, sẵn sàng version control

## 🚀 Cách Chạy Nhanh

```bash
# Di chuyển vào thư mục dự án
cd LibraryManagement

# Chạy ứng dụng chính
python3 main.py

# Hoặc chạy test nhanh
python3 test_run.py

# Hoặc chạy demo đầy đủ
python3 demo.py
```

**🎯 Lưu ý**: Hãy sử dụng `python3` trên macOS và `python`  trên Windown