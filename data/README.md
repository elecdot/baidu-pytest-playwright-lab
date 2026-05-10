# Data

This directory stores reusable test data for parametrized pytest cases.
Data should be small, readable, and safe for repeated low-volume testing against
the public Baidu Map Web application.

## Planned Files

- `test_data.py` for search keywords, invalid inputs, route cases, and mocked
  geolocation coordinates.

## Conventions

- Keep test data deterministic and human-readable.
- Prefer public, well-known places for search and route scenarios.
- Do not add private addresses, account data, secrets, cookies, or scraped map
  data.
- Separate valid, invalid, route, and geolocation data into named constants.
- Add comments only when a data value needs context, such as why a coordinate or
  keyword was chosen.

## Initial Data Groups

- `SEARCH_KEYWORDS`
- `INVALID_KEYWORDS`
- `ROUTE_CASES`
- `GEO_LOCATIONS`
