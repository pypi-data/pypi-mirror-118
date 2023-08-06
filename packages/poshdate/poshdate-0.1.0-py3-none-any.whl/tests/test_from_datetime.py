from datetime import datetime
import pytest
from poshdate import formatter


# Test Valid dates
def test_from_datetime_1st():
    date_ = datetime(2021, 5, 1)
    assert formatter.from_datetime(date_) == "1st May 2021"


def test_from_datetime_2nd():
    date_ = datetime(2020, 4, 2)
    assert formatter.from_datetime(date_) == "2nd April 2020"


def test_from_datetime_3rd():
    date_ = datetime(2019, 11, 3)
    assert formatter.from_datetime(date_) == "3rd November 2019"


def test_from_datetime_4th():
    date_ = datetime(2018, 9, 4)
    assert formatter.from_datetime(date_) == "4th September 2018"


def test_from_datetime_11th():
    date_ = datetime(1999, 2, 11)
    assert formatter.from_datetime(date_) == "11th February 1999"


def test_from_datetime_19th():
    date_ = datetime(1999, 2, 19)
    assert formatter.from_datetime(date_) == "19th February 1999"


def test_from_datetime_21st():
    date_ = datetime(1998, 8, 21)
    assert formatter.from_datetime(date_) == "21st August 1998"


def test_from_datetime_22nd():
    date_ = datetime(1997, 7, 22)
    assert formatter.from_datetime(date_) == "22nd July 1997"


def test_from_datetime_23rd():
    date_ = datetime(1996, 3, 23)
    assert formatter.from_datetime(date_) == "23rd March 1996"


def test_from_datetime_27th():
    date_ = datetime(1995, 10, 27)
    assert formatter.from_datetime(date_) == "27th October 1995"


def test_from_datetime_30th():
    date_ = datetime(1994, 6, 30)
    assert formatter.from_datetime(date_) == "30th June 1994"


def test_from_datetime_31st():
    date_ = datetime(2010, 1, 31)
    assert formatter.from_datetime(date_) == "31st January 2010"


def test_from_datetime_leapyear():
    date_ = datetime(2020, 2, 29)
    assert formatter.from_datetime(date_) == "29th February 2020"


# Test Invalid dates
def test_from_datetime_invalid_leapyear():
    with pytest.raises(ValueError):
        date_ = datetime(2021, 2, 29)


# Invalid argument types
def test_from_datetime_int():
    with pytest.raises(TypeError):
        date_ = 3
        formatter.from_datetime(date_)


def test_from_datetime_str():
    with pytest.raises(TypeError):
        date_ = "4"
        formatter.from_datetime(date_)


def test_from_datetime_str_yyyyddmm():
    with pytest.raises(TypeError):
        date_ = "2020-12-12"
        formatter.from_datetime(date_)
