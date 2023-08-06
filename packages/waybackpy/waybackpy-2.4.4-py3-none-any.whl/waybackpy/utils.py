import re
import time
import requests
from datetime import datetime

from .exceptions import WaybackError, URLError, RedirectSaveError
from .__version__ import __version__

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

quote = requests.utils.quote
default_user_agent = "waybackpy python package - https://github.com/akamhy/waybackpy"


def _latest_version(package_name, headers):
    """Returns the latest version of package_name.

    Parameters
    ----------
    package_name : str
        The name of the python package

    headers : dict
        Headers that will be used while making get requests

    Return type is str

    Use API <https://pypi.org/pypi/> to get the latest version of
    waybackpy, but can be used to get latest version of any package
    on PyPi.
    """

    request_url = "https://pypi.org/pypi/" + package_name + "/json"
    response = _get_response(request_url, headers=headers)
    data = response.json()
    return data["info"]["version"]


def _unix_timestamp_to_wayback_timestamp(unix_timestamp):
    """Returns unix timestamp converted to datetime.datetime

    Parameters
    ----------
    unix_timestamp : str, int or float
        Unix-timestamp that needs to be converted to datetime.datetime

    Converts and returns input unix_timestamp to datetime.datetime object.
    Does not matter if unix_timestamp is str, float or int.
    """

    return datetime.utcfromtimestamp(int(unix_timestamp)).strftime("%Y%m%d%H%M%S")


def _add_payload(instance, payload):
    """Adds payload from instance that can be used to make get requests.

    Parameters
    ----------
    instance : waybackpy.cdx.Cdx
        instance of the Cdx class

    payload : dict
        A dict onto which we need to add keys and values based on instance.

    instance is object of Cdx class and it contains the data required to fill
    the payload dictionary.
    """

    if instance.start_timestamp:
        payload["from"] = instance.start_timestamp

    if instance.end_timestamp:
        payload["to"] = instance.end_timestamp

    if instance.gzip != True:
        payload["gzip"] = "false"

    if instance.match_type:
        payload["matchType"] = instance.match_type

    if instance.filters and len(instance.filters) > 0:
        for i, f in enumerate(instance.filters):
            payload["filter" + str(i)] = f

    if instance.collapses and len(instance.collapses) > 0:
        for i, f in enumerate(instance.collapses):
            payload["collapse" + str(i)] = f

    # Don't need to return anything as it's dictionary.
    payload["url"] = instance.url


def _timestamp_manager(timestamp, data):
    """Returns the timestamp.

    Parameters
    ----------
    timestamp : datetime.datetime
        datetime object

    data : dict
        A python dictionary, which is loaded JSON os the availability API.

    Return type:
        datetime.datetime

     If timestamp is not None then sets the value to timestamp itself.
     If timestamp is None the returns the value from the last fetched API data.
     If not timestamp and can not read the archived_snapshots form data return datetime.max
    """

    if timestamp:
        return timestamp

    if not data["archived_snapshots"]:
        return datetime.max

    return datetime.strptime(
        data["archived_snapshots"]["closest"]["timestamp"], "%Y%m%d%H%M%S"
    )


def _check_match_type(match_type, url):
    """Checks the validity of match_type parameter of the CDX GET requests.

    Parameters
    ----------
    match_type : list
        list  that may contain any or all from  ["exact", "prefix", "host", "domain"]
        See https://github.com/akamhy/waybackpy/wiki/Python-package-docs#url-match-scope

    url : str
        The URL used to create the waybackpy Url object.

    If not vaild match_type raise Exception.

    """

    if not match_type:
        return

    if "*" in url:
        raise WaybackError("Can not use wildcard with match_type argument")

    legal_match_type = ["exact", "prefix", "host", "domain"]

    if match_type not in legal_match_type:
        exc_message = "{match_type} is not an allowed match type.\nUse one from 'exact', 'prefix', 'host' or 'domain'".format(
            match_type=match_type
        )
        raise WaybackError(exc_message)


def _check_collapses(collapses):
    """Checks the validity of collapse parameter of the CDX GET request.

    One or more field or field:N to 'collapses=[]' where
    field is one of (urlkey, timestamp, original, mimetype, statuscode,
    digest and length) and N is the first N characters of field to test.

    Parameters
    ----------
    collapses : list

    If not vaild collapses raise Exception.

    """

    if not isinstance(collapses, list):
        raise WaybackError("collapses must be a list.")

    if len(collapses) == 0:
        return

    for collapse in collapses:
        try:
            match = re.search(
                r"(urlkey|timestamp|original|mimetype|statuscode|digest|length)(:?[0-9]{1,99})?",
                collapse,
            )
            field = match.group(1)

            N = None
            if 2 == len(match.groups()):
                N = match.group(2)

            if N:
                if not (field + N == collapse):
                    raise Exception
            else:
                if not (field == collapse):
                    raise Exception

        except Exception:
            exc_message = "collapse argument '{collapse}' is not following the cdx collapse syntax.".format(
                collapse=collapse
            )
            raise WaybackError(exc_message)


def _check_filters(filters):
    """Checks the validity of filter parameter of the CDX GET request.

    Any number of filter params of the following form may be specified:
        filters=["[!]field:regex"] may be specified..

    Parameters
    ----------
    filters : list

    If not vaild filters raise Exception.

    """

    if not isinstance(filters, list):
        raise WaybackError("filters must be a list.")

    # [!]field:regex
    for _filter in filters:
        try:

            match = re.search(
                r"(\!?(?:urlkey|timestamp|original|mimetype|statuscode|digest|length)):(.*)",
                _filter,
            )

            key = match.group(1)
            val = match.group(2)

        except Exception:

            exc_message = (
                "Filter '{_filter}' is not following the cdx filter syntax.".format(
                    _filter=_filter
                )
            )
            raise WaybackError(exc_message)


def _cleaned_url(url):
    """Sanatize the url
    Remove and replace illegal whitespace characters from the URL.
    """
    return str(url).strip().replace(" ", "%20")


def _url_check(url):
    """
    Check for common URL problems.
    What we are checking:
    1) '.' in self.url, no url that ain't '.' in it.

    If you known any others, please create a PR on the github repo.
    """

    if "." not in url:
        exc_message = "'{url}' is not a vaild URL.".format(url=url)
        raise URLError(exc_message)


def _full_url(endpoint, params):
    """API endpoint + GET parameters = full_url

    Parameters
    ----------
    endpoint : str
        The API endpoint

    params : dict
        Dictionary that has name-value pairs.

    Return type is str

    """

    if not params:
        return endpoint

    full_url = endpoint if endpoint.endswith("?") else (endpoint + "?")
    for key, val in params.items():
        key = "filter" if key.startswith("filter") else key
        key = "collapse" if key.startswith("collapse") else key
        amp = "" if full_url.endswith("?") else "&"
        full_url = full_url + amp + "{key}={val}".format(key=key, val=quote(str(val)))
    return full_url


def _get_total_pages(url, user_agent):
    """
    If showNumPages is passed in cdx API, it returns
    'number of archive pages'and each page has many archives.

    This func returns number of pages of archives (type int).
    """
    total_pages_url = (
        "https://web.archive.org/cdx/search/cdx?url={url}&showNumPages=true".format(
            url=url
        )
    )
    headers = {"User-Agent": user_agent}
    return int((_get_response(total_pages_url, headers=headers).text).strip())


def _archive_url_parser(
    header, url, latest_version=__version__, instance=None, response=None
):
    """Returns the archive after parsing it from the response header.

    Parameters
    ----------
    header : str
        The response header of WayBack Machine's Save API

    url : str
        The input url, the one used to created the Url object.

    latest_version : str
        The latest version of waybackpy (default is __version__)

    instance : waybackpy.wrapper.Url
        Instance of Url class


    The wayback machine's save API doesn't
    return JSON response, we are required
    to read the header of the API response
    and find the archive URL.

    This method has some regular expressions
    that are used to search for the archive url
    in the response header of Save API.

    Two cases are possible:
    1) Either we find the archive url in
       the header.

    2) Or we didn't find the archive url in
       API header.

    If we found the archive URL we return it.

    Return format:
    web.archive.org/web/<TIMESTAMP>/<URL>

    And if we couldn't find it, we raise
    WaybackError with an error message.
    """

    if "save redirected" in header and instance:
        time.sleep(60)  # makeup for archive time

        now = datetime.utcnow().timetuple()
        timestamp = _wayback_timestamp(
            year=now.tm_year,
            month=now.tm_mon,
            day=now.tm_mday,
            hour=now.tm_hour,
            minute=now.tm_min,
        )

        return_str = "web.archive.org/web/{timestamp}/{url}".format(
            timestamp=timestamp, url=url
        )
        url = "https://" + return_str

        headers = {"User-Agent": instance.user_agent}

        res = _get_response(url, headers=headers)

        if res.status_code < 400:
            return "web.archive.org/web/{timestamp}/{url}".format(
                timestamp=timestamp, url=url
            )

    # Regex1
    m = re.search(r"Content-Location: (/web/[0-9]{14}/.*)", str(header))
    if m:
        return "web.archive.org" + m.group(1)

    # Regex2
    m = re.search(
        r"rel=\"memento.*?(web\.archive\.org/web/[0-9]{14}/.*?)>", str(header)
    )
    if m:
        return m.group(1)

    # Regex3
    m = re.search(r"X-Cache-Key:\shttps(.*)[A-Z]{2}", str(header))
    if m:
        return m.group(1)

    if response:
        if response.url:
            if "web.archive.org/web" in response.url:
                m = re.search(
                    r"web\.archive\.org/web/(?:[0-9]*?)/(?:.*)$",
                    str(response.url).strip(),
                )
                if m:
                    return m.group(0)

    if instance:
        newest_archive = None
        try:
            newest_archive = instance.newest()
        except WaybackError:
            pass  # We don't care as this is a save request

        if newest_archive:
            minutes_old = (
                datetime.utcnow() - newest_archive.timestamp
            ).total_seconds() / 60.0

            if minutes_old <= 30:
                archive_url = newest_archive.archive_url
                m = re.search(r"web\.archive\.org/web/[0-9]{14}/.*", archive_url)
                if m:
                    instance.cached_save = True
                    return m.group(0)

    if __version__ == latest_version:
        exc_message = (
            "No archive URL found in the API response. "
            "If '{url}' can be accessed via your web browser then either "
            "Wayback Machine is malfunctioning or it refused to archive your URL."
            "\nHeader:\n{header}".format(url=url, header=header)
        )

        if "save redirected" == header.strip():
            raise RedirectSaveError(
                "URL cannot be archived by wayback machine as it is a redirect.\nHeader:\n{header}".format(
                    header=header
                )
            )
    else:
        exc_message = (
            "No archive URL found in the API response. "
            "If '{url}' can be accessed via your web browser then either "
            "this version of waybackpy ({version}) is out of date or WayBack "
            "Machine is malfunctioning. Visit 'https://github.com/akamhy/waybackpy' "
            "for the latest version of waybackpy.\nHeader:\n{header}".format(
                url=url, version=__version__, header=header
            )
        )

    raise WaybackError(exc_message)


def _wayback_timestamp(**kwargs):
    """Returns a valid waybackpy timestamp.

    The standard archive URL format is
    https://web.archive.org/web/20191214041711/https://www.youtube.com

    If we break it down in three parts:
    1 ) The start (https://web.archive.org/web/)
    2 ) timestamp (20191214041711)
    3 ) https://www.youtube.com, the original URL


    The near method of Url class in wrapper.py takes year, month, day, hour
    and minute as arguments, their type is int.

    This method takes those integers and converts it to
    wayback machine timestamp and returns it.


    zfill(2) adds 1 zero in front of single digit days, months hour etc.

    Return type is string.
    """

    return "".join(
        str(kwargs[key]).zfill(2) for key in ["year", "month", "day", "hour", "minute"]
    )


def _get_response(
    endpoint,
    params=None,
    headers=None,
    return_full_url=False,
    retries=5,
    backoff_factor=0.5,
    no_raise_on_redirects=False,
):
    """Makes get requests.

    Parameters
    ----------
    endpoint : str
        The API endpoint.

    params : dict
        The get request parameters. (default is None)

    headers : dict
        Headers for the get request. (default is None)

    return_full_url : bool
        Determines whether the call went full url returned along with the
        response. (default is False)

    retries : int
        Maximum number of retries for the get request. (default is 5)

    backoff_factor : float
        The factor by which we determine the next retry time after wait.
        https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
        (default is 0.5)

    no_raise_on_redirects : bool
        If maximum 30(default for requests) times redirected than instead of
        exceptions return. (default is False)


    To handle WaybackError:
    from waybackpy.exceptions import WaybackError

    try:
        ...
    except WaybackError as e:
        # handle it
    """

    # From https://stackoverflow.com/a/35504626
    # By https://stackoverflow.com/users/401467/datashaman

    s = requests.Session()

    retries = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )

    s.mount("https://", HTTPAdapter(max_retries=retries))

    # The URL with parameters required for the get request
    url = _full_url(endpoint, params)

    try:

        if not return_full_url:
            return s.get(url, headers=headers)

        return (url, s.get(url, headers=headers))

    except Exception as e:

        reason = str(e)

        if no_raise_on_redirects:
            if "Exceeded 30 redirects" in reason:
                return

        exc_message = "Error while retrieving {url}.\n{reason}".format(
            url=url, reason=reason
        )

        exc = WaybackError(exc_message)
        exc.__cause__ = e
        raise exc
