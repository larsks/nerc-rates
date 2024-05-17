from typing import Annotated, Self

import datetime
import pydantic


class Base(pydantic.BaseModel):
    pass


def parse_date(v: str | datetime.date) -> datetime.date:
    if isinstance(v, str):
        return datetime.datetime.strptime(v, "%Y-%m").date()
    return v


DateField = Annotated[datetime.date, pydantic.BeforeValidator(parse_date)]


class RateValue(Base):
    value: str
    date_from: Annotated[DateField, pydantic.Field(alias="from")]
    date_until: Annotated[DateField, pydantic.Field(alias="until", default=None)]

    @pydantic.model_validator(mode="after")
    @classmethod
    def validate_date_range(cls, data: Self):
        if data.date_until and data.date_until < data.date_from:
            raise ValueError("date_until must be after date_from")
        return data


class RateItem(Base):
    name: str
    history: list[RateValue]


RateItemDict = Annotated[
    dict[str, RateItem],
    pydantic.BeforeValidator(lambda items: {x["name"]: x for x in items}),
]


class Rates(pydantic.RootModel):
    root: RateItemDict

    def __getitem__(self, item):
        return self.root[item]

    def get_value_at(self, name: str, queried_date: datetime.date | str):
        d = parse_date(queried_date)
        for item in self.root[name].history:
            if item.date_from <= d <= (item.date_until or d):
                return item.value

        raise ValueError(f"No value for {name} for {queried_date}.")
