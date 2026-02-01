from common import app, api
import resources as apir 

api.add_resource(apir.OAuth2, '/mobile/OAuth2')
api.add_resource(apir.MobileLogin, '/mobile/MobileLogin')
api.add_resource(apir.MobileRegistration, '/mobile/MobileRegistration')