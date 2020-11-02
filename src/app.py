from flask import Flask, render_template
from flask_cors import CORS

from .config import app_config
from .models import db, bcrypt

from .views.WorkflowView import workflow_api as workflow_blueprint

# https://www.codementor.io/@olawalealadeusi896/restful-api-with-python-flask-framework-and-postgres-db-part-1-kbrwbygx5
# http://js.syncfusion.com/demos/web/?_ga=2.107922690.1860884945.1580010873-1672802669.1580010873#!/azure/diagram/gettingstarted/swimlane


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__, static_url_path='/static/logo.jpg', static_folder = '/static')

    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    bcrypt.init_app(app)

    db.init_app(app)

    app.register_blueprint(workflow_blueprint, url_prefix='/api/v1/flow')

    CORS(app)

    @app.route('/', methods=['GET'])
    def index():

        return render_template('base.html')

    return app
