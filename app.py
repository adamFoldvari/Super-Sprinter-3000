from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)


def read_data_from_csv(filename):
    story_list = []
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as workfile:
        reader = csv.reader(workfile)
        for row in reader:
            story_list.append(row[0].split(';'))
    return story_list


def add_data_to_csv(filename, story_list):
    with open(os.path.join(os.path.dirname(__file__), filename), 'w') as workfile:
        for item in story_list:
            story = [element.replace("\r\n", " ") for element in item]
            row = ';'.join(story)
            workfile.write(row + "\n")


@app.route('/')
@app.route('/list')
def list_page():
    readed_story_list = read_data_from_csv('story_list.csv')
    return render_template("list.html", story_list=readed_story_list)


@app.route('/story', methods=['GET'])
def story_page(story_id=None):
    empyt_list = []
    for i in range(7):
        empyt_list.append(' ')
    return render_template('form.html', story_id=story_id, data_to_edit=empyt_list)


@app.route('/story', methods=['POST'])
def add_story():

    story_list = read_data_from_csv('story_list.csv')
    new_row = [str(len(story_list)+1)]
    form_elements = [
                    "story_title",
                    "user_story",
                    "acceptance_criteria",
                    "business_value",
                    "estimation",
                    "status"
                    ]
    for element in form_elements:
        new_row.append(request.form[element])
    story_list.append(new_row)
    add_data_to_csv('story_list.csv', story_list)
    return redirect(url_for('list_page'))


@app.route('/story/<story_id>')
def update_strory(story_id):
    story_list = read_data_from_csv('story_list.csv')
    for row in story_list:
        if row[0] == story_id:
            editable_row = row
    return render_template('form.html', story_id=story_id, data_to_edit=editable_row)


@app.route('/story/update/<story_id>', methods=['POST'])
def update_data(story_id):
    story_list = read_data_from_csv('story_list.csv')
    for index in range(len(story_list)):
        if story_id == story_list[index][0]:
            story_list[index][1] = request.form["story_title"]
            story_list[index][2] = request.form["user_story"]
            story_list[index][3] = request.form["acceptance_criteria"]
            story_list[index][4] = request.form["business_value"]
            story_list[index][5] = request.form["estimation"]
            story_list[index][6] = request.form["status"]
    add_data_to_csv('story_list.csv', story_list)
    return redirect(url_for('list_page'))


@app.route('/story/<story_id>/delete/')
def delete_story(story_id):
    story_list = read_data_from_csv('story_list.csv')
    for row in story_list:
        if row[0] == story_id:
            story_list.remove(row)
    add_data_to_csv('story_list.csv', story_list)
    return redirect(url_for('list_page'))


if __name__ == '__main__':
    app.run(debug=True)
