"""
Global test fixtures
"""
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Dict
from typing import List
from typing import Tuple

import numpy as np
import pytest
from astropy.io import fits
from dkist_data_simulator.dataset import key_function
from dkist_data_simulator.spec122 import Spec122Dataset
from dkist_header_validator import spec122_validator

from dkist_processing_common._util.constants import Constants
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common._util.tags import TagDB
from dkist_processing_common.models.graphql import InputDatasetResponse
from dkist_processing_common.models.graphql import RecipeInstanceResponse
from dkist_processing_common.models.graphql import RecipeRunResponse
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess


@pytest.fixture()
def recipe_run_id():
    return randint(0, 99999)


@pytest.fixture()
def tag_db(recipe_run_id) -> TagDB:
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags")
    yield t
    t.purge()
    t.close()


@pytest.fixture()
def tag_db2(recipe_run_id) -> TagDB:
    """
    Another instance of a tag db in the same redis db
    """
    recipe_run_id = recipe_run_id + 15  # same db number but different namespace
    t = TagDB(recipe_run_id=recipe_run_id, task_name="test_tags2")
    yield t
    t.purge()
    t.close()


@pytest.fixture(params=[None, "use_tmp_path"])
def workflow_file_system(request, recipe_run_id, tmp_path) -> Tuple[WorkflowFileSystem, int, Path]:
    if request.param == "use_tmp_path":
        path = tmp_path
    else:
        path = request.param
    wkflow_fs = WorkflowFileSystem(
        recipe_run_id=recipe_run_id,
        task_name="wkflow_fs_test",
        scratch_base_path=path,
    )
    yield wkflow_fs, recipe_run_id, tmp_path
    wkflow_fs.purge(ignore_errors=True)
    tmp_path.rmdir()
    wkflow_fs.close()


@pytest.fixture()
def constants(recipe_run_id) -> Constants:
    constants = Constants(recipe_run_id=recipe_run_id, task_name="test_constants")
    yield constants
    constants.purge()
    constants.close()


class CommonDataset(Spec122Dataset):
    def __init__(self):
        super().__init__(
            array_shape=(1, 10, 10),
            time_delta=1,
            dataset_shape=(4, 10, 10),
            instrument="visp",
            start_time=datetime(2020, 1, 1, 0, 0, 0),
        )

        self.add_constant_key("DATE_BGN", "2020-01-01T00:00:00.000")
        self.add_constant_key("TELEVATN", 6.28)
        self.add_constant_key("TAZIMUTH", 3.14)
        self.add_constant_key("TTBLANGL", 1.23)
        self.add_constant_key("INST_FOO", "bar")
        self.add_constant_key("DKIST004", "observe")
        self.add_constant_key("ID___005", "ip id")
        self.add_constant_key("PAC__004", "Polarizer")
        self.add_constant_key("PAC__005", 31.2)
        self.add_constant_key("PAC__006", "clear")
        self.add_constant_key("PAC__007", 6.66)
        self.add_constant_key("PAC__008", "DarkShutter")
        self.add_constant_key("INSTRUME", "VBI")
        self.add_constant_key("WAVELNTH", 1080.0)
        self.add_constant_key("DATE-OBS", "2020-01-02T00:00:00.000")
        self.add_constant_key("DATE-END", "2020-01-03T00:00:00.000")
        self.add_constant_key("ID___013", "PROPOSAL_ID1")
        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("PAC__003", "on")
        self.add_constant_key("TELSCAN", "Raster")
        self.add_constant_key("DKIST008", 1)
        self.add_constant_key("DKIST009", 1)


@pytest.fixture()
def complete_common_header():
    """
    A header with some common by-frame keywords
    """
    ds = CommonDataset()
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]

    return header_list[0]


class CalibrationSequenceDataset(Spec122Dataset):
    def __init__(
        self,
        array_shape: Tuple[int, ...],
        time_delta: float,
        instrument="visp",
    ):
        self.num_frames_per_CS_step = 5

        # Make up a Calibration sequence. Mostly random except for two clears and two darks at start and end, which
        # we want to test
        self.pol_status = [
            "clear",
            "clear",
            "Polarizer",
            "Polarizer",
            "Polarizer",
            "clear",
            "clear",
        ]
        self.pol_theta = [0.0, 0.0, 60.0, 60.0, 120.0, 0.0, 0.0]
        self.ret_status = ["clear", "clear", "clear", "SiO2", "clear", "clear", "clear"]
        self.ret_theta = [0.0, 0.0, 0.0, 45.0, 0.0, 0.0, 0.0]
        self.dark_status = [
            "DarkShutter",
            "FieldStop (2.8arcmin)",
            "FieldStop (2.8arcmin)",
            "FieldStop (2.8arcmin)",
            "FieldStop (2.8arcmin)",
            "FieldStop (2.8arcmin)",
            "DarkShutter",
        ]

        self.num_steps = len(self.pol_theta)
        dataset_shape = (self.num_steps * self.num_frames_per_CS_step,) + array_shape[1:]
        super().__init__(
            dataset_shape,
            array_shape,
            time_delta,
            instrument=instrument,
            start_time=datetime(2020, 1, 1, 0, 0, 0),
        )
        self.add_constant_key("DKIST004", "polcal")
        self.add_constant_key("TELEVATN", 6.28)
        self.add_constant_key("ID___013", "PROPOSAL_ID1")
        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("PAC__003", "on")

    @property
    def cs_step(self) -> int:
        return self.index // self.num_frames_per_CS_step

    @key_function("PAC__004")
    def polarizer_status(self, key: str) -> str:
        return self.pol_status[self.cs_step]

    @key_function("PAC__005")
    def polarizer_angle(self, key: str) -> float:
        return self.pol_theta[self.cs_step]

    @key_function("PAC__006")
    def retarder_status(self, key: str) -> str:
        return self.ret_status[self.cs_step]

    @key_function("PAC__007")
    def retarder_angle(self, key: str) -> float:
        return self.ret_theta[self.cs_step]

    @key_function("PAC__008")
    def gos_level3_status(self, key: str) -> str:
        return self.dark_status[self.cs_step]


class NonPolCalDataset(Spec122Dataset):
    def __init__(self):
        super().__init__(
            dataset_shape=(4, 2, 2),
            array_shape=(1, 2, 2),
            time_delta=1,
            instrument="visp",
            start_time=datetime(2020, 1, 1, 0, 0, 0),
        )  # Instrument doesn't matter
        self.add_constant_key("DKIST004", "dark")  # Anything that's not polcal
        self.add_constant_key("ID___013", "PROPOSAL_ID1")
        self.add_constant_key("TELEVATN", 6.28)
        self.add_constant_key("PAC__002", "clear")
        self.add_constant_key("PAC__003", "on")
        self.add_constant_key("PAC__004", "Polarizer")
        self.add_constant_key("PAC__005", 0.0)
        self.add_constant_key("PAC__006", "clear")
        self.add_constant_key("PAC__007", 0.0)
        self.add_constant_key("PAC__008", "DarkShutter")


@pytest.fixture(scope="session")
def grouped_cal_sequence_headers() -> Dict[int, List[L0FitsAccess]]:
    ds = CalibrationSequenceDataset(array_shape=(1, 2, 2), time_delta=2.0)
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]
    expected_cs_dict = defaultdict(list)
    for i in range(ds.num_steps):
        for j in range(ds.num_frames_per_CS_step):
            expected_cs_dict[i].append(L0FitsAccess.from_header(header_list.pop(0)))

    return expected_cs_dict


@pytest.fixture(scope="session")
def non_polcal_headers() -> List[L0FitsAccess]:
    ds = NonPolCalDataset()
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]
    obj_list = [L0FitsAccess.from_header(h) for h in header_list]
    return obj_list


class FakeGQLClient:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def execute_gql_query(**kwargs):
        query_base = kwargs["query_base"]

        if query_base == "recipeRuns":
            return [
                RecipeRunResponse(
                    recipeInstanceId=1,
                    recipeInstance=RecipeInstanceResponse(
                        recipeId=1,
                        inputDataset=InputDatasetResponse(
                            inputDatasetId=1,
                            isActive=True,
                            inputDatasetDocument='{"bucket": "bucket-name", "parameters": [{"parameterName": "", "parameterValues": [{"parameterValueId": 1, "parameterValue": "[[1,2,3],[4,5,6],[7,8,9]]", "parameterValueStartDate": "1/1/2000"}]}], "frames": ["objectKey1", "objectKey2", "objectKeyN"]}',
                        ),
                    ),
                )
            ]

    @staticmethod
    def execute_gql_mutation(**kwargs):
        ...


@pytest.fixture()
def calibrated_header():
    hdu = fits.PrimaryHDU(data=np.ones((1, 128, 128)))
    hdu.header["TELEVATN"] = 6.28
    hdu.header["TAZIMUTH"] = 3.14
    hdu.header["TTBLANGL"] = 1.23
    hdu.header["DATE-OBS"] = "2020-05-25T00:00:00.000"
    hdu.header["DKIST004"] = "observe"
    hdu.header["ID___004"] = "ip id"
    hdu.header["PAC__004"] = "Polarizer"
    hdu.header["PAC__005"] = 0
    hdu.header["PAC__006"] = "clear"
    hdu.header["PAC__007"] = 0
    hdu.header["PAC__008"] = "FieldStop (2.8arcmin)"
    hdu.header["INSTRUME"] = "VISP"
    hdu.header["LINEWAV"] = 1080.0
    hdu.header["DATE-BGN"] = "2020-03-13T00:00:00.000"
    hdu.header["DATE-END"] = "2021-08-15T00:00:00.000"
    hdu.header["ID___013"] = "PROPOSAL_ID1"
    hdu.header["ID___005"] = "id string"
    hdu.header["PAC__002"] = "clear"
    hdu.header["PAC__003"] = "on"
    hdu.header["TELSCAN"] = "Raster"
    hdu.header["DKIST008"] = 1
    hdu.header["DKIST009"] = 1
    hdu.header["BTYPE"] = ""
    hdu.header["BUNIT"] = ""
    hdu.header["CAMERA"] = ""
    hdu.header["CDELT1"] = 1
    hdu.header["CDELT2"] = 1
    hdu.header["CDELT3"] = 1
    hdu.header["CRPIX1"] = 0
    hdu.header["CRPIX2"] = 0
    hdu.header["CRPIX3"] = 0
    hdu.header["CRVAL1"] = 0
    hdu.header["CRVAL2"] = 0
    hdu.header["CRVAL3"] = 0
    hdu.header["CTYPE1"] = ""
    hdu.header["CTYPE2"] = ""
    hdu.header["CTYPE3"] = ""
    hdu.header["CUNIT1"] = ""
    hdu.header["CUNIT2"] = ""
    hdu.header["CUNIT3"] = ""
    hdu.header["DATE"] = "2021-08-20T00:00:00.000"
    hdu.header["DKIST003"] = "observe"
    hdu.header["DKISTVER"] = ""
    hdu.header["ID___012"] = ""
    hdu.header["CAM__002"] = ""
    hdu.header["CAM__004"] = 1
    hdu.header["CAM__005"] = 1
    hdu.header["CAM__014"] = 1
    hdu.header["FILE_ID"] = ""
    hdu.header["ID___001"] = ""
    hdu.header["ID___002"] = ""
    hdu.header["ID___008"] = ""
    hdu.header["NETWORK"] = "NSF-DKIST"
    hdu.header["OBJECT"] = "quietsun"
    hdu.header["OBSERVAT"] = "Haleakala High Altitude Observatory Site"
    hdu.header["OBSPR_ID"] = ""
    hdu.header["ORIGIN"] = "National Solar Observatory"
    hdu.header["TELESCOP"] = "Daniel K. Inouye Solar Telescope"
    hdu.header["WAVELNTH"] = 123.45
    hdu.header["WCSAXES"] = 3
    hdu.header["WCSNAME"] = ""
    hdu.header["PC1_1"] = 0
    hdu.header["PC1_2"] = 0
    hdu.header["PC1_3"] = 0
    hdu.header["PC2_1"] = 0
    hdu.header["PC2_2"] = 0
    hdu.header["PC2_3"] = 0
    hdu.header["PC3_1"] = 0
    hdu.header["PC3_2"] = 0
    hdu.header["PC3_3"] = 0
    hdu.header["CHECKSUM"] = ""
    hdu.header["DATASUM"] = ""
    hdu.header["NBIN"] = 1
    hdu.header["NBIN1"] = 1
    hdu.header["NBIN2"] = 1
    hdu.header["NBIN3"] = 1
    hdu.header["CAM__001"] = "cam string"
    hdu.header["CAM__003"] = 1
    hdu.header["CAM__006"] = 1
    hdu.header["CAM__007"] = 1
    hdu.header["CAM__008"] = 1
    hdu.header["CAM__009"] = 1
    hdu.header["CAM__010"] = 1
    hdu.header["CAM__011"] = 1
    hdu.header["CAM__012"] = 1
    hdu.header["CAM__013"] = 1
    hdu.header["CAM__015"] = 1
    hdu.header["CAM__016"] = 1
    hdu.header["CAM__017"] = 1
    hdu.header["CAM__018"] = 1
    hdu.header["CAM__019"] = 1
    hdu.header["CAM__020"] = 1
    hdu.header["CAM__033"] = 1
    hdu.header["CAM__034"] = 1
    hdu.header["CAM__035"] = 1
    hdu.header["CAM__036"] = 1
    hdu.header["CAM__037"] = 1
    hdu.header["DKIST001"] = "Auto"
    hdu.header["DKIST002"] = "Full"
    hdu.header["DKIST005"] = "id string"
    hdu.header["DKIST006"] = "Good"
    hdu.header["DKIST007"] = True
    hdu.header["DKIST010"] = 1
    hdu.header["ID___003"] = "id string"
    hdu.header["ID___006"] = "id string"
    hdu.header["ID___007"] = "id string"
    hdu.header["ID___009"] = "id string"
    hdu.header["ID___010"] = "id string"
    hdu.header["ID___011"] = "id string"
    hdu.header["ID___014"] = "id string"
    hdu.header["PAC__001"] = "open"
    hdu.header["PAC__009"] = "None"
    hdu.header["PAC__010"] = "closed"
    hdu.header["PAC__011"] = 0
    hdu.header["WS___001"] = "ws string"
    hdu.header["WS___002"] = 0
    hdu.header["WS___003"] = 0
    hdu.header["WS___004"] = 0
    hdu.header["WS___005"] = 0
    hdu.header["WS___006"] = 0
    hdu.header["WS___007"] = 0
    hdu.header["WS___008"] = 0

    return spec122_validator.validate_and_translate_to_214_l0(hdu.header, return_type=fits.HDUList)[
        0
    ].header
