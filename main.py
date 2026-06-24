"""
main.py - File thuc thi chinh cua ung dung Quan Ly Sieu Thi

Chay chuong trinh:
  python main.py

Yeu cau:
  pip install PyQt6
"""

import sys
import os

# Dam bao import duong dan dung
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.giao_dien import GiaoDienChinh


def main():
    """Ham chinh - Khoi dong ung dung."""
    # Tao ung dung
    app = QApplication(sys.argv)
    app.setApplicationName("He Thong Quan Ly Hang Hoa Sieu Thi")

    # Tao va hien thi giao dien chinh
    cua_so = GiaoDienChinh()
    cua_so.show()

    # Chay vong lap chinh
    sys.exit(app.exec())


if __name__ == "__main__":
    main()