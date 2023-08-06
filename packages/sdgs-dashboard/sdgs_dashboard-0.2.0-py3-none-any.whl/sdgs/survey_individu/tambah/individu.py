import attr
from datetime import date
from typing import Any, Dict, List, Optional

from . import Agama
from . import FasilitasKesehatan
from . import KondisiPekerjaan
from . import PekerjaanUtama
from . import PendidikanTertinggi
from . import Penghasilan
from . import PenyakitDiderita
from . import StatusPernikahan


MAPPING = {
    "desa": "desa",
    "I.P103": "nama",
    "I.P104": "jenis_kelamin",
    "I.P105": "tempat_lahir",
    "I.P106": "tanggal_lahir",
    "I.P107": "usia",
    "I.P108": "status_pernikahan",
    "I.P109": "usia_menikah",
    "I.P110": "agama",
    "I.P111": "suku_bangsa",
    "I.P112": "warga_negara",
    "I.P113": "nomor_hp",
    "I.P114": "nomor_whatsapp",
    "I.P115": "alamat_email",
    "I.P116": "alamat_facebook",
    "I.P117": "alamat_twitter",
    "I.P118": "alamat_instagram",
    "I.P119": "aktif_internet",
    "I.P120": "akses_melalui",
    "I.P121": "kecepatan_internet",
    "I.P201": "kondisi_pekerjaan",
    "I.P202": "pekerjaan_utama",
    "I.P202-Comment": "pekerjaan_utama_comment",
    "I.P203": "jaminan_sosial_ketenagakerjaan",
    "I.P204": "penghasilan",
    "I.P204_penghasilan": "pekerjaan_penghasilan",
    "I.P401": "penyakit_diderita",
    "I.P402": "fasilitas_kesehatan",
    "I.P403": "jamsos_ketenagakerjaan",
    "I.P404": "penyakit_diderita",
    "I.P405": "setahun_melahirkan",
    "I.P406": "mendapat_asi",
    "I.P501": "pendidikan_tertinggi",
    "I.P502": "tahun_pendidikan",
    "I.P505": "bahasa_permukiman",
    "I.P506": "bahasa_formal",
    "I.P507": "kerja_bakti",
    "I.P508": "siskamling",
    "I.P509": "pesta_rakyat",
    "I.P510": "menolong_kematian",
    "I.P511": "menolong_sakit",
    "I.P512": "menolong_kecelakaan",
    "I.P513": "memperoleh_pelayanan_desa",
    "I.P514": "pelayanan_desa",
    "I.P515": "saran_desa",
    "I.P516": "keterbukaan_desa",
    "I.P517": "terjadi_bencana",
    "I.P518": "terdampak_bencana",
    "kecamatan": "kecamatan",
    "kota": "kota",
    "nik": "nik",
    "no_kk": "no_kk",
    "provinsi": "provinsi",
    "rt": "rt",
    "rw": "rw",
}


@attr.dataclass
class TambahIndividu:
    desa: str
    nama: str
    jenis_kelamin: str
    tempat_lahir: str
    tanggal_lahir: date
    usia: str
    status_pernikahan: StatusPernikahan
    usia_menikah: Optional[str]
    agama: Agama
    suku_bangsa: str
    warga_negara: str
    nomor_hp: str
    nomor_whatsapp: Optional[str]
    alamat_email: Optional[str]
    alamat_facebook: Optional[str]
    alamat_twitter: Optional[str]
    alamat_instagram: Optional[str]
    aktif_internet: bool
    akses_melalui: Optional[str]
    kecepatan_internet: str
    kondisi_pekerjaan: KondisiPekerjaan
    pekerjaan_utama: Optional[PekerjaanUtama]
    pekerjaan_utama_comment: Optional[str]
    jaminan_sosial_ketenagakerjaan: Optional[str]
    penghasilan: List[Penghasilan]
    pekerjaan_penghasilan: str
    # P400
    penyakit_diderita: PenyakitDiderita
    fasilitas_kesehatan: FasilitasKesehatan
    jamsos_ketenagakerjaan: str
    setahun_melahirkan: Optional[bool]
    mendapat_asi: Optional[bool]
    # Pendidikan
    pendidikan_tertinggi: PendidikanTertinggi
    tahun_pendidikan: int
    bahasa_permukiman: str
    bahasa_formal: str
    kerja_bakti: str
    siskamling: str
    pesta_rakyat: str
    menolong_kematian: str
    menolong_sakit: str
    menolong_kecelakaan: str
    memperoleh_pelayanan_desa: str
    pelayanan_desa: bool
    saran_desa: str
    keterbukaan_desa: str
    terjadi_bencana: bool
    terdampak_bencana: Optional[bool]
    # Alamat
    kecamatan: str
    kota: str
    nik: str
    no_kk: str
    provinsi: str
    rt: str
    rw: str

    def __attrs_post_init__(self) -> None:
        if self.status_pernikahan.bu and not self.usia_menikah:
            raise ValueError(
                f"{self.nik} Mohon diisi usia menikah, apabila sudah menikah"
            )
        if self.aktif_internet and not self.akses_melalui:
            raise ValueError(f"{self.nik} Mohon diisi usia menikah")
        if self.kondisi_pekerjaan == KondisiPekerjaan.BEKERJA:
            if not self.pekerjaan_utama:
                raise ValueError(f"{self.nik} Mohon diisi pekerjaan utama, jika bekerja")
            if self.pekerjaan_utama == PekerjaanUtama.LAINNYA and not self.pekerjaan_utama_comment:
                raise ValueError(f"{self.nik} Mohon diisi nama pekerjaan utama, jika kondisinya lainnya")
            if not self.jaminan_sosial_ketenagakerjaan:
                raise ValueError(f"{self.nik} Mohon diisi jamsos ketenagakerjaan, jika bekerja")
        else:
            # TODO Isi Penghasilan
            pass

    def todict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = dict()
        for key, name in MAPPING.items():
            if not hasattr(self, name):
                continue
            value: Any = getattr(self, name)
            if value in (None, "None"):
                continue
            if hasattr(value, "todict") and callable(getattr(value, "todict")):
                real_value: Any = getattr(value, "todict", lambda: None)()
                if real_value in (None, "None"):
                    continue
                data[key] = real_value
            else:
                data[key] = value
        return data
