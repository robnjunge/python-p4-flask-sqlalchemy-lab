#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()

    if not animal:
        response_body = "<h1>Animal not found!</h1>"
        response = make_response(response_body, 404)
        return response
    else:
        response_body = f"""
            <ul>ID: {animal.id}</ul>
            <ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>
        """
        response = make_response(response_body, 200)
        return response


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    if not zookeper:
        response_body = "<h1>Zookeeper not found!</h1>"
        response = make_response(response_body, 404)


    response_body = f"""
        <ul>ID: {zookeper.id}</ul>
        <ul>Name: {zookeper.name}</ul>
        <ul>Birthday: {zookeper.birthday}</ul>
    """

    animals = [animal for animal in zookeper.animals]
    if not animals:
        response_body += f"<ul>Has no Animals at this time</ul>"
    
    else:
        for animal in animals:
            response_body += f"<ul>Animal: {animal.name}</ul>"

    response = make_response(response_body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    if not enclosure:
        response_body = "<h1>No enclosure found!</h1>"
        response = make_response(response_body, 404)
        return response
    response_body = f"""
        <ul>ID: {enclosure.id}</ul>
        <ul>Environment: {enclosure.environment}</ul>
        <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
    """

    animals = [animal for animal in enclosure.animals]

    if not animals:
        response_body += "<ul>Has no animals at this time"
    else:
        for animal in animals:
            response_body += f"<ul>Animal: {animal.name}</ul>"

    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)