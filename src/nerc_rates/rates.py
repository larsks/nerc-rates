from datetime import date, datetime

import requests
import yaml

DEFAULT_URL = "https://raw.githubusercontent.com/knikolla/nerc-rates/main/rates.yaml"


class Rates:
    def __init__(self, config):
        self.values = {x["name"]: x for x in config}

    @staticmethod
    def _parse_date(d: str | date) -> date:
        if isinstance(d, str):
            d = datetime.strptime(d, "%Y-%m").date()
        return d

    def get_value_at(self, name: str, queried_date: date | str):
        d = self._parse_date(queried_date)
        for v_dict in self.values[name]["history"]:
            v_from = self._parse_date(v_dict["from"])
            v_until = self._parse_date(v_dict.get("until", d))
            if v_from <= d <= v_until:
                return v_dict["value"]

        raise ValueError(f"No value for {name} for {queried_date}.")


def load_from_url(url=DEFAULT_URL) -> Rates:
    r = requests.get(url, allow_redirects=True)
    # Using the BaseLoader prevents conversion of numeric
    # values to floats and loads them as strings.
    config = yaml.load(r.content.decode("utf-8"), Loader=yaml.BaseLoader)
    return Rates(config)


def load_from_file() -> Rates:
    with open("rates.yaml", "r") as f:
        # Using the BaseLoader prevents conversion of numeric
        # values to floats and loads them as strings.
        config = yaml.load(f, Loader=yaml.BaseLoader)
    return Rates(config)
