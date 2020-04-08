from urllib.parse import urlparse, urljoin


def is_safe_url(request, target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    safe = test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
    return safe


def get_endpoint(url):
    o = urlparse(url)
    return o.path
