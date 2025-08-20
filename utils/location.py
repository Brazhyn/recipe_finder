import requests


def get_user_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_user_location_by_ip(ip: str) -> str:
    default_location = "50.4501,30.5234"
    url = f"http://ip-api.com/json/{ip}"
    if ip in ("127.0.0.1", "::1", None):
        return default_location

    try:
        response = requests.get(url=url)
        response.raise_for_status()
        data = response.json()

        lat = str(data.get("lat"))
        lon = str(data.get("lon"))
        location = lat + "," + lon

        if lat is None or lon is None:
            return default_location

        return location

    except requests.RequestException:
        return default_location
