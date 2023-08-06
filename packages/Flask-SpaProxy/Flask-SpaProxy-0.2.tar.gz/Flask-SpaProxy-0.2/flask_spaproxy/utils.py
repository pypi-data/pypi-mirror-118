def is_url_for_file(url: str) -> bool:
    splitted_url = url.split('/')
    last_part = splitted_url[-1]
    return "." in last_part
