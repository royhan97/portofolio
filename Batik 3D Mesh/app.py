from flask import Flask, request
from flask_mail import Mail
import src.controllers as controllers
import config.config as config


"""
DEFINE APP
"""
app = Flask(__name__)
config.configure(app)
mail = Mail(app)


"""
WITH CONTROLLERS
"""

""" RETURN PAGES """
@app.route('/')
def index_page():
    return controllers.index_page()


@app.route('/build')
def build_page():
    return controllers.build_page()


@app.route('/order')
def order_page():
    return controllers.order_page()


@app.route('/result-design')
def result_design_page():
    return controllers.result_design_page()


@app.route('/result-order')
def result_order_page():
    return controllers.result_order_page()


""" PROCEED FORM SUBMIT """
@app.route('/submit-design', methods=['POST'])
def submit_design():
    return controllers.submit_design(request)


@app.route('/submit-order', methods=['POST'])
def submit_order():
    return controllers.submit_order(request)


""" OTHERS """
@app.route('/finish')
def finish():
    return controllers.finish(mail)


@app.route('/get-result-img/<string:img_id>')
def get_image(img_id):
    return controllers.get_image(img_id)


"""
MAIN EXECUTION
"""
if __name__ == '__main__':
    app.run()
