from flask import Flask, request, jsonify #JSONIFY converting python dictionaries or lists into JSON
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipeBook.db"
db = SQLAlchemy(app)

class Recipe(db.Model): #Creates a recipe object
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    ingredient = db.Column(db.String, nullable = False)
    instruction = db.Column(db.String, nullable = False)
    createdAt = db.Column(db.String, nullable=False)
    updatedAt = db.Column(db.String, nullable=False)

    def to_dict(self): #Converts Recipe object into a python dictionary
        return {
            "id": self.id,
            "name": self.name,
            "ingredient": self.ingredient,
            "instruction": self.instruction,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

with app.app_context():
    db.create_all()

#Displays a json txt(Welcome to recipe book)
@app.route("/")
def home():
    return jsonify({"message": "Welcome to recipe book"})


#Displays all recipes if available
@app.route("/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes])


#Displays a specific recipe based on the id number
@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        return jsonify(recipe.to_dict())
    else:
        return jsonify({"error": "Recipe not found"}), 404


#Creates a recipe
@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.get_json()
    new_recipe = Recipe(
        name=data["name"],
        ingredient=data["ingredient"],
        instruction=data["instruction"],
        createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updatedAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201


#Replaces a recipe based on the id
@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def find_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Note not found"}), 404
    else:
        data = request.get_json()
        recipe.name = data["name"]
        recipe.ingredient = data["ingredient"]
        recipe.instruction = data["instruction"]
        recipe.updatedAt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        return jsonify(recipe.to_dict())

#Deletes a recipe based on the id
@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"})


if __name__ == "__main__": #Refresh
    app.run(debug=True)

