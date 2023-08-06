# Weather plugin

This plugin connects to weather server and retrieves weather information.

# Configuration

First you need to configure what type of temperature you need. Either in Celsius (MATRIC) of Fahrenheit (IMPERIAL)

Example of configuration.
```json
{
  "system": "METRIC"
}
```

# Payload

Plugin takes a payload in form of:

```json
{
  "city": "profile@traits.public.city"
}
```

Where the value can be a path as dotted notation to city name or a string with city name:

```json
{
  "city": "Paris"
}
```