import logging
from random import randint
from typing import Literal

import numpy as np
import pytest
from astropy.io import fits

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.write_l1 import WriteL1Frame
from dkist_processing_common.tests.conftest import FakeGQLClient


class CompleteWriteL1Frame(WriteL1Frame):
    def add_dataset_headers(
        self, header: fits.Header, stokes: Literal["I", "Q", "U", "V"]
    ) -> fits.Header:
        header["DAAXES"] = 2
        header["DEAXES"] = 3
        header["DNAXIS"] = 5
        header["FRAMEWAV"] = 123.45
        header["LEVEL"] = 1
        header["WAVEMAX"] = 124
        header["WAVEMIN"] = 123
        header["WAVEREF"] = "Air"
        header["WAVEUNIT"] = -9
        header["DINDEX3"] = 3
        header["DINDEX4"] = 2
        header["DINDEX5"] = 1
        header["DNAXIS1"] = header["NAXIS1"]
        header["DNAXIS2"] = header["NAXIS2"]
        header["DNAXIS3"] = 10
        header["DNAXIS4"] = 1
        header["DNAXIS5"] = 4
        header["DPNAME1"] = ""
        header["DPNAME2"] = ""
        header["DPNAME3"] = ""
        header["DPNAME4"] = ""
        header["DPNAME5"] = ""
        header["DTYPE1"] = "SPATIAL"
        header["DTYPE2"] = "SPATIAL"
        header["DTYPE3"] = "TEMPORAL"
        header["DTYPE4"] = "SPECTRAL"
        header["DTYPE5"] = "STOKES"
        header["DUNIT1"] = ""
        header["DUNIT2"] = ""
        header["DUNIT3"] = ""
        header["DUNIT4"] = ""
        header["DUNIT5"] = ""
        header["DWNAME1"] = ""
        header["DWNAME2"] = ""
        header["DWNAME3"] = ""
        header["DWNAME4"] = ""
        header["DWNAME5"] = ""
        header["CALVERS"] = ""
        header["CAL_URL"] = ""
        header["HEADVERS"] = ""
        header["HEAD_URL"] = ""
        header["INFO_URL"] = ""

        return header


@pytest.fixture(scope="function", params=[1, 4])
def write_l1_task(calibrated_header, request):
    with CompleteWriteL1Frame(
        recipe_run_id=randint(0, 99999),
        workflow_name="workflow_name",
        workflow_version="workflow_version",
    ) as task:
        num_of_stokes_params = request.param
        stokes_params = ["I", "Q", "U", "V"]
        hdu = fits.PrimaryHDU(data=np.ones(shape=(128, 128)), header=calibrated_header)
        logging.info(f"{num_of_stokes_params=}")
        hdul = fits.HDUList([hdu])
        for i in range(num_of_stokes_params):
            task.fits_data_write(
                hdu_list=hdul,
                tags=[Tag.calibrated(), Tag.frame(), Tag.stokes(stokes_params[i])],
            )
        task.constants[BudName.average_cadence.value] = 10
        task.constants[BudName.minimum_cadence.value] = 10
        task.constants[BudName.maximum_cadence.value] = 10
        task.constants[BudName.variance_cadence.value] = 0
        yield task, num_of_stokes_params
        task.constants.purge()
        task.scratch.purge()


def test_write_l1_frame(write_l1_task, mocker):
    """
    :Given: a write L1 task
    :When: running the task
    :Then: no errors are raised
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, num_of_stokes_params = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    logging.info(f"{files=}")
    assert len(files) == num_of_stokes_params
    for file in files:
        logging.info(f"Checking file {file}")
        assert file.exists


def test_replace_header_values(write_l1_task, calibrated_header):
    """
    :Given: an input header
    :When: replacing specific header values
    :Then: the header values have changed
    """
    task, _ = write_l1_task
    original_file_id = calibrated_header["FILE_ID"]
    original_date = calibrated_header["DATE"]
    header = task._replace_header_values(header=calibrated_header)
    assert header["FILE_ID"] != original_file_id
    assert header["DATE"] != original_date


def test_l1_filename(write_l1_task, calibrated_header):
    """
    :Given: an input header
    :When: asking for the corresponding L1 filename
    :Then: the filename is formatted as expected
    """
    task, _ = write_l1_task
    assert (
        task.l1_filename(header=calibrated_header, stokes="Q")
        == "VISP_L1_01080000_2020_05_25T00_00_00_000_Q.fits"
    )


def test_calculate_date_avg(write_l1_task, calibrated_header):
    """
    :Given: an input header
    :When: finding the average date
    :Then: the correct datetime string is returned
    """
    task, _ = write_l1_task
    assert task._calculate_date_avg(header=calibrated_header) == "2021-01-03T12:00:00.000"


def test_calculate_telapse(write_l1_task, calibrated_header):
    """
    :Given: an input header
    :When: finding the time elapsed in an observation
    :Then: the correct time value is returned
    """
    task, _ = write_l1_task
    assert task._calculate_telapse(header=calibrated_header) == 38620800


def test_solarnet_keys(write_l1_task, mocker):
    """
    :Given: files with headers converted to SPEC 214 L1
    :When: checking the solarnet extra headers
    :Then: the correct values are found
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, _ = write_l1_task
    task()
    files = list(task.read(tags=[Tag.frame(), Tag.output()]))
    logging.info(f"{files=}")
    for file in files:
        header = fits.open(file)[1].header
        assert header["DATEREF"] == header["DATE-BEG"]
        assert round(header["OBSGEO-X"]) == -5466045
        assert round(header["OBSGEO-Y"]) == -2404389
        assert round(header["OBSGEO-Z"]) == 2242134
        assert round(header["OBS_VR"]) == -144
        assert header["SPECSYS"] == "TOPOCENT"
        assert header["VELOSYS"] is False
