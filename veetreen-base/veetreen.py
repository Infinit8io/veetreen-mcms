from flask import Flask
from flask import render_template

# Credentials google
from veetreen_utils import get_configuration
from veetreen_utils import page_is_valid

import gspread
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

template = "bootstrap4"

@app.route('/')
@app.route('/<pagename>')
def page(pagename=None):

    # Get all the pages
    spreadsheet = gc.open('veetreen')

    # Get the config
    conf = spreadsheet.worksheet("Configuration")

    # Config infos
    sitename = conf.acell('B3').value
    template = conf.acell('B4').value
    all_pages = conf.row_values(5)[1:]
    pages = [page for page in all_pages if page]


    # Checking page validity
    if not page_is_valid(pagename, pages):
        page = "home"

    worksheets_list = spreadsheet.worksheets()
    return render_template(template + '/home.html', pages=pages)


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
gc = gspread.authorize(credentials)
