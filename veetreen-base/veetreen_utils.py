

def get_configuration():
    pass

def page_is_valid(pagename, pages):
    # Test if the page is valid
    if pagename is None or pagename.title() not in pages:
        print("Invalid page name in route")
        return False
    else:
        print("Route is ok")
        return True
