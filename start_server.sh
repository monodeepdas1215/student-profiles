python app/questions_before_starting.py
nohup gunicorn -c app/gunicorn_config.py app:flask_app &