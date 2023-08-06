"""Some common functions for HTTP requests used by all API modules"""
import threading
from logging import getLogger
from os import getenv
from typing import Dict
from unittest.mock import Mock
from warnings import warn

import forge
from pyrate_limiter import Duration, Limiter, RequestRate
from requests import PreparedRequest, Request, Response, Session
from requests_cache import CachedSession

import pyinaturalist
from pyinaturalist.constants import (
    CACHE_EXPIRATION,
    CACHE_FILE,
    MAX_DELAY,
    REQUEST_BURST_RATE,
    REQUESTS_PER_DAY,
    REQUESTS_PER_MINUTE,
    REQUESTS_PER_SECOND,
    WRITE_HTTP_METHODS,
    FileOrPath,
    MultiInt,
    RequestParams,
)
from pyinaturalist.converters import ensure_file_obj
from pyinaturalist.formatters import format_request
from pyinaturalist.request_params import (
    convert_url_ids,
    preprocess_request_body,
    preprocess_request_params,
)

# Mock response content to return in dry-run mode
MOCK_RESPONSE = Mock(spec=Response)
MOCK_RESPONSE.json.return_value = {'results': [], 'total_results': 0, 'access_token': ''}

logger = getLogger('pyinaturalist')
thread_local = threading.local()


def get_limiter(
    per_second: int = REQUESTS_PER_SECOND,
    per_minute: int = REQUESTS_PER_MINUTE,
    burst: int = REQUEST_BURST_RATE,
) -> Limiter:
    """Get a rate-limiter, optionally with modified rate limits

    Args:
        per_second: Max number of requests per second
        per_minute: Max number of requests per minute
        burst: Max number of consecutive requests allowed before applying rate-limiting delays
    """
    return Limiter(
        RequestRate(per_second * burst, Duration.SECOND * burst),
        RequestRate(per_minute, Duration.MINUTE),
        RequestRate(REQUESTS_PER_DAY, Duration.DAY),
    )


RATE_LIMITER = get_limiter()


def request(
    method: str,
    url: str,
    access_token: str = None,
    dry_run: bool = False,
    files: FileOrPath = None,
    headers: Dict = None,
    ids: MultiInt = None,
    json: Dict = None,
    limiter: Limiter = None,
    session: Session = None,
    raise_for_status: bool = True,
    timeout: float = 5,
    user_agent: str = None,
    **params: RequestParams,
) -> Response:
    """Wrapper around :py:func:`requests.request` with additional options specific to iNat API requests

    Args:
        method: HTTP method
        url: Request URL
        access_token: access_token: the access token, as returned by :func:`get_access_token()`
        dry_run: Just log the request instead of sending a real request
        files: File path or object to upload
        headers: Request headers
        ids: One or more integer IDs used as REST resource(s) to request
        json: JSON request body
        limiter: Custom rate limits to apply to this request
        session: An existing Session object to use instead of creating a new one
        timeout: Time (in seconds) to wait for a response from the server; if exceeded, a
            :py:exc:`requests.exceptions.Timeout` will be raised.
        user_agent: A custom user-agent string to provide to the iNaturalist API
        params: All other keyword arguments are interpreted as request parameters

    Returns:
        API response
    """
    request = prepare_request(
        method=method,
        url=url,
        access_token=access_token,
        files=files,
        headers=headers,
        ids=ids,
        json=json,
        params=params,
        user_agent=user_agent,
    )
    bucket = request.headers.get('User-Agent') or 'pyinaturalist'
    limiter = limiter or RATE_LIMITER
    session = session or get_session()

    logger.info(format_request(request))
    # Make a mock request, if specified
    if dry_run or is_dry_run_enabled(method):
        return MOCK_RESPONSE
    # Otherwise, apply rate-limiting and send the request
    else:
        with limiter.ratelimit(bucket, delay=True, max_delay=MAX_DELAY):
            response = session.send(request, timeout=timeout)
        if raise_for_status:
            response.raise_for_status()
        return response


def prepare_request(
    method: str,
    url: str,
    access_token: str = None,
    files: FileOrPath = None,
    headers: Dict = None,
    ids: MultiInt = None,
    json: Dict = None,
    params: RequestParams = None,
    user_agent: str = None,
    **kwargs,
) -> PreparedRequest:
    """Translate ``pyinaturalist``-specific options into standard request arguments."""
    # Prepare request params and URL
    params = preprocess_request_params(params)
    url = convert_url_ids(url, ids)

    # Prepare user-agent and authentication headers
    headers = headers or {}
    headers['User-Agent'] = user_agent or pyinaturalist.user_agent
    headers['Accept'] = 'application/json'
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'

    # Convert any datetimes to strings in request body
    if json:
        headers['Content-type'] = 'application/json'
        json = preprocess_request_body(json)

    # Read any files for uploading
    if files:
        files = {'file': ensure_file_obj(files)}  # type: ignore

    request = Request(
        method=method, url=url, files=files, headers=headers, json=json, params=params, **kwargs
    )
    return request.prepare()


@forge.copy(request, exclude='method')
def delete(url: str, **kwargs) -> Response:
    """Wrapper around :py:func:`requests.delete` with additional options specific to iNat API requests"""
    return request('DELETE', url, **kwargs)


@forge.copy(request, exclude='method')
def get(url: str, **kwargs) -> Response:
    """Wrapper around :py:func:`requests.get` with additional options specific to iNat API requests"""
    return request('GET', url, **kwargs)


@forge.copy(request, exclude='method')
def post(url: str, **kwargs) -> Response:
    """Wrapper around :py:func:`requests.post` with additional options specific to iNat API requests"""
    return request('POST', url, **kwargs)


@forge.copy(request, exclude='method')
def put(url: str, **kwargs) -> Response:
    """Wrapper around :py:func:`requests.put` with additional options specific to iNat API requests"""
    return request('PUT', url, **kwargs)


def get_session(cache: bool = True) -> Session:
    """Get a Session object with default settings. This will be reused across requests to take
    advantage of connection pooling and (optionally) caching. If used in a multi-threaded context
    (for example, a :py:class:`~concurrent.futures.ThreadPoolExecutor`), a separate session is used
    for each thread.
    """
    if not hasattr(thread_local, 'session'):
        if cache:
            thread_local.session = CachedSession(
                CACHE_FILE,
                backend='sqlite',
                ignored_parameters=['access_token'],
                old_data_on_error=True,
                urls_expire_after=CACHE_EXPIRATION,  # type: ignore  # False positive; can't reproduce locally
            )
        else:
            thread_local.session = Session()
    return thread_local.session


# TODO: Drop support for global variables in version 0.16
def is_dry_run_enabled(method: str) -> bool:
    """A wrapper to determine if dry-run (aka test mode) has been enabled via either
    a constant or an environment variable. Dry-run mode may be enabled for either write
    requests, or all requests.
    """
    if pyinaturalist.DRY_RUN_ENABLED or pyinaturalist.DRY_RUN_WRITE_ONLY:
        msg = (
            'Global varibale usage is deprecated; please use environment variables or dry_run '
            'keyword argument instead'
        )
        warn(DeprecationWarning(msg))

    dry_run_enabled = pyinaturalist.DRY_RUN_ENABLED or env_to_bool('DRY_RUN_ENABLED')
    if method in WRITE_HTTP_METHODS:
        return dry_run_enabled or pyinaturalist.DRY_RUN_WRITE_ONLY or env_to_bool('DRY_RUN_WRITE_ONLY')
    return dry_run_enabled


def env_to_bool(environment_variable: str) -> bool:
    """Translate an environment variable to a boolean value, accounting for minor
    variations (case, None vs. False, etc.)
    """
    env_value = getenv(environment_variable)
    return bool(env_value) and str(env_value).lower() not in ['false', 'none']
