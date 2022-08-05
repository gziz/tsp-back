from project import db


class Location(db.Model):
    __tablename__='locations_fake'
    id= db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(30))
    city = db.Column(db.String(50))
    institution = db.Column(db.String(120))
    location = db.Column(db.String(140))
    university = db.Column(db.String(140))
    enrollments = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __repr__(self):
        return f"Location: {self.university}"

    def __init__(self):
        pass

def format_location(location):
    return {
        "id": location.id,
        "estado": location.estado,
        "city": location.city,
        "institution": location.institution,
        "location": location.location,
        "university": location.university,
        "enrollments": location.enrollments,
        "lat": location.lat,
        "lon": location.lon,
    }