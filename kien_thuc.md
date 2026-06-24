# Kien Thuc Ve Thuat Toan Va Cau Truc Du Lieu

> File nay giai thich cac thuat toan va cau truc du lieu su dung trong du an, viet theo kieu "noi chuyen voi ban than" de de hieu.

---

## 1. Danh Sach Lien Ket Doi (Doubly Linked List)

### Noi ro la gi?

Hoi tu nhien: Ban dang dung **list** cua Python (vd: `ds = [1, 2, 3]`), the nao ban co the them 1 phan tu vao giua ma khong can dich toan bo phan tu phia sau? 

That ra, Python list da lam duoc roi nhung ben duoi no, no van phai dich chuyen. Nhung voi **Linked List**, viec them vao giua chi can thay doi 2 con tro la xong.

### Cau truc 1 Node

Moi Node co 3 thanh phan:
- **du_lieu**: Luu doi tuong hang hoa
- **truoc**: Con tro toi Node phia truoc
- **sau**: Con tro toi Node phia sau

```
[NULL] <- [Node A] <=> [Node B] <=> [Node C] -> [NULL]
          dau                              cuoi
```

### Vi sao dung Double Linked List thay vi Single?

- **Single** chi co con tro `sau` -> muon lui lai phai duyet tu dau
- **Double** co ca `truoc` va `sau` -> co the duyet **ca 2 chieu**: tu dau ra cuoi hoac tu cuoi ve dau

Trong sieu thi, dieu nay huu ich khi ban muon xem cac hang hoa **moi nhap** (nam o cuoi danh sach) ma khong can duyet tu dau.

### Do phuc tap

| Hanh dong | List (Python) | Linked List |
|-----------|---------------|-------------|
| Them dau  | O(n)          | O(1)        |
| Them cuoi | O(1)          | O(1)*       |
| Them giua | O(n)          | O(1) neu da co node |
| Xoa giua  | O(n)          | O(1) neu da co node |
| Truy cap ngau nhien | O(1) | O(n) |

*O(1) neu luu con tro `cuoi`

---

## 2. Merge Sort (Sap Xep Gop)

### Noi ro la gi?

Hoi tu nhien: Ban co 2 bo bai da sap xep, lam sao gop thanh 1 bo da sap xep?

Vi du:
```
Bo 1: [1, 4, 7]    Bo 2: [2, 3, 8]
```

Ban chi can so sanh phan tu dau tien cua tung bo:
- 1 vs 2 -> lay 1
- 4 vs 2 -> lay 2
- 4 vs 3 -> lay 3
- 4 vs 8 -> lay 4
- 7 vs 8 -> lay 7
- con lai 8 -> lay 8

Ket qua: `[1, 2, 3, 4, 7, 8]`

### Merge Sort lam gi?

No chia danh sach thanh 2 nua -> sap xep tung nha -> gop lai.

```
[5, 3, 8, 1, 4]
       |
   CHIA 2
       |
[5, 3, 8]     [1, 4]
   |              |
 CHIA 2         CHIA 2
   |              |
[5, 3] [8]    [1]  [4]
   |     |      |    |
[3, 5] [8]    [1, 4]
   |              |
[3, 5, 8]    [1, 4]
       |
   GOP LAI
       |
[1, 3, 4, 5, 8]
```

### Do phuc tap

- **Thoi gian**: O(n log n) - o dinh nhat, kem nhat cung vay
- **Khong gian**: O(log n) do de quy (voi linked list khong can tao mang trung gian nhu array)

### Ung dung trong du an

Chon Merge Sort de sap xep danh sach hang hoa theo gia ban, ten, so luong. Merge Sort phu hop voi linked list vi khong can truy cap ngau nhien.

---

## 3. Quick Sort (Sap Xep Nhanh)

### Noi ro la gi?

Hoi tu nhien: Ban muon sap xep dong xu. Chon 1 dong xu lam "muc" (pivot). 
- Dong xu nho hon -> de vao ben trai
- Dong xu lon hon -> de vao ben phai
- Lap lai voi tung ben

Vi du sap xep `[5, 3, 8, 1, 4]`, chon 4 lam pivot:
```
[3, 1]  [4]  [5, 8]
   |           |
 [1, 3]      [5, 8] -> [1, 3, 4, 5, 8]
```

### Do phuc tap

- **Thoi gian trung binh**: O(n log n)
- **Thoi gian xau nhat**: O(n^2) - khi mang da sap xep roi va chon sai pivot
- **Khong gian**: O(log n) do de quy

### Merge Sort vs Quick Sort

| Tieu chi | Merge Sort | Quick Sort |
|----------|-----------|------------|
| Do phuc tap trung binh | O(n log n) | O(n log n) |
| Do phuc tap xau nhat | O(n log n) | O(n^2) |
| Tinh on dinh | Luon O(n log n) | Phu thuoc pivot |
| Bo nho | O(log n) | O(log n) |
| Phu hop voi LL | Rat phu hop | Phu hop |

---

## 4. Linear Search (Tim Kiem Tuyen Tinh)

### Noi ro la gi?

Hoi tu nhien: Ban mat mat roi, muon tim cai but trong cai hop. Ban phai xem tung cai mot tu dau den cuoi. Do la **Linear Search**.

### Cach hoat dong

```python
# Tim "Cà phê" trong danh sach
for hang in danh_sach:
    if "cà phê" in hang.ten:
        return hang
```

### Do phuc tap

- **Thoi gian**: O(n) - trong truong hop xau nhat phai duyet toan bo
- **Khong can sap xep** truoc

### Ung dung trong du an

Dung de tim kiem theo **ten hang** (vi ten khong the sap xep de dung Binary Search).

---

## 5. Binary Search (Tim Kiem Nhi Phan)

### Noi ro la gi?

Hoi tu nhun: Ban muon tim tu trong tu dien. Tu dien da sap xep theo bang chu cai. Ban se khong doc tu dau den cuoi, ma mo ra o giua, neu tu can tim dung truoc o giua thi chi can tim nua truoc, nguoc lai thi tim nua sau. Do la **Binary Search**.

### Cach hoat dong

Tim ma hang "DM002" trong danh sach da sap xep:
```
[DM001, DM002, DM003, GD001, GD002, TP001, TP002]
 ^trai                            ^phai
          ^giua (GD001)

"DM002" < "GD001" -> chi tim nua ben trai
[DM001, DM002, DM003]
 ^trai         ^phai
     ^giua (DM002)

"DM002" == "DM002" -> TIM THAY!
```

### Do phuc tap

- **Thoi gian**: O(log n) - cuc ky nhanh!
- **DIEU KIEN**: Danh sach **PHAI DA SAP XEP**

### Ung dung trong du an

Dung de tim kiem theo **ma hang** (sap xep theo ma truoc, roi moi binary search).

| So luong hang | Linear Search | Binary Search |
|---------------|---------------|---------------|
| 10            | toi da 10 buoc | toi da 4 buoc |
| 100           | toi da 100 buoc | toi da 7 buoc |
| 1000          | toi da 1000 buoc | toi da 10 buoc |
| 1,000,000     | toi da 1,000,000 buoc | toi da 20 buoc |

---

## 6. OOP (Lap Trinh Huong Doi Tuong)

### 4 tinh chat OOP trong du an

#### A. Ke Thua (Inheritance)

```
HangHoa (lop co so)
  ├── ThucPham (ke thua thuoc tinh: ma_hang, ten_hang, so_luong, gia_nhap)
  ├── DienMay  (ke thua thuoc tinh: ma_hang, ten_hang, so_luong, gia_nhap)
  └── HangGiaDung (ke thua thuoc tinh: ma_hang, ten_hang, so_luong, gia_nhap)
```

Moi lop con them thuoc tinh rieng cua no:
- ThucPham: `ngay_san_xuat`, `ngay_het_han`
- DienMay: `thoi_gian_bao_hanh`, `cong_suat`
- HangGiaDung: `chat_lieu`

#### B. Da Hinh (Polymorphism)

Phuong thuc `tinh_gia_ban()` la **phuong thuc truu tuong** trong lop co so. Moi lop con cai dat cach tinh khac nhau:

| Lop | Cong thuc |
|-----|-----------|
| ThucPham | Gia nhap * 1.10 * 0.95 = Gia nhap * 1.045 |
| DienMay | Gia nhap * 1.20 * 0.90 = Gia nhap * 1.08 |
| HangGiaDung | Gia nhap * 1.15 |

Khi goi `hang.tinh_gia_ban()`, Python tu dong goi phuong thuc dung cua lop do. Khong can viet `if loai == "ThucPham"` hay switch-case.

#### C. Dong Goi (Encapsulation)

- Thuoc tinh cua lop duoc truy cap qua phuong thuc (getter/setter ngam)
- Ngoai le tu dinh nghia (LoiTrungMa, LoiFile, LoiNhapLieu) bao ve du lieu
- Form nhap lieu kiem tra hop le truoc khi tao doi tuong

#### D. Lop Truu Tuong (ABC)

`HangHoa` la **Abstract Base Class** (lop co so truu tuong). No **khong the tao doi tuong** truc tiep (vi co phuong thuc `@abstractmethod`). Ban **bat buoc** phai ke thua no va cai dat `tinh_gia_ban()`.

---

## 7. Xu Ly Ngoai Le (Exception Handling)

### 3 ngoai le tu dinh nghia

1. **LoiTrungMa**: Khi them hang ma trung ma da co. Giup tranh lap du lieu.
2. **LoiFile**: Khi file JSON bi hong, khong ton tai, hoac sai dinh dang.
3. **LoiNhapLieu**: Khi nguoi dung nhap sai (nhap chu vao o gia tien, gia am, thieu truong bat buoc).

### Vi sao can ngoai le tu dinh nghia thay vi dung ValueError?

Vi khi gap loi, chuong trinh can biet CHINH XAC loi gi de hien thi thong bao phu hop cho nguoi dung. Vi du: "Ma hang TP001 da ton tai!" ro rang hon la "Co loi xay ra!".

---

## 8. JSON (JavaScript Object Notation)

### Vi sao dung JSON de luu tru?

- **De doc**: Con nguoi co the mo va doc hieu
- **Ho tro Python**: Co san module `json` trong Python
- **Linh hoat**: Luu duoc ca chuoi, so, danh sach, dictionary
- **Pho bien**: Duoc su dung rong rai trong nhieu ngon ngu lap trinh

### Cach hoat dong

1. **Luu**: Moi hang hoa co phuong thuc `to_dict()` chuyen doi thanh dictionary. Toan bo danh sach duoc chuyen thanh list va ghi vao file JSON.
2. **Doc**: Doc file JSON -> list dictionary -> dung ham `tao_hang_hoa_tu_dict()` (Factory Pattern) tao lai doi tuong tuong ung.