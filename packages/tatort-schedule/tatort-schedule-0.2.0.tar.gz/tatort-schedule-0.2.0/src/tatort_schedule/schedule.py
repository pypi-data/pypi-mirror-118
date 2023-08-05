import urllib.request
import dateutil.parser
import dateutil.tz
import datetime
from bs4 import BeautifulSoup
from datetime import timedelta

# Global
TATORT_URL = "https://www.daserste.de/unterhaltung/krimi/tatort/vorschau/index.html"


def get_tatort() -> [dict]:
    """
    Returns the current schedule for Tatort.
    """
    website = load_tatort_website()
    return parse_tatort_website(website)


def load_tatort_website() -> str:
    """
    Loads the Tatort schedule webiste defined in TATORT_URL.
    """
    html_file = ""
    with urllib.request.urlopen(TATORT_URL) as response:
        html_file = response.read().decode("utf-8")
    return html_file


def parse_tatort_website(html: str) -> [dict]:
    """
    Parses the given Tatort website and returns an array of dicts, each
    containing a schedule entry for the upcoming Tatort episodes.

    >>> site = open("../../tests/testdata/20210209.html", "r").read()
    >>> schedule = parse_tatort_website(site)
    >>> schedule[0]
    {'title': 'Rettung so nah', 'city': 'Dresden', 'inspectors': 'Gorniak, Winkler und Schnabel', 'time': '2021-02-07T20:15:00+01:00', 'link': 'https://www.daserste.de/unterhaltung/krimi/tatort/sendung/rettung-so-nah-100.html'}
    """
    soup = BeautifulSoup(html, "html.parser")

    # Found linklists:
    # 0:"nächste Erstausstrahlung"
    # 1:"im Ersten"
    # 2:"in den Dritten"
    # 3:"auf ONE"
    # 4:"Tatort in Ihrem dritten Programm"
    tatort_linklists = soup.find_all("div", class_="linklist")

    # Timestamp of website request is between </body> and </html> tag:
    # </body><!-- stage-4.deo @ Sun Feb 07 09:16:08 CET 2021 --></html>
    for line in reversed(soup.html.contents):
        at_index = line.find("@")  # look for comment
        if at_index == -1:
            continue
        else:  # valid line: ' stage-3.deo @ Sun Aug 29 17:40:15 CEST 2021 '
            timestamp_text = line[at_index+2:-1]
            break

    tzmapping = {'CET': dateutil.tz.gettz('Europe/Berlin'),
                 'CEST': dateutil.tz.gettz('Europe/Berlin')}
    try:
        request_timestamp = dateutil.parser.parse(
            timestamp_text, tzinfos=tzmapping)
    except Exception as e:
        request_timestamp = datetime.now()

    tatort_im_ersten_list = tatort_linklists[1].find_all("a")
    schedule_list = []
    for link in tatort_im_ersten_list:
        entry = _parse_row(link.string, request_timestamp)
        entry["link"] = link["href"]
        if not "https://www.daserste.de" in entry["link"]:
            entry["link"] = "https://www.daserste.de" + entry["link"]
        schedule_list.append(entry)
    return schedule_list


def _parse_row(schedule_text: str, request_timestamp: datetime.datetime) -> dict:
    """
    Parses a row in the Tatort schedule, for example:
    >>> entry_string = "So., 14.02. | 20:15 Uhr | Hetzjagd (Odenthal und Stern  (Ludwigshafen))"

    A request timestamp has to be passed into the function, because the first column can contain 'Heute' or 'Morgen' (today and tomorrow respectively)
    >>> request_ts = datetime.datetime(2021, 2, 7, 9, 16, 8, 0, dateutil.tz.gettz('Europe/Berlin'))
    >>> entry = _parse_row(entry_string, request_ts)

    The results are returned in a dictionary:
    >>> entry["time"]
    '2021-02-14T20:15:00+01:00'
    >>> entry["title"]
    'Hetzjagd'
    >>> entry["city"]
    'Ludwigshafen'
    >>> entry["inspectors"]
    'Odenthal und Stern'
    """
    columns = schedule_text.split(" | ")
    entry = _parse_title(columns[2])
    entry["time"] = _parse_datetime(columns[0], columns[1], request_timestamp)
    return entry


def _parse_datetime(date_text: str, time_text: str, request_ts: datetime.datetime) -> datetime.datetime:
    """
    Returns a datetime object containing info from date_text and time_text:

    >>> request_ts = datetime.datetime(2021, 2, 7, 9, 16, 8, 0, dateutil.tz.gettz('Europe/Berlin'))
    >>> _parse_datetime("So., 14.02.", "20:15 Uhr", request_ts)
    '2021-02-14T20:15:00+01:00'

    When the new Tatort episode is coming today, the date of the request
    timestamp is used:
    >>> _parse_datetime("Heute", "20:15 Uhr", request_ts)
    '2021-02-07T20:15:00+01:00'

    Same thing with tomorrow:
    >>> _parse_datetime("Morgen", "20:15 Uhr", request_ts)
    '2021-02-08T20:15:00+01:00'

    During summertime / CEST, the timezone in the timestamp is UTC+2:
    >>> _parse_datetime("So., 11.07.", "20:15 Uhr", request_ts)
    '2021-07-11T20:15:00+02:00'
    """

    if "Heute" in date_text:
        day = int(request_ts.day)
        month = int(request_ts.month)
    elif "Morgen" in date_text:
        tomorrow = request_ts + timedelta(days=1)
        day = int(tomorrow.day)
        month = int(tomorrow.month)
    else:
        date = date_text.split(", ")
        date_split = date[1].split(".")
        day = int(date_split[0])
        month = int(date_split[1])

    hour = int(time_text[0:2])
    minute = int(time_text[3:5])

    return datetime.datetime(2021, month, day, hour, minute, 0, 0, request_ts.tzinfo).isoformat()


def _parse_title(title_text: str) -> dict:
    """
    Parses the title, city and inspector names from the given string:

    >>> title = "Damian (Tobler und Weber  (Schwarzwald))"
    >>> title_infos = _parse_title(title)
    >>> title_infos["title"]
    'Damian'
    >>> title_infos["city"]
    'Schwarzwald'
    >>> title_infos["inspectors"]
    'Tobler und Weber'
    """

    title_info = {}
    title_info["title"] = title_text[:title_text.find("(")-1]

    bracket_text = title_text[title_text.find("(")+1:len(title_text)-1]

    city_text = bracket_text[bracket_text.rfind("(")+1:len(bracket_text)-1]
    title_info["city"] = city_text

    title_info["inspectors"] = bracket_text[:-len(city_text)-4]
    return title_info


if __name__ == "__main__":
    import doctest
    doctest.testmod()
