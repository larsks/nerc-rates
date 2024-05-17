import pytest
import requests_mock

from nerc_rates import load_from_url, rates


def test_load_from_url():
    mock_response_text = """
    - name: CPU SU Rate
      history:
        - value: "0.013"
          from: 2023-06
    """
    with requests_mock.Mocker() as m:
        m.get(rates.DEFAULT_URL, text=mock_response_text)
        r = load_from_url()
        assert r.get_value_at("CPU SU Rate", "2023-06") == "0.013"


def test_invalid_dates():
    mock_response_text = """
    - name: CPU SU Rate
      history:
        - value: "0.013"
          from: 2023-06
          until: 2023-04
    """
    with requests_mock.Mocker() as m:
        m.get(rates.DEFAULT_URL, text=mock_response_text)
        with pytest.raises(ValueError):
            load_from_url()


def test_rates_get_value_at():
    r = rates.Rates(
        [
            {
                "name": "Test Rate",
                "history": [
                    {"value": "1", "from": "2020-01", "until": "2020-12"},
                    {"value": "2", "from": "2021-01"},
                ],
            }
        ]
    )
    assert r.get_value_at("Test Rate", "2020-01") == "1"
    assert r.get_value_at("Test Rate", "2020-12") == "1"
    assert r.get_value_at("Test Rate", "2021-01") == "2"
    with pytest.raises(ValueError):
        assert r.get_value_at("Test Rate", "2019-01")
