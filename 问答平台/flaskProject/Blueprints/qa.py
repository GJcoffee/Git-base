from flask import Blueprint, request, render_template, g, redirect, url_for
from .forms import QuestionForm
from models import QuestionModel
from exts import db

qa_bp = Blueprint('qa', __name__, url_prefix='/')


@qa_bp.route('/')
def index():
    return 'OK'


@qa_bp.route('/qa/public', methods=['GET', 'POST'])
def qa_public():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.commit()
            # todo:跳转到详情页
            return redirect(url_for('qa.index'))
        else:
            print(form.errors)
            return redirect(url_for('qa.qa_public'))
        # 7:26
