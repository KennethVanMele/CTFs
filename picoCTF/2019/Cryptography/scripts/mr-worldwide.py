import requests, re, time

flag = "picoCTF{(35.028309, 135.753082)(46.469391, 30.740883)(39.758949, -84.191605)(41.015137, 28.979530)(24.466667, 54.366669)(3.140853, 101.693207)(9.005401, 38.763611)(-3.989038, -79.203560)(52.377956, 4.897070)(41.085651, -73.858467)(57.790001, -152.407227)(31.205753, 29.924526)} "


def get_letter_from_coordinate(match):
    lat = match.group(1)
    long = match.group(2)
    time.sleep(3)
    r = requests.get("https://geocode.xyz/{},{}?json=1".format(lat, long))
    time.sleep(3)
    j = r.json()
    time.sleep(3)
    print(j)
    time.sleep(3)
    return j['geocode']


time.sleep(3)
print(re.sub(r'\(([\d\.-]+), ([\d\.-]+)\)', get_letter_from_coordinate, flag))
