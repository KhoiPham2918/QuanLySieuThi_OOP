# He Thong Quan Ly Hang Hoa Sieu Thi

## Gioi thieu

Do an **Lap Trinh Huong Doi Tuong (OOP)** - He thong quan ly hang hoa sieu thi duoc xay dung bang **Python** va **PyQt6**. Ung dung ho tro day du cac chuc nang quan ly, tim kiem, sap xep va thong ke hang hoa.

## Cac tinh nang chinh

- **Quan ly danh muc:** Them, sua, xoa hang hoa
- **3 loai hang hoa:** Thuc pham, Dien may, Hang gia dung
- **Tim kiem nang cao:** Binary Search (theo ma), Linear Search (theo ten)
- **Sap xep:** Merge Sort va Quick Sort tren Linked List
- **Thong ke:** Tong so luong, hang dat/re nhat, canh bao het hang/het han
- **Luu tru du lieu:** Tu dong luu vao file JSON
- **Xuat tem bao hanh:** Cho hang dien may

## Cau truc du an

```
QuanLySieuThi_OOP/
├── main.py                     # File chay chinh
├── .gitignore                  # File bo qua
├── README.md                   # Huong dan su dung
├── kien_thuc.md                # Giai thich thuat toan (van dap)
├── data/
│   └── du_lieu.json            # Du lieu mau (6 san pham)
├── core/
│   ├── __init__.py
│   ├── nut.py                  # Node cho Doubly Linked List
│   ├── danh_sach_lien_ket.py   # Doubly Linked List + Sort + Search
│   ├── mo_hinh.py              # OOP: HangHoa, ThucPham, DienMay, HangGiaDung
│   └── ngoai_le.py             # Ngoai le: LoiTrungMa, LoiFile, LoiNhapLieu
└── ui/
    ├── __init__.py
    ├── giao_dien.py            # Giao dien chinh (PyQt6)
    └── dinh_dang.qss           # File dinh dang giao dien
```

## Cai dat va chay

### 1. Cai dat thu vien
```bash
pip install PyQt6
```

### 2. Chay chuong trinh
```bash
python main.py
```

## Cong nghe su dung

| Ky thuat | Chi tiet |
|----------|----------|
| Ngon ngu | Python 3 |
| GUI | PyQt6 |
| Cau truc du lieu | Doubly Linked List (tu cai dat) |
| Thuat toan sap xep | Merge Sort, Quick Sort |
| Thuat toan tim kiem | Linear Search, Binary Search |
| Luu tru du lieu | JSON |
| OOP | Ke thua, Da hinh, Dong goi, ABC |