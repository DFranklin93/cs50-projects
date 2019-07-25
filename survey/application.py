import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Testing list of students
students = []

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name")
    house = request.form.get("house")
    position = request.form.get("position")
    if not name or not house or not position:
        return "failure"
    with open('survey.csv','a') as survey:
        fieldnames = ['name', 'house', 'position']
        writer = csv.DictWriter(survey, fieldnames=fieldnames)
        writer.writerow({'name': name, 'house': house, 'position': position})
    return redirect("/sheet")

@app.route("/sheet", methods=['GET'])
def get_sheet():
    name = request.args.get('name')
    with open('survey.csv','r') as file:
        reader = csv.reader(file)
        student = list(reader)
    return render_template("sheet.html", student=student)
