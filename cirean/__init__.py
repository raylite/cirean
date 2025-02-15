from flask import Flask
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_bootstrap import Bootstrap
import os

from myneo4j.myneo4j import Neo4j

db = Neo4j()
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    bootstrap.init_app(app)

    from cirean.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from cirean.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='cirex_no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Cirex Failure Notification',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cirex.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
        app.logger.setLevel(logging.INFO)
    
        app.logger.info('Cirex startup')
    return app



from cirean import models
