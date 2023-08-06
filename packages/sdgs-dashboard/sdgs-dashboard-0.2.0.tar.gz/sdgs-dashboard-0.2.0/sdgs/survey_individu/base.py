import cattr
from typing import Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from sdgs import Sdgs

from .tambah import Penghasilan
from .tambah import PenyakitDiderita
from . import SurveyPagedData, TambahIndividu
from sdgs import SdgsResponse


class SurveyIndividu:
    def __init__(self, sdgs: "Sdgs"):
        self.sdgs = sdgs
        cattr.register_unstructure_hook(Penghasilan, Penghasilan.todict)
        cattr.register_unstructure_hook(PenyakitDiderita, PenyakitDiderita.todict)

    def __call__(
        self,
        page: int = 1,
        search: str = "",
        pageSize: int = 50,
        isSortAsc: bool = True,
        kodeDesa: str = None,
    ) -> List[SurveyPagedData]:
        return self.getSurveyPagedData(
            page=page,
            search=search,
            pageSize=pageSize,
            isSortAsc=isSortAsc,
            kodeDesa=kodeDesa,
        )

    def getSurveyPagedData(
        self,
        page: int = 1,
        search: str = "",
        pageSize: int = 50,
        isSortAsc: bool = True,
        kodeDesa: str = None,
    ) -> List[SurveyPagedData]:
        json_data = {
            "isSortAsc": isSortAsc,
            "kodeDesa": kodeDesa or self.sdgs.token.wilayah,
            "page": page,
            "pageSize": pageSize,
            "search": search,
        }
        return self.sdgs.api_post_to_res(
            "surveyIndividu/getSurveyPagedData",
            List[SurveyPagedData],
            json=json_data,
        )

    def validateNik(
        self,
        nik: str,
    ):
        json_data = {"nik": nik}
        return self.sdgs.api_post_to_res(
            "surveyIndividu/validateNik",
            str,
            json=json_data,
        )

    def save(self, individu: TambahIndividu):
        json_data = individu.todict()
        return self.sdgs.api_post_to_res(
            "surveyIndividu/save",
            str,
            json=json_data,
        )
