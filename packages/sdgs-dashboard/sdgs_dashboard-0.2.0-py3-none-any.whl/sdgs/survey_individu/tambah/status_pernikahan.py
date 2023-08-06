from enum import Enum


class StatusPernikahan(Enum):
    BELUM_KAWIN = "1"
    KAWIN = "2"
    CERAI_HIDUP = "3"
    CERAI_MATI = "4"

    @property
    def bu(self) -> bool:
        """Mengecek apa membutuhkan usia menikah"""
        if self.value == self.KAWIN:
            return True
        elif self.value == self.CERAI_HIDUP:
            return True
        elif self.value == self.CERAI_MATI:
            return True
        return False
