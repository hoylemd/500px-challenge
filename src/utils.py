def make_pager_url(rpp, page, total):
    """Generate a url for a pager link, or None if the link would be invalid"""
    rpp = int(rpp)
    page = int(page)

    if page < 1:
        return None

    if page > total:
        return None

    rpp_section = f"rpp={rpp}" if rpp else ''
    page_section = f"page={page}" if page else ''

    return f"/?{rpp_section}&{page_section}"


def prune_dict(obj):
    """Remove any None elements from the dict"""
    return {k: v for k, v in obj.items() if v is not None}
