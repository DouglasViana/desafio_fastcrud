from flask_restful import Resource, reqparse
from models.team import TeamModel
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

class Teams(Resource):

    def get(self):
        connection = mysql.connector.connect(user=my_user, password=my_password,
                                             host=my_host,
                                             database=my_database)
        cursor = connection.cursor()

        times = []
        for team in TeamModel.query.all():
            times.append(team.json())
        return {'employees': times}

    def post(self):
        team_name = request.json['team']

        team = TeamModel(team_name)

        datastorage.session.add(team)
        datastorage.session.commit()

        return jsonify(team.json())



class Team(Resource):
    info = reqparse.RequestParser()
    info.add_argument('team', type=str, required=True, help="The Field 'team' cannot be left blank")

    def get(self, team_id):
        team = TeamModel.find_team(team_id)
        if team:
            return team.json()
        return {'message': 'Team not found.'}, 404




    def put(self, team_id):
        data = Team.info.parse_args()
        team_found = TeamModel.find_team(team_id)
        if team_found:
            team_found .update_team(**data)
            team_found .save_team()
            return team_found .json(), 200
        time = TeamModel(team_id, **data)
        try:
            time.save_team()
        except:
            return {'message': 'An internal error occurred trying to save team.'}, 500
        return time.json(), 201


    def delete(self, team_id):
        team = TeamModel.find_team(team_id)
        if team:
            try:
                team.delete_team()
            except:
                return {'message': 'An error occurred trying to delete the team.'}, 500
            return {'message': 'Team deleted'}
        return {'message': 'Team not found'}, 404
