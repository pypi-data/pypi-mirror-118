import asyncio
from tracardi.domain.profile import Profile

from tracardi_weather.plugin import WeatherAction


async def main():

    init = {
        "system": "metric",
        "city": "Wrocław"
    }

    payload = {}

    plugin = WeatherAction(**init)
    result = await plugin.run(payload)

    print(result)

    # ------------------------------

    init = {
        "system": "metric",
        "city": "profile@traits.public.city"
    }

    payload = {}

    plugin = WeatherAction(**init)

    plugin.profile = Profile(id="1")
    plugin.profile.traits.public['city'] = "Paris"

    result = await plugin.run(payload)

    print(result)


asyncio.run(main())
