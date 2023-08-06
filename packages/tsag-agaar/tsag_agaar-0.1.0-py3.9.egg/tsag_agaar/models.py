import dataclasses
import datetime
from tsag_agaar.util import recursive_dict
import lxml.etree
from tsag_agaar.constants import DATE_FORMAT, WEATHER_ENDPOINT
import typing
import requests


class BaseModel:
    def to_json(self):
        return recursive_dict(self)


@dataclasses.dataclass
class Forecast(BaseModel):
    date: datetime.datetime
    temp_night: int
    temp_day: int
    pheno_id_night: int
    pheno_night: str
    pheno_id_day: str
    pheno_day: str
    wind_night: int
    wind_day: int


def unpack_forecast(node, **kwargs) -> typing.Iterator[Forecast]:
    filter_date = kwargs.get("date")

    for forecast in node.xpath("weather"):
        (
            date,
            temp_night,
            temp_day,
            pheno_id_night,
            pheno_night,
            pheno_id_day,
            pheno_day,
            wind_night,
            wind_day,
        ) = forecast.iterchildren()

        if filter_date is None or filter_date == date.text:
            yield Forecast(
                datetime.datetime.strptime(date.text, DATE_FORMAT),
                int(temp_night.text),
                int(temp_day.text),
                int(pheno_id_night.text),
                pheno_night.text,
                int(pheno_id_day.text),
                pheno_day.text,
                int(wind_night.text),
                int(wind_day.text),
            )


def unpack_city(node, **kwargs):
    iterate_over_forecasts = kwargs.get("iterate_over_forecasts")
    city, data = node.iterchildren()

    if iterate_over_forecasts:
        return City(city.text, [*unpack_forecast(data, **kwargs)])

    return City(city.text, unpack_forecast(data, **kwargs))


@dataclasses.dataclass
class City(BaseModel):
    name: str
    forecasts: typing.Iterator[Forecast]


@dataclasses.dataclass
class QueryResult(BaseModel):
    data: typing.Union[any, None]
    error: typing.Union[str, Exception, None]
    query: "Query"
    ok: bool

    def retry(self):
        return self.query.run()

    def to_json(self):
        return recursive_dict(self)


@dataclasses.dataclass
class Query(BaseModel):
    city: typing.Optional[str] = None
    date: typing.Optional[typing.Union[datetime.datetime, str]] = None

    def run(self, iterate_over_forecasts=False):
        date = (
            datetime.datetime.strftime(self.date, DATE_FORMAT)
            if isinstance(self.date, datetime.datetime)
            else self.date
        )

        req = requests.get(WEATHER_ENDPOINT)

        if not req.ok:
            return QueryResult(
                None, "request returned code %d" % req.status_code, query=self, ok=False
            )

        doc = lxml.etree.fromstring(req.content)

        return QueryResult(
            data=[
                unpack_city(
                    city,
                    date=(self.date if self.date is None else date),
                    iterate_over_forecasts=iterate_over_forecasts,
                )
                for city in doc.xpath("/xml/forecast5day")
                if self.city is None or city[0].text == self.city
            ],
            error=None,
            query=self,
            ok=True,
        )
