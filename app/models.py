from app import db

class Key(db.Model):
    Round = db.Column(db.Integer, primary_key=True)
    Prob = db.Column(db.String(120), primary_key=True)
    Key = db.Column(db.String(120), index = True, unique=True)
    

    def __repr__(self):
        return '<Key: {0}, Round: {1}, Prob: {2} >'.format(self.Key, self.Round, self.Prob) 
