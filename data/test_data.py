"""Shared test data for the Baidu Map automation lab."""

SEARCH_KEYWORDS = [
    "天安门广场",
    "北京大学",
    "清华大学",
    "北京南站",
    "上海虹桥站",
    "咖啡",
    "医院",
    "银行",
]

INVALID_KEYWORDS = [
    "",
    "@@@###",
    "abcdefg不存在地点12345",
]

ROUTE_CASES = [
    {
        "name": "beijing_south_to_tiananmen",
        "start": "北京南站",
        "end": "天安门广场",
    },
    {
        "name": "pku_to_tsinghua",
        "start": "北京大学",
        "end": "清华大学",
    },
    {
        "name": "shanghai_hongqiao_to_oriental_pearl",
        "start": "上海虹桥站",
        "end": "东方明珠",
    },
]

# Coordinates are public city-center examples used only for browser geolocation
# simulation, not for validating map data accuracy.
GEO_LOCATIONS = {
    "beijing": {
        "longitude": 116.397128,
        "latitude": 39.916527,
    },
    "shanghai": {
        "longitude": 121.475190,
        "latitude": 31.228833,
    },
    "guangzhou": {
        "longitude": 113.324520,
        "latitude": 23.119160,
    },
}
