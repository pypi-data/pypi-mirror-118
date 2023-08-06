from pydantic import BaseModel
from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result

from tracardi_weather.service.weather_client import AsyncWeatherClient


class PluginConfiguration(BaseModel):
    system: str = "metric"
    city: str


class WeatherResult(BaseModel):
    temperature: float = None
    humidity: float = None
    wind_speed: float = None
    description: str = None


class WeatherAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = PluginConfiguration(**kwargs)
        if self.config.system.lower() == 'metric':
            system = "C"
        else:
            system = "F"
        self.client = AsyncWeatherClient(system)

    async def run(self, payload):

        city = self.config.city

        dot = DotAccessor(self.profile, self.session, None, self.event, self.flow)
        city = dot[city]
        result = WeatherResult()

        weather = await self.client.fetch(city)

        result.temperature = weather.current.temperature
        result.humidity = weather.current.humidity
        result.wind_speed = weather.current.wind_speed
        result.description = weather.current.sky_text

        return Result(port="weather", value=result.dict())


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_weather.plugin',
            className='WeatherAction',
            inputs=["payload"],
            outputs=['weather'],
            version='0.1.5',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "system": "METRIC",
                "city": None
            }
        ),
        metadata=MetaData(
            name='Weather service',
            desc='Retrieves weather information.',
            type='flowNode',
            width=200,
            height=100,
            icon='weather',
            group=["Connectors"]
        )
    )
