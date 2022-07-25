from flask import Flask
from flask_restful import Api
from resources.employee import Employees, Employee
from resources.recommendation import Recommendations, Recommendation
from resources.team import Teams, Team
from sql_alchemy import datastorage
from dotenv import load_dotenv
import os

load_dotenv()

my_user = os.getenv("USER")
my_password = os.getenv("PASS")
my_database = os.getenv("DATABASE")


app = Flask(__name__)
datastorage.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://{user}:{password}@mysql.pythonanywhere-services.com/{database}'.format(user=my_user, password=my_password, database=my_database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.route('/')
def index():
    return '<h1>Está Funcionando!<h1>'

@app.before_first_request
def cria_datastorage():
    datastorage.create_all()


api.add_resource(Employees, '/employees')
api.add_resource(Employee, '/employee/<string:employee_id>')
api.add_resource(Recommendations, '/recommendations')
api.add_resource(Recommendation, '/recommendation/<string:recommendation_id>')
api.add_resource(Teams, '/teams')
api.add_resource(Team, '/team/<string:team_id>')

