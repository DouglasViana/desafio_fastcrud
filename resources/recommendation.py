from flask_restful import Resource, reqparse
from models.recommendation import RecommendationModel
from flask import request, jsonify
from sql_alchemy import datastorage
import mysql.conector
from dotenv import load_dotenv
import os

load_dotenv()

my_user = os.getenv("USER")
my_password = os.getenv("PASS")
my_host = os.getenv("HOST")
my_database = os.getenv("DATABASE")

path_params = reqparse.RequestParser()
path_params.add_argument('recommendation_id', type=int)
path_params.add_argument('name', type=str)
path_params.add_argument('email', type=str)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Recommendations(Resource):

    def get(self):
        connection = mysql.connector.connect(user=my_user, password=my_password,
                                             host=my_host,
                                             database=my_database)
        cursor = connection.cursor()

        indications = []
        for recommendation in RecommendationModel.query.all():
            indications.append(recommendation.json())
        return {'recommendations': indications}

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
            recommendation_found .update_recommendation(**data)
            recommendation_found .save_recommendation()
            return recommendation_found .json(), 200
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
