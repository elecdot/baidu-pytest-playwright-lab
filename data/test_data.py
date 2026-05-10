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

KNOWN_SEARCH_RESULT_PAGES = {
    "北京大学": "https://map.baidu.com/search/%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6/@12931654.56,4855939.47,12z?querytype=s&da_src=shareurl&wd=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6&c=131&src=0&pn=0&sug=0&l=12&b=(12918278.56,4802307.47;13000198.56,4848387.47)&from=webmap&biz_forward=%7B%22scaler%22:1,%22styles%22:%22pl%22%7D&device_ratio=1",
}

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
