import webbrowser

SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
}


def open_website(name: str) -> str:
    """Открывает сайт в браузере.

    Args:
        name: Название сайта: google, youtube или github.
    """
    url = SITES.get(name.lower())

    if url is None:
        return f"Сайт {name} не поддерживается."

    success = webbrowser.open(url)

    if success:
        return f"Запрошено открытие сайта {name}."

    return "Не удалось открыть браузер."