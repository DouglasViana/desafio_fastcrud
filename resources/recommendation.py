from flask_restful import Resource, reqparse
from models.recommendation import RecommendationModel
from models.employee import EmployeeModel
from flask import request, jsonify
from sql_alchemy import datastorage


class Recommendations(Resource):

    def get(self):
        slk = []
        for recommendation in RecommendationModel.query.all():
            slk.append(recommendation.json())
        return {'recommendations': slk}

    def post(self):

        data = [request.json['name'], request.json['email'], request.json['employee_id']]
        recommendation = RecommendationModel(*data)
        datastorage.session.add(recommendation)
        datastorage.session.commit()

        return jsonify(recommendation.json())



class Recommendation(Resource):
    info = reqparse.RequestParser()
    info.add_argument('name', type=str, required=True, help="The Field 'name' cannot be left blank")
    info.add_argument('email', type=str, required=True, help="The Field 'email' cannot be left blank")
    info.add_argument('employee_id', type=int, required=True, help="The Field 'employee_id' cannot be left blank")

    def get(self, recommendation_id):
        recommendation = RecommendationModel.find_recommendation(recommendation_id)
        if recommendation:
            return recommendation.json()
        return {'message': 'Recommendation not found.'}, 404


    def put(self, recommendation_id):
        data = Recommendation.info.parse_args()
        recommendation_found = RecommendationModel.find_recommendation(recommendation_id)
        if recommendation_found:
           recommendation_found.update_recommendation(**data)
           recommendation_found.save_recommendation()
           return recommendation_found.json(), 200
        recomend = RecommendationModel(recommendation_id, **data)
        try:
            recomend.save_recommendation()
        except:
            return {'message': 'An internal error occurred trying to save recommendation.'}, 500
        return recomend.json(), 201


    def delete(self, recommendation_id):
        recommendation = RecommendationModel.find_recommendation(recommendation_id)
        if recommendation:
            try:
                recommendation.delete_recommendation()
            except:
                return {'message': 'An error occurred trying to delete recommendation.'}, 500
            return {'message': 'Recommendation deleted'}
        return {'message': 'Recommendation not found'}, 404


class EmployeeRecommendations(Resource):
    def get(self):
        internal_recommendations=datastorage.session.query(RecommendationModel, EmployeeModel).join(EmployeeModel).all()

        for recommended, employees in internal_recommendations:
            employees_who_recommend = [recommended.name, employees.json()]
            return employees_who_recommend
