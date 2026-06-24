"""
nut.py - Dinh nghia Node cho Danh sach lien ket doi (Doubly Linked List)

Moi Node chua:
  - du_lieu: doi tuong HangHoa (hoac lop dan xuat)
  - truoc: con tro toi Node phia truoc
  - sau: con tro toi Node phia sau
"""


class Nut:
    """Lop Node cho danh sach lien ket doi."""

    def __init__(self, du_lieu=None):
        """
        Khoi tao Node moi.

        Args:
            du_lieu: Doi tuong hang hoa luu trong node (mac dinh None).
        """
        self.du_lieu = du_lieu
        self.truoc = None
        self.sau = None

    def __str__(self):
        """Tra ve chuoi bieu dien cua Node."""
        if self.du_lieu is not None:
            return str(self.du_lieu)
        return "Node(rong)"