from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(80), unique=False, nullable=False)
  is_active = db.Column(db.Boolean(), unique=False, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.email

  def serialize(self):
    return {
      "id": self.id,
      "email": self.email,
      # do not serialize the password, its a security breach
    }


class Planets(db.Model):
  __tablename__ = 'planets'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60))
  rotation_period = db.Column(db.Integer)
  orbital_period = db.Column(db.Integer)
  climate = db.Column(db.String(50))
  terrain = db.Column(db.String(60))
  surface_water = db.Column(db.Integer)

  def __repr__(self):
    return '<Planet %r>' % self.id

  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "rotation_period": self.rotation_period,
      "orbital_period": self.orbital_period,
      "climate": self.climate,
      "superface_water": self.surface_water,
      "terrain": self.terrain
    }


class Character(db.Model):
  __tablename__ = 'character'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60), unique=True)
  height = db.Column(db.Integer)
  hair_color = db.Column(db.String(50))
  skin_color = db.Column(db.String(50))
  eye_color = db.Column(db.String(50))
  mass = db.Column(db.Integer)
  gender = db.Column(db.String(20))
  homeworld = db.Column(db.Integer, db.ForeignKey(Planets.id))
  homeworld_relationship = relationship(Planets)

  def __repr__(self):
    return '<Character %r>' % self.id

  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "height": self.height,
      "hair_color": self.hair_color,
      "eye_color": self.eye_color,
      "gender": self.gender,
      "mass": self.mass,
      "homeworld": self.homeworld
    }


class Starships(db.Model):
  __tablename__ = 'starships'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True)
  model = db.Column(db.String(50), unique=True)
  length = db.Column(db.Integer)
  passengers = db.Column(db.Integer)
  starship_class = db.Column(db.String(100))
  pilots = db.Column(db.Integer, db.ForeignKey(Character.id))
  pilots_relationship = relationship(Character)

  def __repr__(self):
    return '<Starships %r>' % self.id

  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "model": self.model,
      "length": self.length,
      "passengers": self.passengers,
      "starship_class": self.starship_class,
      "pilots": self.pilots
    }


class Favorite_Planets(db.Model):
  __tablename__ = 'favplanets'
  id = db.Column(db.Integer, primary_key=True)
  planets = db.Column(db.Integer, db.ForeignKey(Planets.id))
  planets_relationship = relationship(Planets)
  user = db.Column(db.Integer, db.ForeignKey(User.id))
  user_relationship = relationship(User)

  def __repr__(self):
    return '<Favorite_Planets %r>' % self.id

  def serialize(self):
    return {
      "id": self.id,
      "planets": self.planets
    }


class Favorite_Character(db.Model):
  __tablename__ = 'favcharacter'
  id = db.Column(db.Integer, primary_key=True)
  character = db.Column(db.Integer, db.ForeignKey(Character.id))
  character_relationship = relationship(Character)
  user = db.Column(db.Integer, db.ForeignKey(User.id))
  user_relationship = relationship(User)

  def __repr__(self):
    return '<Favorite_Character %r>' % self.id

  def serialize(self):
    return {
      "id": self.id,
      "character": self.character
    }


class Favorite_Starships(db.Model):
  __tablename__ = 'favstarships'
  id = db.Column(db.Integer, primary_key=True)
  starships = db.Column(db.Integer, db.ForeignKey(Starships.id))
  starships_relationship = relationship(Starships)
  user = db.Column(db.Integer, db.ForeignKey(User.id))
  user_relationship = relationship(User)

  def __repr__(self):
    return '<Favorite_Starships %r>' % self.id

  def serialize(self):
    return {
      "id": self.id,
      "starships": self.starships
    }
