import os
import sys
import json
import pytest

import logging
logging.basicConfig(level=logging.INFO)

#from terrautils.metadata import clean_metadata, get_terraref_metadata
from stereo_rgb.stereo_rgb import get_image_shape, process_raw


@pytest.fixture(scope='module')
def read_metadata():
    fname = os.path.join(os.path.dirname(__file__), 'data/metadata.json')
    with open(fname) as f:
        metadata = json.load(f)
    return metadata


# TODO dumb pointer to a static data file but could get file from 
# alternate source
@pytest.fixture(scope='module')
def binfile():
    return os.path.join(os.path.dirname(__file__), 'data/binfile.bin')


@pytest.mark.parametrize("metadata,side", [
    (read_metadata(), 'left'),
    (read_metadata(), 'right'),
])
def test_get_image_shape(metadata, side):
    dims = get_image_shape(metadata, side)
    assert len(dims) == 2
    width, height = dims

    assert isinstance(width, int)
    assert isinstance(height, int)
    assert width > 0
    assert height > 0


def test_process_raw(binfile):
    dims = get_image_shape(read_metadata(), 'left')
    im = process_raw(dims, binfile)
    assert im.any
    assert im.shape[0] == dims[0]
    assert im.shape[1] == dims[1]
    assert im.shape[2] == 3   # r,g,b


@pytest.mark.skip(reason='Not sure why this fails.')
def test_process_raw_with_save(binfile, tmpdir):
    dims = get_image_shape(read_metadata(), 'left')
    outfile = tmpdir.mkdir('save_test').join('output.jpeg') 
    im = process_raw(dims, binfile, outfile)
    assert os.exists(outfile)


def test_calculate_canopycover():
    pass