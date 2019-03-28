from flask import Flask, render_template, request, redirect

import data_manager

app = Flask(__name__)


@app.route('/')
def route_home():
    return render_template('index.html')


@app.route('/list')
def route_list():
    questions = data_manager.get_all_questions()
    return render_template('list.html', questions=questions)


@app.route('/add', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        data_manager.add_question(request.form)
        return redirect('/list')
    return render_template('form.html')


@app.route('/question_detail/<id>')
def route_question_detail(id):
    try:
        question = data_manager.get_question_by_id(id)
        answers = data_manager.get_answers_by_question_id(id)
        return render_template('qd.html', question=question, id=id, answers=answers)
    except ValueError:
        return redirect('/')


@app.route('/question/<id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(id):
    if request.method == 'POST':
        current_file = data_manager.get_all_answers()
        new_answer = {}
        if current_file:
            new_answer['id'] = str(int(current_file[-1]['id']) + 1)
        else:
            new_answer['id'] = '0'
        new_answer['submission_time'] = ''
        new_answer['vote_number'] = '0'
        new_answer['question_id'] = id
        new_answer['message'] = request.form['answer']
        new_answer['image'] = ''
        current_file.append(new_answer)
        data_manager.save_new_answer(current_file)
        return redirect('/question_detail/' + id)
    return render_template('answer.html')


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5004
)
