"""
danh_sach_lien_ket.py - Danh sach lien ket doi (Doubly Linked List) cho quan ly hang hoa

Cai dat day du:
  - Them / Xoa / Sua hang hoa
  - Merge Sort (theo gia ban, so luong, ten)
  - Quick Sort (theo gia ban, so luong, ten)
  - Linear Search (tim theo ten)
  - Binary Search (tim theo ma hang - can sap xep truoc)
  - Thong ke (tong so luong, hang dat nhat, re nhat, canh bao het hang)
  - Luu / Doc du lieu tu file JSON
  - Tim kiem theo loai hang (loc)
"""

import json
import os
from core.nut import Nut
from core.ngoai_le import LoiTrungMa, LoiFile
from core.mo_hinh import tao_hang_hoa_tu_dict


class DanhSachLienKet:
    """
    Lop Danh Sach Lien Ket Doi (Doubly Linked List) quan ly hang hoa.

    Moi Node chua 1 doi tuong HangHoa (hoac lop dan xuat).
    Ho tro duyet xuoi (dau -> cuoi) va nguoc (cuoi -> dau).
    """

    def __init__(self):
        """Khoi tao danh sach rong."""
        self.dau = None
        self.cuoi = None
        self.so_luong_node = 0

    # ─────────────────────────────────────────────
    # CAC PHUONG THUC CO BAN (Them / Xoa / Sua)
    # ─────────────────────────────────────────────

    def la_rong(self):
        """Kiem tra danh sach co rong khong."""
        return self.dau is None

    def them_vao_cuoi(self, hang_hoa):
        """
        Them hang hoa vao cuoi danh sach.

        Args:
            hang_hoa: Doi tuong HangHoa can them.

        Raises:
            LoiTrungMa: Neu ma hang da ton tai.
        """
        # Kiem tra trung ma truoc khi them
        if self.tim_theo_ma(hang_hoa.ma_hang) is not None:
            raise LoiTrungMa(hang_hoa.ma_hang)

        nut_moi = Nut(hang_hoa)

        if self.la_rong():
            self.dau = nut_moi
            self.cuoi = nut_moi
        else:
            self.cuoi.sau = nut_moi
            nut_moi.truoc = self.cuoi
            self.cuoi = nut_moi

        self.so_luong_node += 1

    def them_vao_dau(self, hang_hoa):
        """
        Them hang hoa vao dau danh sach.

        Args:
            hang_hoa: Doi tuong HangHoa can them.

        Raises:
            LoiTrungMa: Neu ma hang da ton tai.
        """
        if self.tim_theo_ma(hang_hoa.ma_hang) is not None:
            raise LoiTrungMa(hang_hoa.ma_hang)

        nut_moi = Nut(hang_hoa)

        if self.la_rong():
            self.dau = nut_moi
            self.cuoi = nut_moi
        else:
            nut_moi.sau = self.dau
            self.dau.truoc = nut_moi
            self.dau = nut_moi

        self.so_luong_node += 1

    def xoa_theo_ma(self, ma_hang):
        """
        Xoa hang hoa theo ma hang.

        Args:
            ma_hang (str): Ma hang can xoa.

        Returns:
            HangHoa: Doi tuong hang hoa da bi xoa.

        Raises:
            ValueError: Neu khong tim thay ma hang.
        """
        nut = self.tim_nut_theo_ma(ma_hang)
        if nut is None:
            raise ValueError(f"Khong tim thay hang hoa co ma '{ma_hang}'")

        return self._xoa_nut(nut)

    def _xoa_nut(self, nut):
        """Xoa mot node khoi danh sach (phuong thuc noi bo)."""
        if nut.truoc is not None:
            nut.truoc.sau = nut.sau
        else:
            # Xoa node dau tien
            self.dau = nut.sau

        if nut.sau is not None:
            nut.sau.truoc = nut.truoc
        else:
            # Xoa node cuoi cung
            self.cuoi = nut.truoc

        self.so_luong_node -= 1
        return nut.du_lieu

    def sua_theo_ma(self, ma_hang, hang_hoa_moi):
        """
        Cap nhat thong tin hang hoa.

        Args:
            ma_hang (str): Ma hang can sua.
            hang_hoa_moi: Doi tuong hang hoa moi.

        Returns:
            HangHoa: Doi tuong hang hoa cu (da bi thay the).

        Raises:
            ValueError: Neu khong tim thay ma hang.
        """
        nut = self.tim_nut_theo_ma(ma_hang)
        if nut is None:
            raise ValueError(f"Khong tim thay hang hoa co ma '{ma_hang}'")

        hang_cu = nut.du_lieu
        nut.du_lieu = hang_hoa_moi
        return hang_cu

    def xoa_toan_bo(self):
        """Xoa toan bo danh sach."""
        self.dau = None
        self.cuoi = None
        self.so_luong_node = 0

    # ─────────────────────────────────────────────
    # TIM KIEM (Searching)
    # ─────────────────────────────────────────────

    def tim_nut_theo_ma(self, ma_hang):
        """
        Tim node theo ma hang (dung Linear Search).

        Args:
            ma_hang (str): Ma hang can tim.

        Returns:
            Nut: Node chua hang hoa, hoac None neu khong tim thay.
        """
        hien_tai = self.dau
        while hien_tai is not None:
            if hien_tai.du_lieu.ma_hang == ma_hang:
                return hien_tai
            hien_tai = hien_tai.sau
        return None

    def tim_theo_ma(self, ma_hang):
        """
        Tim hang hoa theo ma hang.

        Args:
            ma_hang (str): Ma hang can tim.

        Returns:
            HangHoa: Doi tuong hang hoa, hoac None neu khong tim thay.
        """
        nut = self.tim_nut_theo_ma(ma_hang)
        return nut.du_lieu if nut else None

    def tim_theo_ten(self, tu_khoa):
        """
        Tim kiem hang hoa theo ten (Linear Search).

        Args:
            tu_khoa (str): Tu khoa tim kiem (khong phan biet hoa/thuong).

        Returns:
            DanhSachLienKet: Danh sach moi chua cac ket qua.
        """
        tu_khoa = tu_khoa.lower().strip()
        ket_qua = DanhSachLienKet()
        hien_tai = self.dau

        while hien_tai is not None:
            ten = hien_tai.du_lieu.ten_hang.lower()
            if tu_khoa in ten:
                ket_qua.them_vao_cuoi_khong_kiem_tra_trung(hien_tai.du_lieu)
            hien_tai = hien_tai.sau

        return ket_qua

    def tim_theo_loai(self, loai):
        """
        Loc hang hoa theo loai (ThucPham, DienMay, HangGiaDung).

        Args:
            loai (str): Ten loai hang can loc.

        Returns:
            DanhSachLienKet: Danh sach moi chua cac ket qua.
        """
        ket_qua = DanhSachLienKet()
        hien_tai = self.dau

        while hien_tai is not None:
            if hien_tai.du_lieu.loai_hang() == loai:
                ket_qua.them_vao_cuoi_khong_kiem_tra_trung(hien_tai.du_lieu)
            hien_tai = hien_tai.sau

        return ket_qua

    def tim_kiem_nhi_phan(self, ma_hang):
        """
        Tim kiem nhi phan (Binary Search) theo ma hang.

        LUU Y: Chi hoat dong dung khi danh sach DA DUOC SAP XEP theo ma hang.

        Args:
            ma_hang (str): Ma hang can tim.

        Returns:
            HangHoa: Doi tuong hang hoa, hoac None neu khong tim thay.
        """
        # Chuyen danh sach lien ket thanh list tam thoi de truy cap chi so
        ds_tam = self.chuyen_sang_list()
        if not ds_tam:
            return None

        trai = 0
        phai = len(ds_tam) - 1

        while trai <= phai:
            giua = (trai + phai) // 2
            ma_giua = ds_tam[giua].ma_hang

            if ma_giua == ma_hang:
                return ds_tam[giua]
            elif ma_giua < ma_hang:
                trai = giua + 1
            else:
                phai = giua - 1

        return None

    def them_vao_cuoi_khong_kiem_tra_trung(self, hang_hoa):
        """Them vao cuoi khong kiem tra trung ma (dung cho ket qua tim kiem)."""
        nut_moi = Nut(hang_hoa)
        if self.la_rong():
            self.dau = nut_moi
            self.cuoi = nut_moi
        else:
            self.cuoi.sau = nut_moi
            nut_moi.truoc = self.cuoi
            self.cuoi = nut_moi
        self.so_luong_node += 1

    # ─────────────────────────────────────────────
    # SAP XEP (Sorting)
    # ─────────────────────────────────────────────

    def sap_xep_merge(self, tieu_chi="gia_ban", tang_dan=True):
        """
        Sap xep danh sach bang Merge Sort.

        Args:
            tieu_chi (str): "gia_ban", "so_luong", hoac "ten".
            tang_dan (bool): True = tang dan, False = giam dan.
        """
        if self.dau is None or self.dau.sau is None:
            return

        self.dau = self._merge_sort(self.dau, tieu_chi, tang_dan)

        # Cap nhat lai con tro cuoi
        hien_tai = self.dau
        while hien_tai.sau is not None:
            hien_tai = hien_tai.sau
        self.cuoi = hien_tai

    def _merge_sort(self, dau, tieu_chi, tang_dan):
        """Merge Sort - phan de tri (recursive)."""
        if dau is None or dau.sau is None:
            return dau

        # Tim diem giua
        cham = dau
        nhanh = dau.sau
        while nhanh is not None and nhanh.sau is not None:
            cham = cham.sau
            nhanh = nhanh.sau.sau

        giua = cham.sau
        cham.sau = None
        if giua is not None:
            giua.truoc = None

        # De quy sap xep 2 nua
        trai = self._merge_sort(dau, tieu_chi, tang_dan)
        phai = self._merge_sort(giua, tieu_chi, tang_dan)

        # Gop 2 nua da sap xep
        return self._merge(trai, phai, tieu_chi, tang_dan)

    def _merge(self, trai, phai, tieu_chi, tang_dan):
        """Gop 2 danh sach da sap xep thanh 1 danh sach da sap xep."""
        dummy = Nut()
        hien_tai = dummy

        while trai is not None and phai is not None:
            if self._so_sanh(trai.du_lieu, phai.du_lieu, tieu_chi, tang_dan):
                hien_tai.sau = trai
                trai.truoc = hien_tai
                trai = trai.sau
            else:
                hien_tai.sau = phai
                phai.truoc = hien_tai
                phai = phai.sau
            hien_tai = hien_tai.sau

        # Noi phan con lai
        if trai is not None:
            hien_tai.sau = trai
            trai.truoc = hien_tai
        if phai is not None:
            hien_tai.sau = phai
            phai.truoc = hien_tai

        ket_qua = dummy.sau
        if ket_qua is not None:
            ket_qua.truoc = None
        return ket_qua

    def sap_xep_quick(self, tieu_chi="gia_ban", tang_dan=True):
        """
        Sap xep danh sach bang Quick Sort.

        Args:
            tieu_chi (str): "gia_ban", "so_luong", hoac "ten".
            tang_dan (bool): True = tang dan, False = giam dan.
        """
        if self.dau is None or self.dau.sau is None:
            return

        self.dau = self._quick_sort(self.dau, tieu_chi, tang_dan)

        # Cap nhat lai con tro cuoi
        hien_tai = self.dau
        while hien_tai.sau is not None:
            hien_tai = hien_tai.sau
        self.cuoi = hien_tai

    def _quick_sort(self, dau, tieu_chi, tang_dan):
        """Quick Sort - phan de tri (recursive)."""
        if dau is None or dau.sau is None:
            return dau

        # Chon pivot la node cuoi (dung ham helper de lay cuoi)
        pivot = self._lay_node_cuoi(dau)
        nho = []
        bang = []
        lon = []

        hien_tai = dau
        while hien_tai is not None:
            if hien_tai == pivot:
                hien_tai = hien_tai.sau
                continue
            if self._so_sanh(hien_tai.du_lieu, pivot.du_lieu, tieu_chi, tang_dan):
                nho.append(hien_tai)
            elif self._so_sanh(pivot.du_lieu, hien_tai.du_lieu, tieu_chi, tang_dan):
                lon.append(hien_tai)
            else:
                bang.append(hien_tai)
            hien_tai = hien_tai.sau

        # De quy sap xep cac phan
        nho_sort = self._quick_sort(self._xay_danh_sach_tu_list(nho), tieu_chi, tang_dan)
        lon_sort = self._quick_sort(self._xay_danh_sach_tu_list(lon), tieu_chi, tang_dan)

        # Noi lai: nho + bang + pivot + lon
        return self._noi_ba_phan(nho_sort, bang, pivot, lon_sort)

    def _lay_node_cuoi(self, dau):
        """Lay node cuoi cung tu dau."""
        hien_tai = dau
        while hien_tai.sau is not None:
            hien_tai = hien_tai.sau
        return hien_tai

    def _xay_danh_sach_tu_list(self, ds_nut):
        """Xay danh sach lien ket tu mot list cac node (reset con tro)."""
        if not ds_nut:
            return None
        for i, nut in enumerate(ds_nut):
            nut.truoc = None
            nut.sau = ds_nut[i + 1] if i + 1 < len(ds_nut) else None
        if len(ds_nut) > 1:
            ds_nut[-1].sau = None
        return ds_nut[0]

    def _noi_ba_phan(self, dau1, giua_list, pivot, dau2):
        """Noi 3 phan danh sach: nho + bang + pivot + lon."""
        # Tao linked list tu giua_list
        dau_giua = self._xay_danh_sach_tu_list(giua_list)

        # Reset pivot
        pivot.truoc = None
        pivot.sau = None

        # Tim cuoi cua phan 1
        cuoi1 = self._lay_node_cuoi(dau1) if dau1 else None
        # Tim dau cua phan 2
        dau3 = dau2

        # Noi: cuoi1 -> dau_giua -> pivot -> dau3
        def noi(a, b):
            if a is None:
                return b
            if b is None:
                return a
            cuoi_a = self._lay_node_cuoi(a)
            cuoi_a.sau = b
            b.truoc = cuoi_a
            return a

        ket_qua = noi(dau1, dau_giua)
        ket_qua = noi(ket_qua, pivot)
        ket_qua = noi(ket_qua, dau3)

        return ket_qua

    def _so_sanh(self, a, b, tieu_chi, tang_dan):
        """
        So sanh hai hang hoa theo tieu chi.

        Returns:
            bool: True neu a nen dung truoc b.
        """
        if tieu_chi == "gia_ban":
            val_a = a.tinh_gia_ban()
            val_b = b.tinh_gia_ban()
        elif tieu_chi == "so_luong":
            val_a = a.so_luong
            val_b = b.so_luong
        elif tieu_chi == "ten":
            val_a = a.ten_hang.lower()
            val_b = b.ten_hang.lower()
        elif tieu_chi == "ma_hang":
            val_a = a.ma_hang.lower()
            val_b = b.ma_hang.lower()
        else:
            val_a = a.tinh_gia_ban()
            val_b = b.tinh_gia_ban()

        if tang_dan:
            return val_a <= val_b
        else:
            return val_a >= val_b

    def sap_xep_theo_ma(self):
        """Sap xep danh sach theo ma hang (tang dan) - dung cho Binary Search."""
        self.sap_xep_merge(tieu_chi="ma_hang", tang_dan=True)

    # ─────────────────────────────────────────────
    # THONG KE (Statistics)
    # ─────────────────────────────────────────────

    def tong_so_luong(self):
        """Tra ve tong so luong node trong danh sach."""
        return self.so_luong_node

    def tong_so_luong_hang(self):
        """Tra ve tong so luong hang hoa (tong so_luong cua tat ca mat hang)."""
        tong = 0
        hien_tai = self.dau
        while hien_tai is not None:
            tong += hien_tai.du_lieu.so_luong
            hien_tai = hien_tai.sau
        return tong

    def hang_dat_nhat(self):
        """
        Tim hang hoa co gia ban cao nhat.

        Returns:
            HangHoa: Doi tuong hang hoa dat nhat, hoac None neu ds rong.
        """
        if self.la_rong():
            return None
        hien_tai = self.dau
        dat_nhat = hien_tai.du_lieu
        while hien_tai is not None:
            if hien_tai.du_lieu.tinh_gia_ban() > dat_nhat.tinh_gia_ban():
                dat_nhat = hien_tai.du_lieu
            hien_tai = hien_tai.sau
        return dat_nhat

    def hang_re_nhat(self):
        """
        Tim hang hoa co gia ban thap nhat.

        Returns:
            HangHoa: Doi tuong hang hoa re nhat, hoac None neu ds rong.
        """
        if self.la_rong():
            return None
        hien_tai = self.dau
        re_nhat = hien_tai.du_lieu
        while hien_tai is not None:
            if hien_tai.du_lieu.tinh_gia_ban() < re_nhat.tinh_gia_ban():
                re_nhat = hien_tai.du_lieu
            hien_tai = hien_tai.sau
        return re_nhat

    def danh_sach_sap_het(self):
        """
        Tim tat ca hang hoa sap het (so luong < 5).

        Returns:
            DanhSachLienKet: Danh sach cac hang sap het.
        """
        ket_qua = DanhSachLienKet()
        hien_tai = self.dau
        while hien_tai is not None:
            if hien_tai.du_lieu.kiem_tra_ton_kho():
                ket_qua.them_vao_cuoi_khong_kiem_tra_trung(hien_tai.du_lieu)
            hien_tai = hien_tai.sau
        return ket_qua

    def danh_sach_het_han(self):
        """
        Tim tat ca thuc pham sap het han hoac da het han.

        Returns:
            DanhSachLienKet: Danh sach cac thuc pham het han.
        """
        ket_qua = DanhSachLienKet()
        hien_tai = self.dau
        while hien_tai is not None:
            hh = hien_tai.du_lieu
            if hh.loai_hang() == "ThucPham" and hh.kiem_tra_het_han():
                ket_qua.them_vao_cuoi_khong_kiem_tra_trung(hh)
            hien_tai = hien_tai.sau
        return ket_qua

    # ─────────────────────────────────────────────
    # LUU / DOC DU LIEU (File I/O)
    # ─────────────────────────────────────────────

    def luu_vao_file(self, duong_dan):
        """
        Luu toan bo danh sach vao file JSON.

        Args:
            duong_dan (str): Duong dan den file JSON.

        Raises:
            LoiFile: Neu khong the ghi file.
        """
        try:
            # Dam bao thu muc ton tai
            thu_muc = os.path.dirname(duong_dan)
            if thu_muc and not os.path.exists(thu_muc):
                os.makedirs(thu_muc)

            ds_dict = []
            hien_tai = self.dau
            while hien_tai is not None:
                ds_dict.append(hien_tai.du_lieu.to_dict())
                hien_tai = hien_tai.sau

            with open(duong_dan, "w", encoding="utf-8") as f:
                json.dump(ds_dict, f, ensure_ascii=False, indent=4)

        except (IOError, OSError) as e:
            raise LoiFile(duong_dan, str(e))

    def doc_tu_file(self, duong_dan):
        """
        Doc du lieu tu file JSON vao danh sach.

        Args:
            duong_dan (str): Duong dan den file JSON.

        Raises:
            LoiFile: Neu khong the doc file hoac file sai dinh dang.
        """
        if not os.path.exists(duong_dan):
            raise LoiFile(duong_dan, "File khong ton tai!")

        try:
            with open(duong_dan, "r", encoding="utf-8") as f:
                ds_dict = json.load(f)
        except json.JSONDecodeError as e:
            raise LoiFile(duong_dan, f"File JSON bi huong: {str(e)}")
        except IOError as e:
            raise LoiFile(duong_dan, str(e))

        # Xoa danh sach cu va nap du lieu moi
        self.xoa_toan_bo()

        try:
            for item in ds_dict:
                hang_hoa = tao_hang_hoa_tu_dict(item)
                self.them_vao_cuoi_khong_kiem_tra_trung(hang_hoa)
        except (KeyError, ValueError) as e:
            raise LoiFile(duong_dan, f"Du lieu khong hop le: {str(e)}")

    # ─────────────────────────────────────────────
    # CAC PHUONG THUC BO TRO
    # ─────────────────────────────────────────────

    def chuyen_sang_list(self):
        """Chuyen danh sach lien ket thanh Python list (de tien xu ly)."""
        ket_qua = []
        hien_tai = self.dau
        while hien_tai is not None:
            ket_qua.append(hien_tai.du_lieu)
            hien_tai = hien_tai.sau
        return ket_qua

    def duyet_nguoc(self):
        """Duyet danh sach tu cuoi ve dau (tra ve list)."""
        ket_qua = []
        hien_tai = self.cuoi
        while hien_tai is not None:
            ket_qua.append(hien_tai.du_lieu)
            hien_tai = hien_tai.truoc
        return ket_qua

    def __iter__(self):
        """Cho phep duyet danh sach bang for-loop."""
        hien_tai = self.dau
        while hien_tai is not None:
            yield hien_tai.du_lieu
            hien_tai = hien_tai.sau

    def __len__(self):
        """Tra ve so luong phan tu."""
        return self.so_luong_node

    def __str__(self):
        """Hien thi thong tin danh sach."""
        if self.la_rong():
            return "Danh sach rong."
        lines = [f"Danh sach ({self.so_luong_node} mat hang):"]
        hien_tai = self.dau
        stt = 1
        while hien_tai is not None:
            lines.append(f"  {stt}. {hien_tai.du_lieu.thong_tin_tom_tat()}")
            stt += 1
            hien_tai = hien_tai.sau
        return "\n".join(lines)