"""
giao_dien.py - Giao dien chinh ung dung Quan Ly Sieu Thi (PyQt6)

Gom:
  - Sidebar ben trai (cac chuc nang)
  - Bang du lieu (QTreeWidget) hien thi danh sach hang hoa
  - Form nhap lieu dong (thay doi theo loai hang)
  - Tim kiem nang cao
  - Thong ke
  - Canh bao hang het han / sap het hang
"""

import sys
import os

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit,
    QPushButton, QComboBox, QGroupBox, QFormLayout,
    QFileDialog, QMessageBox, QHeaderView, QDateEdit,
    QAbstractItemView, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont

# Import tu project
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.danh_sach_lien_ket import DanhSachLienKet
from core.mo_hinh import HangHoa, ThucPham, DienMay, HangGiaDung
from core.ngoai_le import LoiTrungMa, LoiFile, LoiNhapLieu


class GiaoDienChinh(QMainWindow):
    """Lop giao dien chinh cua ung dung Quan Ly Sieu Thi."""

    def __init__(self):
        super().__init__()
        self.danh_sach = DanhSachLienKet()
        self.duong_dan_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "du_lieu.json"
        )
        self.dang_sua = False
        self.ma_dang_sua = None

        self.cai_dat_cua_so()
        self.tao_giao_dien()
        self.tai_du_lieu()

    def cai_dat_cua_so(self):
        """Cai dat thong tin cua so chinh."""
        self.setWindowTitle("He Thong Quan Ly Hang Hoa Sieu Thi")
        self.setMinimumSize(1200, 700)
        self.resize(1300, 750)

    def tao_giao_dien(self):
        """Tao toan bo giao dien: sidebar + content."""
        widget_chinh = QWidget()
        self.setCentralWidget(widget_chinh)

        layout_chinh = QHBoxLayout(widget_chinh)
        layout_chinh.setContentsMargins(0, 0, 0, 0)
        layout_chinh.setSpacing(0)

        # ── Sidebar ──
        sidebar = self.tao_sidebar()
        layout_chinh.addWidget(sidebar)

        # ── Content area ──
        content = self.tao_content_area()
        layout_chinh.addWidget(content, stretch=1)

        # ── Ap dung stylesheet ──
        duong_dan_qss = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dinh_dang.qss"
        )
        if os.path.exists(duong_dan_qss):
            with open(duong_dan_qss, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    # ─────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────

    def tao_sidebar(self):
        """Tao panel ben trai voi cac nut chuc nang."""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(5, 15, 5, 15)
        layout.setSpacing(5)

        # Tieu de
        lbl_tieu_de = QLabel("SIÊU THỊ")
        lbl_tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_tieu_de)

        lbl_phu = QLabel("Quản Lý Hàng Hóa")
        lbl_phu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_phu.setStyleSheet("color: #9fa8da; font-size: 12px;")
        layout.addWidget(lbl_phu)

        layout.addSpacing(20)

        # Cac nut chuc nang
        self.btn_tat_ca = QPushButton("📋  Tất Cả Hàng Hóa")
        self.btn_tat_ca.setObjectName("btn_active")
        self.btn_tat_ca.clicked.connect(lambda: self.chuyen_trang("tat_ca"))
        layout.addWidget(self.btn_tat_ca)

        self.btn_them = QPushButton("➕  Thêm Hàng Mới")
        self.btn_them.clicked.connect(lambda: self.chuyen_trang("them"))
        layout.addWidget(self.btn_them)

        self.btn_tim_kiem = QPushButton("🔍  Tìm Kiếm")
        self.btn_tim_kiem.clicked.connect(lambda: self.chuyen_trang("tim_kiem"))
        layout.addWidget(self.btn_tim_kiem)

        self.btn_sap_xep = QPushButton("📊  Sắp Xếp")
        self.btn_sap_xep.clicked.connect(lambda: self.chuyen_trang("sap_xep"))
        layout.addWidget(self.btn_sap_xep)

        self.btn_thong_ke = QPushButton("📈  Thống Kê")
        self.btn_thong_ke.clicked.connect(lambda: self.chuyen_trang("thong_ke"))
        layout.addWidget(self.btn_thong_ke)

        layout.addSpacing(20)

        # Nut luu
        self.btn_luu_file = QPushButton("💾  Lưu Dữ Liệu")
        self.btn_luu_file.setObjectName("btn_luu")
        self.btn_luu_file.clicked.connect(self.luu_du_lieu)
        layout.addWidget(self.btn_luu_file)

        layout.addStretch()

        # Thong tin
        lbl_ver = QLabel("v1.0 - OOP Project")
        lbl_ver.setStyleSheet("color: #5c6bc0; font-size: 11px;")
        lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_ver)

        # Luu cac nut sidebar de doi mau active
        self.cac_nut_sidebar = [
            self.btn_tat_ca, self.btn_them, self.btn_tim_kiem,
            self.btn_sap_xep, self.btn_thong_ke
        ]

        return sidebar

    # ─────────────────────────────────────────
    # CONTENT AREA
    # ─────────────────────────────────────────

    def tao_content_area(self):
        """Tao vung noi dung chinh (trai + phai)."""
        content = QWidget()
        self.content_layout = QHBoxLayout(content)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)

        # ── Panel trai: Bang + Bo loc ──
        panel_trai = QWidget()
        layout_trai = QVBoxLayout(panel_trai)
        layout_trai.setContentsMargins(0, 0, 0, 0)

        # Tieu de + Bo loc
        header_layout = QHBoxLayout()

        lbl_tieu_de = QLabel("Danh Sách Hàng Hóa")
        lbl_tieu_de.setObjectName("tieu_de")
        header_layout.addWidget(lbl_tieu_de)

        header_layout.addStretch()

        lbl_loc = QLabel("Lọc:")
        header_layout.addWidget(lbl_loc)

        self.combo_loc = QComboBox()
        self.combo_loc.addItems(["Tất cả", "ThucPham", "DienMay", "HangGiaDung"])
        self.combo_loc.setFixedWidth(140)
        self.combo_loc.currentTextChanged.connect(self.loc_danh_sach)
        header_layout.addWidget(self.combo_loc)

        layout_trai.addLayout(header_layout)

        # Bang du lieu
        self.bang = QTreeWidget()
        self.bang.setHeaderLabels([
            "STT", "Mã Hàng", "Tên Hàng", "Loại",
            "Số Lượng", "Giá Nhập", "Giá Bán", "Thông Tin Riêng"
        ])
        self.bang.setAlternatingRowColors(True)
        self.bang.setRootIsDecorated(False)
        self.bang.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.bang.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.bang.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Cai dat do rong cot
        header = self.bang.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.bang.setColumnWidth(0, 50)
        self.bang.setColumnWidth(1, 100)
        self.bang.setColumnWidth(2, 180)
        self.bang.setColumnWidth(3, 100)
        self.bang.setColumnWidth(4, 80)
        self.bang.setColumnWidth(5, 100)
        self.bang.setColumnWidth(6, 100)
        self.bang.setColumnWidth(7, 200)

        # Double click de sua
        self.bang.itemDoubleClicked.connect(self.double_click_sua)

        layout_trai.addWidget(self.bang)

        # Nut hanh dong ben duoi bang
        btn_layout = QHBoxLayout()

        self.btn_sua_select = QPushButton("✏️  Sửa Hàng Đã Chọn")
        self.btn_sua_select.setObjectName("btn_sua")
        self.btn_sua_select.clicked.connect(self.sua_hang_bang_click)
        btn_layout.addWidget(self.btn_sua_select)

        self.btn_xoa_select = QPushButton("🗑️  Xóa Hàng Đã Chọn")
        self.btn_xoa_select.setObjectName("btn_xoa")
        self.btn_xoa_select.clicked.connect(self.xoa_hang_bang_click)
        btn_layout.addWidget(self.btn_xoa_select)

        btn_layout.addStretch()
        layout_trai.addLayout(btn_layout)

        self.content_layout.addWidget(panel_trai, stretch=3)

        # ── Panel phai: Form / Tim kiem / Thong ke ──
        self.panel_phai = QWidget()
        self.panel_phai_layout = QVBoxLayout(self.panel_phai)
        self.panel_phai_layout.setContentsMargins(0, 0, 0, 0)

        # Mac dinh hien thi form them moi
        self.stack_widgets = {}
        self.tao_form_nhap_lieu()
        self.tao_form_tim_kiem()
        self.tao_form_sap_xep()
        self.tao_form_thong_ke()

        self.hien_thi_panel("form_nhap_lieu")

        self.content_layout.addWidget(self.panel_phai, stretch=2)

        return content

    # ─────────────────────────────────────────
    # FORM NHAP LIEU
    # ─────────────────────────────────────────

    def tao_form_nhap_lieu(self):
        """Tao form nhap lieu hang hoa (them moi / sua)."""
        form = QWidget()
        layout = QVBoxLayout(form)

        self.lbl_form_tieu_de = QLabel("THÊM HÀNG MỚI")
        self.lbl_form_tieu_de.setObjectName("tieu_de")
        layout.addWidget(self.lbl_form_tieu_de)

        # ── Thong tin chung ──
        grp_chung = QGroupBox("Thông Tin Chung")
        form_chung = QFormLayout(grp_chung)

        self.input_ma = QLineEdit()
        self.input_ma.setPlaceholderText("VD: TP001")
        form_chung.addRow("Mã hàng:", self.input_ma)

        self.input_ten = QLineEdit()
        self.input_ten.setPlaceholderText("VD: Sữa tươi Vinamilk")
        form_chung.addRow("Tên hàng:", self.input_ten)

        self.input_so_luong = QSpinBox()
        self.input_so_luong.setRange(0, 99999)
        self.input_so_luong.setValue(0)
        form_chung.addRow("Số lượng:", self.input_so_luong)

        self.input_gia_nhap = QDoubleSpinBox()
        self.input_gia_nhap.setRange(0, 999999999)
        self.input_gia_nhap.setDecimals(0)
        self.input_gia_nhap.setValue(0)
        self.input_gia_nhap.setPrefix("")
        self.input_gia_nhap.setSuffix(" VND")
        form_chung.addRow("Giá nhập:", self.input_gia_nhap)

        self.combo_loai = QComboBox()
        self.combo_loai.addItems(["ThucPham", "DienMay", "HangGiaDung"])
        self.combo_loai.currentTextChanged.connect(self.thay_doi_form_theo_loai)
        form_chung.addRow("Loại hàng:", self.combo_loai)

        layout.addWidget(grp_chung)

        # ── Thong tin rieng theo loai ──
        # Nhom Thuc Pham
        self.grp_thuc_pham = QGroupBox("Thông Tin Thực Phẩm")
        form_tp = QFormLayout(self.grp_thuc_pham)

        self.input_nsx = QDateEdit()
        self.input_nsx.setCalendarPopup(True)
        self.input_nsx.setDate(QDate.currentDate())
        self.input_nsx.setDisplayFormat("yyyy-MM-dd")
        form_tp.addRow("Ngày sản xuất:", self.input_nsx)

        self.input_hsd = QDateEdit()
        self.input_hsd.setCalendarPopup(True)
        self.input_hsd.setDate(QDate.currentDate().addMonths(6))
        self.input_hsd.setDisplayFormat("yyyy-MM-dd")
        form_tp.addRow("Ngày hết hạn:", self.input_hsd)

        layout.addWidget(self.grp_thuc_pham)

        # Nhom Dien May
        self.grp_dien_may = QGroupBox("Thông Tin Điện Máy")
        form_dm = QFormLayout(self.grp_dien_may)

        self.input_bao_hanh = QSpinBox()
        self.input_bao_hanh.setRange(0, 120)
        self.input_bao_hanh.setValue(12)
        self.input_bao_hanh.setSuffix(" tháng")
        form_dm.addRow("Bảo hành:", self.input_bao_hanh)

        self.input_cong_suat = QLineEdit()
        self.input_cong_suat.setPlaceholderText("VD: 150W")
        form_dm.addRow("Công suất:", self.input_cong_suat)

        layout.addWidget(self.grp_dien_may)

        # Nhom Hang Gia Dung
        self.grp_gia_dung = QGroupBox("Thông Tin Hàng Gia Dụng")
        form_gd = QFormLayout(self.grp_gia_dung)

        self.combo_chat_lieu = QComboBox()
        self.combo_chat_lieu.addItems(["Nhựa", "Gỗ", "Thép", "Kính", "Khác"])
        form_gd.addRow("Chất liệu:", self.combo_chat_lieu)

        layout.addWidget(self.grp_gia_dung)

        # ── Nut bam ──
        btn_layout = QHBoxLayout()

        self.btn_them_hang = QPushButton("➕  Thêm Hàng")
        self.btn_them_hang.setObjectName("btn_them")
        self.btn_them_hang.clicked.connect(self.them_hang)
        btn_layout.addWidget(self.btn_them_hang)

        self.btn_huy = QPushButton("🔄  Làm Mới")
        self.btn_huy.setObjectName("btn_khac")
        self.btn_huy.clicked.connect(self.lam_moi_form)
        btn_layout.addWidget(self.btn_huy)

        layout.addLayout(btn_layout)

        # Mac dinh hien thi thuc pham
        self.thay_doi_form_theo_loai("ThucPham")

        self.stack_widgets["form_nhap_lieu"] = form

    def thay_doi_form_theo_loai(self, loai):
        """Hien / an cac truong nhap lieu tuy theo loai hang."""
        self.grp_thuc_pham.setVisible(loai == "ThucPham")
        self.grp_dien_may.setVisible(loai == "DienMay")
        self.grp_gia_dung.setVisible(loai == "HangGiaDung")

    # ─────────────────────────────────────────
    # FORM TIM KIEM
    # ─────────────────────────────────────────

    def tao_form_tim_kiem(self):
        """Tao form tim kiem nang cao."""
        form = QWidget()
        layout = QVBoxLayout(form)

        lbl_tieu_de = QLabel("TÌM KIẾM NĂNG CAO")
        lbl_tieu_de.setObjectName("tieu_de")
        layout.addWidget(lbl_tieu_de)

        # Tim theo ma
        grp_ma = QGroupBox("Tìm Theo Mã Hàng (Binary Search)")
        form_ma = QVBoxLayout(grp_ma)
        self.input_tim_ma = QLineEdit()
        self.input_tim_ma.setPlaceholderText("Nhập mã hàng cần tìm...")
        form_ma.addWidget(self.input_tim_ma)
        self.btn_tim_ma = QPushButton("🔍  Tìm Kiếm (Binary Search)")
        self.btn_tim_ma.setObjectName("btn_sua")
        self.btn_tim_ma.clicked.connect(self.tim_kiem_theo_ma)
        form_ma.addWidget(self.btn_tim_ma)
        layout.addWidget(grp_ma)

        # Tim theo ten
        grp_ten = QGroupBox("Tìm Theo Tên Hàng (Linear Search)")
        form_ten = QVBoxLayout(grp_ten)
        self.input_tim_ten = QLineEdit()
        self.input_tim_ten.setPlaceholderText("Nhập tên hoặc từ khóa...")
        form_ten.addWidget(self.input_tim_ten)
        self.btn_tim_ten = QPushButton("🔍  Tìm Kiếm (Linear Search)")
        self.btn_tim_ten.setObjectName("btn_sua")
        self.btn_tim_ten.clicked.connect(self.tim_kiem_theo_ten)
        form_ten.addWidget(self.btn_tim_ten)
        layout.addWidget(grp_ten)

        # Ket qua tim kiem
        grp_kq = QGroupBox("Kết Quả")
        form_kq = QVBoxLayout(grp_kq)
        self.lbl_ket_qua = QLabel("Nhập thông tin để tìm kiếm.")
        self.lbl_ket_qua.setWordWrap(True)
        self.lbl_ket_qua.setStyleSheet("font-size: 13px; padding: 10px;")
        form_kq.addWidget(self.lbl_ket_qua)
        layout.addWidget(grp_kq)

        layout.addStretch()

        self.stack_widgets["form_tim_kiem"] = form

    # ─────────────────────────────────────────
    # FORM SAP XEP
    # ─────────────────────────────────────────

    def tao_form_sap_xep(self):
        """Tao form sap xep hang hoa."""
        form = QWidget()
        layout = QVBoxLayout(form)

        lbl_tieu_de = QLabel("SẮP XẾP HÀNG HÓA")
        lbl_tieu_de.setObjectName("tieu_de")
        layout.addWidget(lbl_tieu_de)

        # Chon tieu chi
        grp_tc = QGroupBox("Tiêu Chí Sắp Xếp")
        form_tc = QFormLayout(grp_tc)

        self.combo_tieu_chi = QComboBox()
        self.combo_tieu_chi.addItems([
            "Giá bán", "Số lượng tồn kho", "Tên hàng", "Mã hàng"
        ])
        form_tc.addRow("Sắp xếp theo:", self.combo_tieu_chi)

        self.combo_thu_tu = QComboBox()
        self.combo_thu_tu.addItems(["Tăng dần", "Giảm dần"])
        form_tc.addRow("Thứ tự:", self.combo_thu_tu)

        layout.addWidget(grp_tc)

        # Chon thuat toan
        grp_al = QGroupBox("Thuật Toán")
        form_al = QVBoxLayout(grp_al)

        self.btn_merge_sort = QPushButton("🔀  Merge Sort")
        self.btn_merge_sort.setObjectName("btn_sua")
        self.btn_merge_sort.clicked.connect(self.sap_xep_merge)
        form_al.addWidget(self.btn_merge_sort)

        self.btn_quick_sort = QPushButton("⚡  Quick Sort")
        self.btn_quick_sort.setObjectName("btn_sua")
        self.btn_quick_sort.clicked.connect(self.sap_xep_quick)
        form_al.addWidget(self.btn_quick_sort)

        layout.addWidget(grp_al)

        layout.addStretch()

        self.stack_widgets["form_sap_xep"] = form

    # ─────────────────────────────────────────
    # FORM THONG KE
    # ─────────────────────────────────────────

    def tao_form_thong_ke(self):
        """Tao form thong ke."""
        form = QWidget()
        layout = QVBoxLayout(form)

        lbl_tieu_de = QLabel("THỐNG KÊ")
        lbl_tieu_de.setObjectName("tieu_de")
        layout.addWidget(lbl_tieu_de)

        # Tong quan
        grp_tq = QGroupBox("Tổng Quan")
        form_tq = QVBoxLayout(grp_tq)

        self.lbl_tong_mat_hang = QLabel("0")
        self.lbl_tong_mat_hang.setObjectName("thong_ke_so")
        lbl1 = QLabel("Mặt hàng")
        lbl1.setObjectName("thong_ke_nhan")
        form_tq.addWidget(self.lbl_tong_mat_hang)
        form_tq.addWidget(lbl1)

        form_tq.addSpacing(10)

        self.lbl_tong_so_luong = QLabel("0")
        self.lbl_tong_so_luong.setObjectName("thong_ke_so")
        lbl2 = QLabel("Tổng số lượng hàng")
        lbl2.setObjectName("thong_ke_nhan")
        form_tq.addWidget(self.lbl_tong_so_luong)
        form_tq.addWidget(lbl2)

        layout.addWidget(grp_tq)

        # Gia tri
        grp_gia = QGroupBox("Giá Trị")
        form_gia = QFormLayout(grp_gia)

        self.lbl_dat_nhat = QLabel("-")
        self.lbl_dat_nhat.setWordWrap(True)
        self.lbl_dat_nhat.setStyleSheet("color: #c62828; font-weight: bold;")
        form_gia.addRow("Hàng đắt nhất:", self.lbl_dat_nhat)

        self.lbl_re_nhat = QLabel("-")
        self.lbl_re_nhat.setWordWrap(True)
        self.lbl_re_nhat.setStyleSheet("color: #2e7d32; font-weight: bold;")
        form_gia.addRow("Hàng rẻ nhất:", self.lbl_re_nhat)

        layout.addWidget(grp_gia)

        # Canh bao
        grp_cw = QGroupBox("Cảnh Báo")
        form_cw = QVBoxLayout(grp_cw)

        self.lbl_canh_bao = QLabel("")
        self.lbl_canh_bao.setWordWrap(True)
        self.lbl_canh_bao.setObjectName("canh_bao")
        form_cw.addWidget(self.lbl_canh_bao)

        self.btn_xem_bao_hanh = QPushButton("📄  Xuất Tém Bảo Hành")
        self.btn_xem_bao_hanh.setObjectName("btn_khac")
        self.btn_xem_bao_hanh.clicked.connect(self.xuat_tem_bao_hanh)
        self.btn_xem_bao_hanh.setVisible(False)
        form_cw.addWidget(self.btn_xem_bao_hanh)

        layout.addWidget(grp_cw)

        layout.addStretch()

        self.stack_widgets["form_thong_ke"] = form

    # ─────────────────────────────────────────
    # CAP NHAT GIAO DIEN
    # ─────────────────────────────────────────

    def hien_thi_panel(self, ten_panel):
        """Chuyen doi panel phai (form nhap lieu / tim kiem / sap xep / thong ke)."""
        # Xoa widget hien tai
        while self.panel_phai_layout.count():
            item = self.panel_phai_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.setVisible(False)

        # Hien thi widget moi
        if ten_panel in self.stack_widgets:
            w = self.stack_widgets[ten_panel]
            w.setParent(self.panel_phai)
            w.setVisible(True)
            self.panel_phai_layout.addWidget(w)

    def doi_mau_sidebar(self, btn_active):
        """Doi mau nut sidebar dang active."""
        for btn in self.cac_nut_sidebar:
            btn.setObjectName("")
        btn_active.setObjectName("btn_active")
        # Force re-style
        btn_active.style().unpolish(btn_active)
        btn_active.style().polish(btn_active)

    def chuyen_trang(self, trang):
        """Xu ly chuyen trang tu sidebar."""
        if trang == "tat_ca":
            self.hien_thi_panel("form_nhap_lieu")
            self.lbl_form_tieu_de.setText("THÊM HÀNG MỚI")
            self.btn_them_hang.setText("➕  Thêm Hàng")
            self.lam_moi_form()
            self.dang_sua = False
            self.doi_mau_sidebar(self.btn_tat_ca)
            self.cap_nhat_bang()

        elif trang == "them":
            self.hien_thi_panel("form_nhap_lieu")
            self.lbl_form_tieu_de.setText("THÊM HÀNG MỚI")
            self.btn_them_hang.setText("➕  Thêm Hàng")
            self.lam_moi_form()
            self.dang_sua = False
            self.doi_mau_sidebar(self.btn_them)

        elif trang == "tim_kiem":
            self.hien_thi_panel("form_tim_kiem")
            self.lbl_ket_qua.setText("Nhập thông tin để tìm kiếm.")
            self.doi_mau_sidebar(self.btn_tim_kiem)

        elif trang == "sap_xep":
            self.hien_thi_panel("form_sap_xep")
            self.doi_mau_sidebar(self.btn_sap_xep)

        elif trang == "thong_ke":
            self.hien_thi_panel("form_thong_ke")
            self.cap_nhat_thong_ke()
            self.doi_mau_sidebar(self.btn_thong_ke)

    # ─────────────────────────────────────────
    # CAP NHAT BANG DU LIEU
    # ─────────────────────────────────────────

    def cap_nhat_bang(self, danh_sach_hien=None):
        """Cap nhat noi dung bang tu danh sach lien ket."""
        self.bang.clear()
        if danh_sach_hien is None:
            danh_sach_hien = self.danh_sach

        stt = 1
        for hang in danh_sach_hien:
            thong_tin_rieng = self._lay_thong_tin_rieng(hang)

            item = QTreeWidgetItem([
                str(stt),
                hang.ma_hang,
                hang.ten_hang,
                hang.loai_hang(),
                str(hang.so_luong),
                f"{hang.gia_nhap:,.0f}",
                f"{hang.tinh_gia_ban():,.0f}",
                thong_tin_rieng
            ])

            # To mau do cho hang sap het hoac het han
            canh_bao = False
            if hang.kiem_tra_ton_kho():
                canh_bao = True
            if hang.loai_hang() == "ThucPham" and hang.kiem_tra_het_han():
                canh_bao = True

            if canh_bao:
                for col in range(self.bang.columnCount()):
                    item.setForeground(col, QColor("#c62828"))
                    item.setBackground(col, QColor("#ffebee"))

            self.bang.addTopLevelItem(item)
            stt += 1

    def _lay_thong_tin_rieng(self, hang):
        """Lay thong tin rieng cua tung loai hang de hien thi trong bang."""
        if hang.loai_hang() == "ThucPham":
            con_lai = hang.so_ngay_con_lai()
            if con_lai < 0:
                return f"Đã hết hạn | HSD: {hang.ngay_het_han}"
            elif con_lai <= 7:
                return f"Còn {con_lai} ngày | HSD: {hang.ngay_het_han}"
            else:
                return f"HSD: {hang.ngay_het_han}"
        elif hang.loai_hang() == "DienMay":
            return f"Bảo hành: {hang.thoi_gian_bao_hanh}T | {hang.cong_suat}"
        elif hang.loai_hang() == "HangGiaDung":
            return f"Chất liệu: {hang.chat_lieu}"
        return ""

    # ─────────────────────────────────────────
    # THEM HANG HOA
    # ─────────────────────────────────────────

    def them_hang(self):
        """Xu ly them hang hoa moi tu form."""
        try:
            ma = self.input_ma.text().strip()
            ten = self.input_ten.text().strip()
            so_luong = self.input_so_luong.value()
            gia_nhap = self.input_gia_nhap.value()
            loai = self.combo_loai.currentText()

            # Kiem tra du lieu hop le
            if not ma:
                raise LoiNhapLieu("Mã hàng", "Không được để trống")
            if not ten:
                raise LoiNhapLieu("Tên hàng", "Không được để trống")
            if gia_nhap < 0:
                raise LoiNhapLieu("Giá nhập", "Giá không được âm")
            if so_luong < 0:
                raise LoiNhapLieu("Số lượng", "Số lượng không được âm")

            # Tao doi tuong hang hoa theo loai
            if loai == "ThucPham":
                nsx = self.input_nsx.date().toString("yyyy-MM-dd")
                hsd = self.input_hsd.date().toString("yyyy-MM-dd")
                hang = ThucPham(ma, ten, so_luong, gia_nhap, nsx, hsd)
            elif loai == "DienMay":
                bh = self.input_bao_hanh.value()
                cs = self.input_cong_suat.text().strip()
                if not cs:
                    raise LoiNhapLieu("Công suất", "Không được để trống")
                hang = DienMay(ma, ten, so_luong, gia_nhap, bh, cs)
            elif loai == "HangGiaDung":
                cl = self.combo_chat_lieu.currentText()
                hang = HangGiaDung(ma, ten, so_luong, gia_nhap, cl)
            else:
                raise LoiNhapLieu("Loại hàng", "Loại không hợp lệ")

            # Kiem tra trung ma
            if self.danh_sach.tim_theo_ma(ma) is not None:
                raise LoiTrungMa(ma)

            # Them vao danh sach
            self.danh_sach.them_vao_cuoi(hang)
            self.cap_nhat_bang()
            self.lam_moi_form()
            self.luu_du_lieu_tu_dong()

            QMessageBox.information(
                self, "Thành Công",
                f"Đã thêm hàng hóa '{ten}' thành công!"
            )

        except LoiTrungMa as e:
            QMessageBox.warning(self, "Lỗi Trùng Mã", str(e))
        except LoiNhapLieu as e:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", str(e))
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi Dữ Liệu", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    # ─────────────────────────────────────────
    # SUA HANG HOA
    # ─────────────────────────────────────────

    def sua_hang_bang_click(self):
        """Sua hang hoa khi nhan nut 'Sua' ben duoi bang."""
        item = self.bang.currentItem()
        if item is None:
            QMessageBox.warning(self, "Chưa Chọn", "Vui lòng chọn một hàng hóa để sửa!")
            return

        ma_hang = item.text(1)
        hang = self.danh_sach.tim_theo_ma(ma_hang)
        if hang is None:
            return

        # Chuyen sang form nhap lieu va dien du lieu
        self.chuyen_trang("them")
        self.lbl_form_tieu_de.setText(f"SỬA HÀNG: {hang.ten_hang}")
        self.btn_them_hang.setText("✅  Cập Nhật")

        self.dang_sua = True
        self.ma_dang_sua = ma_hang

        # Dien du lieu vao form
        self.input_ma.setText(hang.ma_hang)
        self.input_ma.setEnabled(False)  # Khong cho sua ma
        self.input_ten.setText(hang.ten_hang)
        self.input_so_luong.setValue(hang.so_luong)
        self.input_gia_nhap.setValue(hang.gia_nhap)
        self.combo_loai.setCurrentText(hang.loai_hang())

        if hang.loai_hang() == "ThucPham":
            nsx = QDate.fromString(hang.ngay_san_xuat, "yyyy-MM-dd")
            hsd = QDate.fromString(hang.ngay_het_han, "yyyy-MM-dd")
            self.input_nsx.setDate(nsx)
            self.input_hsd.setDate(hsd)
        elif hang.loai_hang() == "DienMay":
            self.input_bao_hanh.setValue(hang.thoi_gian_bao_hanh)
            self.input_cong_suat.setText(hang.cong_suat)
        elif hang.loai_hang() == "HangGiaDung":
            idx = self.combo_chat_lieu.findText(hang.chat_lieu)
            if idx >= 0:
                self.combo_chat_lieu.setCurrentIndex(idx)

        # Thay doi hanh vi nut them thanh cap nhat
        self.btn_them_hang.disconnect()
        self.btn_them_hang.clicked.connect(self.cap_nhat_hang)

    def cap_nhat_hang(self):
        """Cap nhat hang hoa (khi dang sua)."""
        try:
            ten = self.input_ten.text().strip()
            so_luong = self.input_so_luong.value()
            gia_nhap = self.input_gia_nhap.value()
            loai = self.combo_loai.currentText()

            if not ten:
                raise LoiNhapLieu("Tên hàng", "Không được để trống")
            if gia_nhap < 0:
                raise LoiNhapLieu("Giá nhập", "Giá không được âm")
            if so_luong < 0:
                raise LoiNhapLieu("Số lượng", "Số lượng không được âm")

            ma = self.ma_dang_sua

            if loai == "ThucPham":
                nsx = self.input_nsx.date().toString("yyyy-MM-dd")
                hsd = self.input_hsd.date().toString("yyyy-MM-dd")
                hang_moi = ThucPham(ma, ten, so_luong, gia_nhap, nsx, hsd)
            elif loai == "DienMay":
                bh = self.input_bao_hanh.value()
                cs = self.input_cong_suat.text().strip()
                if not cs:
                    raise LoiNhapLieu("Công suất", "Không được để trống")
                hang_moi = DienMay(ma, ten, so_luong, gia_nhap, bh, cs)
            elif loai == "HangGiaDung":
                cl = self.combo_chat_lieu.currentText()
                hang_moi = HangGiaDung(ma, ten, so_luong, gia_nhap, cl)
            else:
                raise LoiNhapLieu("Loại hàng", "Loại không hợp lệ")

            self.danh_sach.sua_theo_ma(ma, hang_moi)
            self.cap_nhat_bang()
            self.lam_moi_form()
            self.luu_du_lieu_tu_dong()

            # Khoi phuc hanh vi nut
            self.btn_them_hang.disconnect()
            self.btn_them_hang.clicked.connect(self.them_hang)
            self.dang_sua = False
            self.input_ma.setEnabled(True)

            QMessageBox.information(self, "Thành Công", f"Đã cập nhật hàng '{ten}'!")

        except LoiNhapLieu as e:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def double_click_sua(self, item, col):
        """Xu ly double click tren bang de sua."""
        self.sua_hang_bang_click()

    # ─────────────────────────────────────────
    # XOA HANG HOA
    # ─────────────────────────────────────────

    def xoa_hang_bang_click(self):
        """Xoa hang hoa khi nhan nut 'Xoa' ben duoi bang."""
        item = self.bang.currentItem()
        if item is None:
            QMessageBox.warning(self, "Chưa Chọn", "Vui lòng chọn một hàng hóa để xóa!")
            return

        ma_hang = item.text(1)
        ten_hang = item.text(2)

        tra_loi = QMessageBox.question(
            self, "Xác Nhận Xóa",
            f"Bạn có chắc muốn xóa hàng hóa '{ten_hang}' (Mã: {ma_hang})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if tra_loi == QMessageBox.StandardButton.Yes:
            try:
                self.danh_sach.xoa_theo_ma(ma_hang)
                self.cap_nhat_bang()
                self.luu_du_lieu_tu_dong()
                QMessageBox.information(self, "Thành Công", "Đã xóa hàng hóa thành công!")
            except ValueError as e:
                QMessageBox.warning(self, "Lỗi", str(e))

    # ─────────────────────────────────────────
    # TIM KIEM
    # ─────────────────────────────────────────

    def tim_kiem_theo_ma(self):
        """Tim kiem hang hoa theo ma (su dung Binary Search)."""
        ma = self.input_tim_ma.text().strip()
        if not ma:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã hàng cần tìm!")
            return

        # Sap xep theo ma truoc khi binary search
        self.danh_sach.sap_xep_theo_ma()
        ket_qua = self.danh_sach.tim_kiem_nhi_phan(ma)

        if ket_qua:
            self.lbl_ket_qua.setText(
                f"✅ TÌM THẤY (Binary Search):\n\n"
                f"{ket_qua.thong_tin_tom_tat()}\n\n"
                f"Loại: {ket_qua.loai_hang()}\n"
                f"Giá nhập: {ket_qua.gia_nhap:,.0f} VND\n"
                f"Giá bán: {ket_qua.tinh_gia_ban():,.0f} VND"
            )
            # Highlight tren bang
            self.cap_nhat_bang()
            for i in range(self.bang.topLevelItemCount()):
                item = self.bang.topLevelItem(i)
                if item.text(1) == ma:
                    self.bang.setCurrentItem(item)
                    break
        else:
            self.lbl_ket_qua.setText(
                f"❌ Không tìm thấy hàng hóa có mã '{ma}'."
            )

    def tim_kiem_theo_ten(self):
        """Tim kiem hang hoa theo ten (su dung Linear Search)."""
        tu_khoa = self.input_tim_ten.text().strip()
        if not tu_khoa:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập từ khóa cần tìm!")
            return

        ket_qua = self.danh_sach.tim_theo_ten(tu_khoa)
        danh_sach_kq = ket_qua.chuyen_sang_list()

        if danh_sach_kq:
            lines = [f"✅ TÌM THẤY {len(danh_sach_kq)} kết quả (Linear Search):\n"]
            for i, hang in enumerate(danh_sach_kq, 1):
                lines.append(
                    f"{i}. [{hang.ma_hang}] {hang.ten_hang}\n"
                    f"   Giá bán: {hang.tinh_gia_ban():,.0f} VND | SL: {hang.so_luong}"
                )
            self.lbl_ket_qua.setText("\n".join(lines))

            # Hien thi ket qua len bang
            self.cap_nhat_bang(ket_qua)
        else:
            self.lbl_ket_qua.setText(
                f"❌ Không tìm thấy hàng hóa nào có tên chứa '{tu_khoa}'."
            )
            self.cap_nhat_bang()

    # ─────────────────────────────────────────
    # SAP XEP
    # ─────────────────────────────────────────

    def _lay_tieu_chi_sap_xep(self):
        """Chuyen doi ten combo sang tieu chi sap xep."""
        tc = self.combo_tieu_chi.currentText()
        if tc == "Giá bán":
            return "gia_ban"
        elif tc == "Số lượng tồn kho":
            return "so_luong"
        elif tc == "Tên hàng":
            return "ten"
        elif tc == "Mã hàng":
            return "ma_hang"
        return "gia_ban"

    def sap_xep_merge(self):
        """Sap xep bang Merge Sort."""
        tieu_chi = self._lay_tieu_chi_sap_xep()
        tang_dan = self.combo_thu_tu.currentText() == "Tăng dần"

        self.danh_sach.sap_xep_merge(tieu_chi=tieu_chi, tang_dan=tang_dan)
        self.cap_nhat_bang()
        self.luu_du_lieu_tu_dong()

        ten_tc = self.combo_tieu_chi.currentText()
        thu_tu = "tăng dần" if tang_dan else "giảm dần"
        QMessageBox.information(
            self, "Sắp Xếp",
            f"Đã sắp xếp theo {ten_tc} ({thu_tu}) bằng Merge Sort!"
        )

    def sap_xep_quick(self):
        """Sap xep bang Quick Sort."""
        tieu_chi = self._lay_tieu_chi_sap_xep()
        tang_dan = self.combo_thu_tu.currentText() == "Tăng dần"

        self.danh_sach.sap_xep_quick(tieu_chi=tieu_chi, tang_dan=tang_dan)
        self.cap_nhat_bang()
        self.luu_du_lieu_tu_dong()

        ten_tc = self.combo_tieu_chi.currentText()
        thu_tu = "tăng dần" if tang_dan else "giảm dần"
        QMessageBox.information(
            self, "Sắp Xếp",
            f"Đã sắp xếp theo {ten_tc} ({thu_tu}) bằng Quick Sort!"
        )

    # ─────────────────────────────────────────
    # THONG KE
    # ─────────────────────────────────────────

    def cap_nhat_thong_ke(self):
        """Cap nhat cac thong so thong ke."""
        self.lbl_tong_mat_hang.setText(str(self.danh_sach.tong_so_luong()))
        self.lbl_tong_so_luong.setText(
            f"{self.danh_sach.tong_so_luong_hang():,}"
        )

        # Hang dat nhat
        dat = self.danh_sach.hang_dat_nhat()
        if dat:
            self.lbl_dat_nhat.setText(
                f"{dat.ten_hang}\n{dat.tinh_gia_ban():,.0f} VND"
            )
        else:
            self.lbl_dat_nhat.setText("Chưa có dữ liệu")

        # Hang re nhat
        re = self.danh_sach.hang_re_nhat()
        if re:
            self.lbl_re_nhat.setText(
                f"{re.ten_hang}\n{re.tinh_gia_ban():,.0f} VND"
            )
        else:
            self.lbl_re_nhat.setText("Chưa có dữ liệu")

        # Canh bao
        canh_bao_lines = []
        ds_het = self.danh_sach.danh_sach_sap_het()
        if ds_het.tong_so_luong() > 0:
            for hang in ds_het:
                canh_bao_lines.append(
                    f"⚠️ {hang.ten_hang} (SL: {hang.so_luong}) - Sắp hết hàng!"
                )

        ds_het_han = self.danh_sach.danh_sach_het_han()
        if ds_het_han.tong_so_luong() > 0:
            for hang in ds_het_han:
                con_lai = hang.so_ngay_con_lai()
                if con_lai < 0:
                    canh_bao_lines.append(
                        f"🚫 {hang.ten_hang} - Đã hết hạn!"
                    )
                else:
                    canh_bao_lines.append(
                        f"⏰ {hang.ten_hang} - Còn {con_lai} ngày hết hạn!"
                    )

        if canh_bao_lines:
            self.lbl_canh_bao.setText("\n".join(canh_bao_lines))
        else:
            self.lbl_canh_bao.setText("✅ Không có cảnh báo nào.")
            self.lbl_canh_bao.setStyleSheet(
                "color: #2e7d32; font-weight: bold; font-size: 13px;"
            )

        # Hien thi nut bao hanh neu co dien may
        co_dien_may = False
        for hang in self.danh_sach:
            if hang.loai_hang() == "DienMay":
                co_dien_may = True
                break
        self.btn_xem_bao_hanh.setVisible(co_dien_may)

    def xuat_tem_bao_hanh(self):
        """Hien thi tem bao hanh cho hang dien may dau tien."""
        for hang in self.danh_sach:
            if hang.loai_hang() == "DienMay":
                QMessageBox.information(
                    self, "Tém Bảo Hành",
                    hang.xuat_tem_bao_hanh()
                )
                return
        QMessageBox.information(self, "Thông Báo", "Không có hàng điện máy nào!")

    # ─────────────────────────────────────────
    # LOC DANH SACH
    # ─────────────────────────────────────────

    def loc_danh_sach(self, loai):
        """Loc danh sach theo loai hang."""
        if loai == "Tất cả":
            self.cap_nhat_bang()
        else:
            ds_loc = self.danh_sach.tim_theo_loai(loai)
            self.cap_nhat_bang(ds_loc)

    # ─────────────────────────────────────────
    # LUU / TAI DU LIEU
    # ─────────────────────────────────────────

    def luu_du_lieu(self):
        """Luu du lieu vao file JSON (nhan tu nut Luu)."""
        try:
            self.danh_sach.luu_vao_file(self.duong_dan_file)
            QMessageBox.information(self, "Thành Công", "Đã lưu dữ liệu thành công!")
        except LoiFile as e:
            QMessageBox.critical(self, "Lỗi File", str(e))

    def luu_du_lieu_tu_dong(self):
        """Luu du lieu tu dong (sau khi them/sua/xoa/sap xep)."""
        try:
            self.danh_sach.luu_vao_file(self.duong_dan_file)
        except LoiFile:
            pass  # Tu dong luu that bai thi khong thong bao

    def tai_du_lieu(self):
        """Tai du lieu tu file JSON khi khoi dong."""
        try:
            if os.path.exists(self.duong_dan_file):
                self.danh_sach.doc_tu_file(self.duong_dan_file)
                self.cap_nhat_bang()
        except LoiFile as e:
            QMessageBox.warning(self, "Cảnh Báo", str(e))

    # ─────────────────────────────────────────
    # LAM MOI FORM
    # ─────────────────────────────────────────

    def lam_moi_form(self):
        """Xoa toan bo noi dung form nhap lieu."""
        self.input_ma.clear()
        self.input_ma.setEnabled(True)
        self.input_ten.clear()
        self.input_so_luong.setValue(0)
        self.input_gia_nhap.setValue(0)
        self.combo_loai.setCurrentText("ThucPham")
        self.input_nsx.setDate(QDate.currentDate())
        self.input_hsd.setDate(QDate.currentDate().addMonths(6))
        self.input_bao_hanh.setValue(12)
        self.input_cong_suat.clear()
        self.combo_chat_lieu.setCurrentIndex(0)

        # Khoi phuc nut them
        if self.dang_sua:
            try:
                self.btn_them_hang.disconnect()
            except TypeError:
                pass
            self.btn_them_hang.clicked.connect(self.them_hang)
            self.dang_sua = False
            self.ma_dang_sua = None
            self.lbl_form_tieu_de.setText("THÊM HÀNG MỚI")
            self.btn_them_hang.setText("➕  Thêm Hàng")