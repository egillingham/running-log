import urlparse


def is_safe_url(request, target):
    ref_url = urlparse.urlparse(request.host_url)
    test_url = urlparse.urlparse(urlparse.urljoin(request.host_url, target))
    safe = test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
    return safe


def get_endpoint(url):
    o = urlparse.urlparse(url)
    return o.path
