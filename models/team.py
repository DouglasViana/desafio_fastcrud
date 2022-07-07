from sql_alchemy import datastorage

class TeamModel(datastorage.Model):
    __tablename__ = 'team'

    team_id = datastorage.Column(datastorage.Integer, primary_key=True)
    team = datastorage.Column(datastorage.String(80))


    def __init__(self,team):
        self.team = team

    def json(self):
        return {
            'team_id': self.team_id,
            'team': self.team
        }

    @classmethod
    def find_team(cls, team_id):
        team = cls.query.filter_by(team_id=team_id) .first()
        if team:
            return team
        return None

    def save_team(self):
        datastorage.session.add(self)
        datastorage.session.commit()


    def update_team(self, team):
        self.team = team

    def delete_team(self):
        datastorage.session.delete(self)
        datastorage.session.commit()
