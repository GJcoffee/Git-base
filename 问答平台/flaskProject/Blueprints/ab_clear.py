from models import UserModel, EmailCaptchaModel
from exts import db
from app import app


def db_clear():
    with app.app_context():
        user = UserModel.query.first()
        db.session.delete(user)
        # db.session.commit()
        captchas = EmailCaptchaModel.query
        for captcha in captchas:
            db.session.delete(captcha)
        db.session.commit()


if __name__ == "__main__":
    db_clear()
