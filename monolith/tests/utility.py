import pytest
import os
import tempfile
from random import uniform, randint
from datetime import datetime

from monolith.app import create_app
from monolith.database import db, Run, Objective


# read in SQL for populating test data
# with open(os.path.join(os.path.dirname(__file__), 'prova.sql'), 'rb') as f:
#    _data_sql = f.read().decode('utf8')

@pytest.fixture
def client():
    """ This function initialize a new DB for every test and creates the app. This function returns a tuple,
    the first element is a test client and the second is the app itself. Test client must be used for sending
    request and the app should be used for getting a context when, for example, we need to query the DB.
    I haven't found a more elegant way to do this."""
    app = create_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    print(app.config['DATABASE'])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.config['DATABASE']
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF validation -> DO THIS ONLY DURING TESTS!
    client = app.test_client()

    db.create_all(app=app)
    db.init_app(app=app)
    #with app.app_context():
        #db.engine.execute(_data_sql)

    yield client, app

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def login(client, email, password):
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def logout(client):
    return client.get('/logout')

def new_user(client, email='marco@prova.it', firstname='marco', lastname='mario', password='123456', age=18,
             weight=70, max_hr=120, rest_hr=65, vo2max=99):

    return client.post('/create_user', data=dict(email=email, firstname=firstname, lastname=lastname, password=password,
                                                 age=age,
                                                 weight=weight,
                                                 max_hr=max_hr,
                                                 rest_hr=rest_hr,
                                                 vo2max=vo2max),
                       follow_redirects=False)


def new_run(user, strava_id=randint(100, 100000000), name=None, distance=uniform(50.0, 10000.0), elapsed_time=uniform(30.0, 3600.0),
average_heartrate=None, total_elevation_gain=uniform(0.0, 25.0), start_date=datetime.now()):
    if name == None :
        name = "Run %s"%(strava_id)

    run = Run()
    run.runner = user
    run.strava_id = strava_id  # a random number 100 - 1.000.000, we hope is unique
    run.name = name
    run.distance = distance  # 50m - 10 km
    run.elapsed_time = elapsed_time  # 30s - 1h
    run.average_speed = run.distance / run.elapsed_time
    run.average_heartrate = average_heartrate
    run.total_elevation_gain = total_elevation_gain  # 0m - 25m
    run.start_date = start_date
    db.session.add(run)
    db.session.commit()

def new_objective(user, name = "Test Objective", target_distance = "42", start_date = datetime.now(), end_date = datetime.now()):
    objective = Objective()
    objective.runner = user
    objective.name = name
    objective.target_distance = target_distance
    objective.start_date = start_date
    objective.end_date = end_date
    db.session.add(objective)
    db.session.commit()

# TODO: delete this
'''
def create_user():
    user = User()
    user.email = 'test@example.com'
    user.firstname = "A"
    user.lastname = "Tester"
    user.strava_token = None
    user.age = 0
    user.weight = 0
    user.max_hr = 0
    user.rest_hr = 0
    user.vo2max = 0
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

def new_objective(client, ...)
    return client.post('create_objective, data')

def create_run(user, name, distance, elapsed_time, average_speed, average_heartrate, total_elevation_gain, start_date):
    run = Run()
    run.runner = user
    run.strava_id = 1
    run.name = name
    run.distance = distance
    run.elapsed_time = elapsed_time
    run.average_speed = average_speed
    run.average_heartrate = average_heartrate
    run.total_elevation_gain = total_elevation_gain
    run.start_date = start_date
    db.session.add(run)
    db.session.commit()
'''
