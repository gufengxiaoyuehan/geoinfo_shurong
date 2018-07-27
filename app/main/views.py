from . import main


@main.route("/")
def index():
    return '<h1 style="text-align:center">树融API</h1>'
