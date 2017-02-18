
class Configuration:
    def __init__(self, conf_spread):

        all_pages = conf_spread.row_values(5)[1:]

        self.sitename = conf_spread.acell('B3').value
        self.template = conf_spread.acell('B4').value
        self.pages = [page for page in all_pages if page]
