from flask import Flask
from flask_restful import Api
from resources.employee import Employees, Employee
from resources.recommendation import Recommendations, Recommendation
from resources.team import Teams, Team

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datastorage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def cria_datastorage():
    datastorage.create_all()


api.add_resource(Employees, '/employees')
api.add_resource(Employee, '/employee/<string:employee_id>')
api.add_resource(Recommendations, '/recommendations')
api.add_resource(Recommendation, '/recommendation/<string:recommendation_id>')
api.add_resource(Teams, '/teams')
api.add_resource(Team, '/team/<string:team_id>')

if __name__ == '__main__':
    from sql_alchemy import datastorage

    datastorage.init_app(app)
    app.run(debug=True)
