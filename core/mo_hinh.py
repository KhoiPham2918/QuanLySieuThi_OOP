"""
mo_hinh.py - Dinh nghia cac lop OOP cho he thong quan ly sieu thi

Cau truc ke thua:
  HangHoa (Lop co so - Abstract Base Class)
    ├── ThucPham
    ├── DienMay
    └── HangGiaDung

Ap dung:
  - Ke thua (Inheritance)
  - Da hinh (Polymorphism) qua phuong thuc truu tuong tinh_gia_ban()
  - Dong goi (Encapsulation) qua thuoc tinh private
  - ABC (Abstract Base Class) cho lop co so
"""

from abc import ABC, abstractmethod
from datetime import datetime, date


class HangHoa(ABC):
    """
    Lop co so (Base Class) cho tat ca loai hang hoa.

    Thuoc tinh:
      - ma_hang: Ma duy nhat cua hang
      - ten_hang: Ten san pham
      - so_luong: So luong ton kho
      - gia_nhap: Gia von (gia nhap vao)
    """

    def __init__(self, ma_hang, ten_hang, so_luong, gia_nhap):
        self.ma_hang = str(ma_hang).strip()
        self.ten_hang = str(ten_hang).strip()
        self.so_luong = int(so_luong)
        self.gia_nhap = float(gia_nhap)

    @abstractmethod
    def tinh_gia_ban(self):
        """
        Phuong thuc truu tuong - Tinh gia ban cua hang hoa.
        Moi lop dan xuat phai cai dat phuong thuc nay.
        """
        pass

    def kiem_tra_ton_kho(self):
        """
        Canh bao neu so luong ton kho it hon 5.

        Returns:
            bool: True neu so luong < 5 (sap het hang), False neu con du.
        """
        return self.so_luong < 5

    def loai_hang(self):
        """Tra ve ten loai hang (de hien thi trong giao dien)."""
        return self.__class__.__name__

    def thong_tin_tom_tat(self):
        """Tra ve chuoi thong tin tom tat cua hang hoa."""
        return (f"[{self.ma_hang}] {self.ten_hang} | "
                f"SL: {self.so_luong} | Gia ban: {self.tinh_gia_ban():,.0f} VND")

    def __str__(self):
        return (f"{self.loai_hang()} - Ma: {self.ma_hang}, "
                f"Ten: {self.ten_hang}, SL: {self.so_luong}, "
                f"Gia nhap: {self.gia_nhap:,.0f}, Gia ban: {self.tinh_gia_ban():,.0f}")

    def to_dict(self):
        """Chuyen doi doi tuong thanh dictionary (de luu vao JSON)."""
        return {
            "loai": self.loai_hang(),
            "ma_hang": self.ma_hang,
            "ten_hang": self.ten_hang,
            "so_luong": self.so_luong,
            "gia_nhap": self.gia_nhap
        }


class ThucPham(HangHoa):
    """
    Lop Thuc Pham - Ke thua tu HangHoa.

    Thuoc tinh rieng:
      - ngay_san_xuat: Ngay san xuat (str dang YYYY-MM-DD)
      - ngay_het_han: Ngay het han (str dang YYYY-MM-DD)

    Da hinh (tinh_gia_ban):
      Gia ban = Gia nhap + (Gia nhap * 10%) - VAT thuc pham thap (5%)
      Tuc la: Gia ban = Gia nhap * 1.10 * 0.95 = Gia nhap * 1.045
    """

    # VAT thuc pham thap (5%)
    TI_LE_VAT = 0.05
    # Ti le loi nhuan thuc pham (10%)
    TI_LE_LOI_NHUAN = 0.10

    def __init__(self, ma_hang, ten_hang, so_luong, gia_nhap,
                 ngay_san_xuat, ngay_het_han):
        super().__init__(ma_hang, ten_hang, so_luong, gia_nhap)
        self.ngay_san_xuat = str(ngay_san_xuat).strip()
        self.ngay_het_han = str(ngay_het_han).strip()

    def tinh_gia_ban(self):
        """
        Da hinh - Tinh gia ban thuc pham.
        Gia ban = Gia nhap * (1 + 10%) * (1 - 5%) = Gia nhap * 1.045
        """
        gia_sau_loi_nhuan = self.gia_nhap * (1 + self.TI_LE_LOI_NHUAN)
        gia_ban = gia_sau_loi_nhuan * (1 - self.TI_LE_VAT)
        return round(gia_ban, 2)

    def kiem_tra_het_han(self):
        """
        Kiem tra san pham co sap het han hay khong.

        Returns:
            bool: True neu da het han hoac con duoi 7 ngay, False neu con han lau.
        """
        try:
            hom_nay = date.today()
            han_dung = datetime.strptime(self.ngay_het_han, "%Y-%m-%d").date()
            con_lai = (han_dung - hom_nay).days
            return con_lai <= 7
        except ValueError:
            return False

    def so_ngay_con_lai(self):
        """Tra ve so ngay con lai den khi het han."""
        try:
            hom_nay = date.today()
            han_dung = datetime.strptime(self.ngay_het_han, "%Y-%m-%d").date()
            return (han_dung - hom_nay).days
        except ValueError:
            return -1

    def to_dict(self):
        """Chuyen doi ThucPham thanh dictionary."""
        data = super().to_dict()
        data["ngay_san_xuat"] = self.ngay_san_xuat
        data["ngay_het_han"] = self.ngay_het_han
        return data


class DienMay(HangHoa):
    """
    Lop Dien May - Ke thua tu HangHoa.

    Thuoc tinh rieng:
      - thoi_gian_bao_hanh: Thoi gian bao hanh (tinh bang thang)
      - cong_suat: Cong suat cua thiet bi (VD: "150W", "500W")

    Da hinh (tinh_gia_ban):
      Gia ban = Gia nhap + (Gia nhap * 20%) - VAT dien may cao (10%)
      Tuc la: Gia ban = Gia nhap * 1.20 * 0.90 = Gia nhap * 1.08
    """

    # VAT dien may cao (10%)
    TI_LE_VAT = 0.10
    # Ti le loi nhuan dien may (20%)
    TI_LE_LOI_NHUAN = 0.20

    def __init__(self, ma_hang, ten_hang, so_luong, gia_nhap,
                 thoi_gian_bao_hanh, cong_suat):
        super().__init__(ma_hang, ten_hang, so_luong, gia_nhap)
        self.thoi_gian_bao_hanh = int(thoi_gian_bao_hanh)
        self.cong_suat = str(cong_suat).strip()

    def tinh_gia_ban(self):
        """
        Da hinh - Tinh gia ban dien may.
        Gia ban = Gia nhap * (1 + 20%) * (1 - 10%) = Gia nhap * 1.08
        """
        gia_sau_loi_nhuan = self.gia_nhap * (1 + self.TI_LE_LOI_NHUAN)
        gia_ban = gia_sau_loi_nhuan * (1 - self.TI_LE_VAT)
        return round(gia_ban, 2)

    def xuat_tem_bao_hanh(self):
        """
        Xuat tem bao hanh cho dien may.

        Returns:
            str: Chuoi thong tin bao hanh.
        """
        return (f"=== TEM BAO HANH ===\n"
                f"San pham: {self.ten_hang}\n"
                f"Ma hang: {self.ma_hang}\n"
                f"Thoi gian bao hanh: {self.thoi_gian_bao_hanh} thang\n"
                f"Cong suat: {self.cong_suat}\n"
                f"Gia ban: {self.tinh_gia_ban():,.0f} VND\n"
                f"=====================")

    def to_dict(self):
        """Chuyen doi DienMay thanh dictionary."""
        data = super().to_dict()
        data["thoi_gian_bao_hanh"] = self.thoi_gian_bao_hanh
        data["cong_suat"] = self.cong_suat
        return data


class HangGiaDung(HangHoa):
    """
    Lop Hang Gia Dung - Ke thua tu HangHoa.

    Thuoc tinh rieng:
      - chat_lieu: Vat lieu lam hang (Nhua, Go, Thep, ...)

    Da hinh (tinh_gia_ban):
      Gia ban = Gia nhap + (Gia nhap * 15%) = Gia nhap * 1.15
      Khong ap dung VAT (hang gia dung thuong khong co VAT rieng).
    """

    # Ti le loi nhuan hang gia dung (15%)
    TI_LE_LOI_NHUAN = 0.15

    def __init__(self, ma_hang, ten_hang, so_luong, gia_nhap, chat_lieu):
        super().__init__(ma_hang, ten_hang, so_luong, gia_nhap)
        self.chat_lieu = str(chat_lieu).strip()

    def tinh_gia_ban(self):
        """
        Da hinh - Tinh gia ban hang gia dung.
        Gia ban = Gia nhap * (1 + 15%) = Gia nhap * 1.15
        """
        gia_ban = self.gia_nhap * (1 + self.TI_LE_LOI_NHUAN)
        return round(gia_ban, 2)

    def to_dict(self):
        """Chuyen doi HangGiaDung thanh dictionary."""
        data = super().to_dict()
        data["chat_lieu"] = self.chat_lieu
        return data


def tao_hang_hoa_tu_dict(data):
    """
    Ham nha may (Factory Function) - Tao doi tuong hang hoa tu dictionary.

    Ham nay doc truong "loai" trong dictionary de biet can tao lop nao.
    Dieu nay giup khoi phuc du lieu tu file JSON mot cach de dang.

    Args:
        data (dict): Dictionary chua thong tin hang hoa.

    Returns:
        HangHoa: Doi tuong hang hoa (ThucPham, DienMay, hoac HangGiaDung).

    Raises:
        ValueError: Neu loai hang khong hop le.
    """
    loai = data.get("loai", "")
    ma_hang = data["ma_hang"]
    ten_hang = data["ten_hang"]
    so_luong = data["so_luong"]
    gia_nhap = data["gia_nhap"]

    if loai == "ThucPham":
        return ThucPham(
            ma_hang=ma_hang,
            ten_hang=ten_hang,
            so_luong=so_luong,
            gia_nhap=gia_nhap,
            ngay_san_xuat=data["ngay_san_xuat"],
            ngay_het_han=data["ngay_het_han"]
        )
    elif loai == "DienMay":
        return DienMay(
            ma_hang=ma_hang,
            ten_hang=ten_hang,
            so_luong=so_luong,
            gia_nhap=gia_nhap,
            thoi_gian_bao_hanh=data["thoi_gian_bao_hanh"],
            cong_suat=data["cong_suat"]
        )
    elif loai == "HangGiaDung":
        return HangGiaDung(
            ma_hang=ma_hang,
            ten_hang=ten_hang,
            so_luong=so_luong,
            gia_nhap=gia_nhap,
            chat_lieu=data["chat_lieu"]
        )
    else:
        raise ValueError(f"Loai hang khong hop le: {loai}")