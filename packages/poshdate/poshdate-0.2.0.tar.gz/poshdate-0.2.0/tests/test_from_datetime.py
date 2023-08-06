from datetime import datetime
import pytest
from pytest import param
import poshdate


@pytest.mark.parametrize(
    "date_obj, expected",
    [
        param(datetime(2021, 5, 1), "1st May 2021", id="1st"),
        param(datetime(2020, 4, 2), "2nd April 2020", id="2nd"),
        param(datetime(2019, 11, 3), "3rd November 2019", id="3rd"),
        param(datetime(2018, 9, 4), "4th September 2018", id="4th"),
        param(datetime(1999, 2, 11), "11th February 1999", id="11th"),
        param(datetime(1999, 2, 19), "19th February 1999", id="19th"),
        param(datetime(1998, 8, 21), "21st August 1998", id="21st"),
        param(datetime(1997, 7, 22), "22nd July 1997", id="22nd"),
        param(datetime(1996, 3, 23), "23rd March 1996", id="23rd"),
        param(datetime(1995, 10, 27), "27th October 1995", id="27th"),
        param(datetime(1994, 6, 30), "30th June 1994", id="30th"),
        param(datetime(2010, 1, 31), "31st January 2010", id="31st"),
        param(datetime(2020, 2, 29), "29th February 2020", id="leapyear"),
    ],
)


# Test Valid dates
def test_from_datetime(date_obj, expected):
    assert poshdate.from_datetime(date_obj) == expected


# Test Invalid dates
def test_from_datetime_invalid_leapyear():
    with pytest.raises(ValueError):
        date_ = datetime(2021, 2, 29)


# Invalid argument types
def test_from_datetime_int():
    with pytest.raises(TypeError):
        date_ = 3
        poshdate.from_datetime(date_)


def test_from_datetime_str():
    with pytest.raises(TypeError):
        date_ = "4"
        poshdate.from_datetime(date_)


def test_from_datetime_str_yyyyddmm():
    with pytest.raises(TypeError):
        date_ = "2020-12-12"
        poshdate.from_datetime(date_)
