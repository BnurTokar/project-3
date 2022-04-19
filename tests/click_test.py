import os

from click.testing import CliRunner

from app import create_log_folder, create_database

runner = CliRunner()

def test_create_log_folder():
    response = runner.invoke(create_log_folder)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    #set the name of the apps log folder to logs
    logdir = os.path.join(root,'../app/logs')
    #make a directory if it doesn't exist
    assert os.path.exists(logdir)


def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    #set the name of the apps log folder to logs
    dbdir = os.path.join(root,'../database')
    #make a directory if it doesn't exist
    assert os.path.exists(dbdir)


def test_logs_files():
    root = os.path.dirname(os.path.abspath(__file__))
    request_log_file = os.path.join(root, '../app/logs/request.log')
    debug_log_file = os.path.join(root, '../app/logs/debug.log')
    flask_log_file = os.path.join(root, '../app/logs/flask.log')
    assert os.path.exists(request_log_file)
    assert os.path.exists(debug_log_file)
    assert os.path.exists(flask_log_file)
