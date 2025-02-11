from flask import Flask,jsonify,redirect
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db,Bookmark
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import *
from flasgger import Swagger,swag_from
from src.config.swagger import template,swagger_config
from dotenv import load_dotenv

def create_app(test_config=None):
    
    load_dotenv()
    
    app = Flask(__name__,
    instance_relative_config = True)
    
    
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("dev"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY'),
            SWAGGER = {
                "title":"Bookmarks API",
                "uiversion" :3
            }
            
        )

    else:
        app.config.from_mapping(test_config)
    
    db.app = app
    db.init_app(app)
    
    JWTManager(app)
    
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    
    Swagger(app,config=swagger_config,template=template)
    
    @app.get('/<short_url>')
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
        if bookmark:
            bookmark.visists += 1
            db.session.commit()
            
            return redirect(bookmark.url)
        else:
            return jsonify({
            "message": "URL not found"
            }),HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error":"Notfound"}),HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_404(e):
        return jsonify({"error":"Internal server error"}),HTTP_500_INTERNAL_SERVER_ERROR
        
    return app
