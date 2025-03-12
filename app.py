from flask import Flask, render_template, request, redirect, url_for
from models import db, Quiz, Question, Answer, UserResult

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>')
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', quiz=quiz)

@app.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    score = 0
    for question in quiz.questions:
        selected_answer = request.form.get(str(question.id))
        if selected_answer == question.correct_answer:
            score += 1
    user_result = UserResult(quiz_id=quiz.id, score=score)
    db.session.add(user_result)
    db.session.commit()
    return redirect(url_for('result', result_id=user_result.id))

@app.route('/result/<int:result_id>')
def result(result_id):
    result = UserResult.query.get_or_404(result_id)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
