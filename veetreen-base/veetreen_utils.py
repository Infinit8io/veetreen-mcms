

def get_configuration():
    pass

def page_is_valid(pagename, pages):
    # Test if the page is valid
    return (pagename is None or pagename.title() not in pages)
