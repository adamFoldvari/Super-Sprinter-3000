from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)


def read_data_from_csv():
    story_list = []
    with open('story_list.csv', 'r') as workfile:
        reader = csv.reader(workfile)
        for row in reader:
            story_list.append(row[0].split(';'))
    return story_list


def add_data_to_csv(story_list):
    with open('story_list.csv', 'w') as workfile:
        datawriter = csv.writer(workfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerows(story_list)


@app.route('/')
@app.route('/list')
def list_page():
    readed_story_list = read_data_from_csv()
    return render_template("list.html", story_list=readed_story_list)


@app.route('/story', methods=['GET', 'POST'])
def story_page(story_id=None):
    if request.method == 'GET':
        empyt_list = []
        for i in range(7):
            empyt_list.append(' ')
        return render_template('form.html', story_id=story_id, data_to_edit=empyt_list)
    else:
        story_list = read_data_from_csv()
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
        add_data_to_csv(story_list)
        return redirect(url_for('list_page'))


@app.route('/story/<story_id>')
def update_strory(story_id):
    story_list = read_data_from_csv()
    for row in story_list:
        if row[0] == story_id:
            editable_row = row
    return render_template('form.html', story_id=story_id, data_to_edit=editable_row)


@app.route('/story/update/<story_id>', methods=['POST'])
def update_data(story_id):
    story_list = read_data_from_csv()
    form_elements = [
                    "story_title",
                    "user_story",
                    "acceptance_criteria",
                    "business_value",
                    "estimation",
                    "status"
                    ]
    for index in range(len(story_list)):
        if story_id == story_list[index][0]:
            for num, element in enumerate(form_elements):
                story_list[index][num+1] = request.form[element]
    add_data_to_csv(story_list)
    return redirect(url_for('list_page'))


@app.route('/story/delete/<story_id>')
def delete_story(story_id):
    story_list = read_data_from_csv()
    for row in story_list:
        if row[0] == story_id:
            story_list.remove(row)
    add_data_to_csv(story_list)
    return redirect(url_for('list_page'))


if __name__ == '__main__':
    app.run(debug=True)
