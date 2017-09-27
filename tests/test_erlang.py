import pytest
from .. import stimulus


def test_erlang_c():
    assert stimulus.required_server_count(aht=752, interval=900, rate=25, target=.90, target_type='SL', wait_time=20) == 28.0

def test_erlang_c_service_level():
    assert .9042 <= stimulus.service_level(aht=752, interval=900, rate=35, server_count=37, wait_time=20) <= .9043

