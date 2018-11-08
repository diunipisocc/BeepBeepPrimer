from monolith.tests.utility import client, login, create_user, logout
from monolith.database import db, User
from werkzeug.security import check_password_hash


def test_create_user(client):
    tested_app, app = client
    reply = tested_app.post('/create_user', data=dict(email='andrea@prova.it', firstname='andrea', lastname='bongiorno',
                                              password='123456',
                                              age=23,
                                              weight=70,
                                              max_hr=120,
                                              rest_hr=60,
                                              vo2max=99), follow_redirects=True)

    assert reply.status_code == 200  # create_user success (it also redirect to login)

    assert login(tested_app, 'andrea@prova.it', '123456').status_code == 200

    # cannot create a user when already logged in
    assert create_user(tested_app).status_code == 403

    with app.app_context():
        user = db.session.query(User).filter(User.email == 'andrea@prova.it').first()
        assert user is not None
        assert user.email == 'andrea@prova.it'
        assert user.firstname == 'andrea'
        assert user.lastname == 'bongiorno'
        assert check_password_hash(user.password, '123456') is True
        assert user.age == 23
        assert user.weight == 70
        assert user.max_hr == 120
        assert user.rest_hr == 60
        assert user.vo2max == 99

    logout(tested_app)

    # cannot create a user with the same email
    reply = tested_app.post('/create_user', data=dict(email='andrea@prova.it', firstname='andrea', lastname='bongiorno',
                                                      password='123456',
                                                      age=23,
                                                      weight=70,
                                                      max_hr=120,
                                                      rest_hr=60,
                                                      vo2max=99), follow_redirects=False)
    assert reply.status_code == 409