from .dynamic_explorer import inspect_dynamic
from .static_explorer import inspect_static
from .online_file_explorer import inspect_file
from .page_type import decide_sd, is_document_url


def inspect_page(url, static, log_file, query, primary_key, primary_key_val, col, given_info, client):
    """Explore a single page.

    ``static`` is the already-known page type when we are revisiting a cached
    source (None means: classify it now with decide_sd).  Returns the page type
    alongside the result so callers can cache it.
    """
    if is_document_url(url):
        given_info = inspect_file(url, query, primary_key, primary_key_val, col, client, given_info, log_file)
        return given_info, [], True, url, {}, True

    if static is None:
        # decide_sd returns (is_static, base_url); a bare tuple is always truthy,
        # so it has to be unpacked or the dynamic branch is unreachable.
        static, _base_url = decide_sd(url, query, primary_key, primary_key_val, col, given_info, client, log_file)

    if static:
        given_info, next_level_links, proceed, source_url, path_record_level = inspect_static(url, query, primary_key, primary_key_val, col, client, given_info, log_file)
    else:
        given_info, next_level_links, proceed, source_url, path_record_level = inspect_dynamic(url, query, primary_key, primary_key_val, col, given_info, client, log_file)

    return given_info, next_level_links, proceed, source_url, path_record_level, static