from flask import Flask
from flask import render_template

# Credentials google
from veetreen_utils import get_configuration
from veetreen_utils import page_is_valid

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from configuration import Configuration

app = Flask(__name__)

template = "bootstrap4"

home_context = {
    'main_title':       'B3',
    'subline_title':    'B4',
    'action_1_text':    'B6',
    'action_1_url':     'C6',
    'action_2_text':    'B7',
    'action_2_url':     'C7',
    'background_image': 'B9',
}

about_context = {
    'about_title':      'B4',
    'about_subline':    'B5',
    'about_txt_1':      'B7',
    'about_txt_2':      'B8',
    'about_txt_3':      'B9',
    'profile_picture':  'B11',
}

blog_context = {
    'blog_first_post':  'A3',
}

@app.route('/')
@app.route('/<pagename>')
def page(pagename=None):

    home_sheet = spreadsheet.worksheet("Home")

    context = {} # Preparing empty context

    for key, cell in home_context.items():
        context[key] = home_sheet.acell(cell).value # Fill the context with cell content

    # Checking page validity
    if not page_is_valid(pagename, conf.pages):
        page = "home"

    return render_template(conf.template + '/home.html', pages=conf.pages, context=context)

@app.route('/about')
def about():

    about_sheet = spreadsheet.worksheet("About")

    context = {}

    for key, cell in about_context.items():
        context[key] = about_sheet.acell(cell).value

    return render_template(conf.template + '/about.html', pages=conf.pages, context=context)

@app.route('/blog')
def blog():

    blog_sheet = spreadsheet.worksheet("Blog")

    context = {}
    context["posts"] = []


    all_blog_sheet = blog_sheet.get_all_records(head=2)

    for post in all_blog_sheet:
        if post["Title"] != "" and post["Content"] != "" and post["Published"] != "No":
            context["posts"].append(post)

    return render_template(conf.template + '/blog.html', pages=conf.pages, posts=context["posts"])

@app.route('/blog/<id>-<title>')
def blog_post(id, title):

    blog_sheet = spreadsheet.worksheet("Blog")

    blog_post = blog_sheet.row_values(int(id) + 2)
    print(blog_post)

    return render_template(conf.template + '/post.html', pages=conf.pages, post=blog_post)


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
gc = gspread.authorize(credentials)
# Get all the pages ad create the configuration
spreadsheet = gc.open('veetreen')
conf = Configuration(spreadsheet.worksheet("Configuration"))
