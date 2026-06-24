"""
ngoai_le.py - Cac ngoai le tu dinh nghia cho he thong quan ly sieu thi

Gom 3 ngoai le chinh:
  1. LoiTrungMa   - Khi nhap ma hang da ton tai
  2. LoiFile      - Khi file du lieu bi hong hoac khong tim thay
  3. LoiNhapLieu  - Khi nguoi dung nhap sai du lieu
"""


class LoiTrungMa(Exception):
    """
    Ngoai le khi ma hang hoa da ton tai trong he thong.

    Duoc nem ra khi nguoi dung thu them hang hoa moi ma co ma
    trung voi ma hang da co trong danh sach lien ket.
    """

    def __init__(self, ma_hang):
        self.ma_hang = ma_hang
        super().__init__(f"Ma hang '{ma_hang}' da ton tai trong he thong!")


class LoiFile(Exception):
    """
    Ngoai le khi co van de voi file du lieu.

    Duoc nem ra khi:
      - File JSON khong ton tai
      - File bi huong (khong doc duoc)
      - Du lieu trong file sai dinh dang
    """

    def __init__(self, ten_file, loi="Khong the doc file"):
        self.ten_file = ten_file
        self.loi = loi
        super().__init__(f"Loi file '{ten_file}': {loi}")


class LoiNhapLieu(Exception):
    """
    Ngoai le khi nguoi dung nhap du lieu sai.

    Duoc nem ra khi:
      - Nhap chu vao o chi nhan so
      - Nhap gia tien am
      - Nhap so luong am
      - Thieu truong bat buoc
    """

    def __init__(self, truong, noi_dung="Du lieu khong hop le"):
        self.truong = truong
        self.noi_dung = noi_dung
        super().__init__(f"Loi nhap lieu ({truong}): {noi_dung}")