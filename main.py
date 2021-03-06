#!/usr/bin/python
import random
import requests
import uuid
import json


def clean_ascii(text):
    result = ''.join([i if ord(i) < 128 else ' ' for i in text])
    return result.strip()


def clean_numeric(s):
    return int(''.join(i for i in s if i.isdigit()))


http_proxies = [
    "http://58.242.145.227:8080",
    "http://101.66.253.22:8080",
    "http://209.66.193.186:8080",
    "http://101.26.38.162:80",
    "http://123.7.88.171:3128",
    "http://50.207.44.18:3128",
    "http://117.169.14.81:8080",
    "http://177.133.140.243:3128",
    "http://122.4.244.121:80",
    "http://199.115.114.38:80",
]


def get_cars(page):
    identifier = uuid.uuid4()

    params = {
        'CatID': 1,
        'Auto': 0.0,
        'SubModelID': 247.0,
        'SubCatID': 1,
        'ModelID': 28.0,
        'FromPrice': 26000,
        'ToPrice': 35000,
        'FromYear': 2009.0,
        'AppType': 'Android',
        'AppVersion': 2.9,
        'DeviceType': 'Nexus 5',
        'udid': identifier,
        'OSVersion': 5.1,
        'Page': page
    }

    http_proxy = random.choice(http_proxies)

    proxy_dict = {
        "http": http_proxy
    }

    headers = {
        'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)'
    }

    r = requests.get('http://m.yad2.co.il/API/MadorResults.php', params=params, headers=headers, proxies=proxy_dict)

    try:
        data = r.json()
    except:
        print r.text
        raise

    private_cars = data['Private']['Results']
    for item in private_cars:

        car_id = clean_ascii(item.get('RecordID', ''))

        if not car_id:
            continue

        price = clean_ascii(item['Line3'])
        price = clean_numeric(price)
        raw = item['Line2']

        raw = raw.encode('ascii', 'ignore')
        raw = clean_ascii(raw)
        raw = ''.join(raw.split())
        raw = raw.split(',:')
        hand = clean_numeric(raw[0])
        year = clean_numeric(raw[1])

        car_link = 'http://www.yad2.co.il/Cars/Car_info.php?CarID={car_id}'.format(car_id=car_id)

        yield car_id, price, hand, year, car_link

        # Sleep placed for avoiding load on their servers
        # time.sleep(0.3)


def main():
    try:
        with open('.data') as f:
            raw = f.read()
            data = json.loads(raw)
    except:
        data = {}

    for car_id, price, hand, year, url in get_cars(1):
        item = data.get(car_id, {})
        prev_max_price = item.get('max_price', price)
        prev_min_price = item.get('min_price', price)

        item['price'] = price
        item['max_price'] = max(prev_max_price, price)
        item['min_price'] = min(prev_min_price, price)
        item['hand'] = hand
        item['year'] = year
        item['url'] = url

        data[car_id] = item

    with open('.data', "w+") as w:
        raw = json.dumps(data, indent=4, sort_keys=True)
        w.write(raw)


if __name__ == "__main__":
    main()
