from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.seat_service import SeatInfoService

app = Flask( __name__ )
CORS( app, resources={r"/api/*": {"origins": "*"}} )
api = Api( app )
api.prefix = '/api'
api.add_resource( SeatInfoService, "/seat/<string:info_type>" )

if __name__ == "__main__":
    app.run( debug=True )
