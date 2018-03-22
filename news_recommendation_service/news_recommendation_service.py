import operator
import os
import sys
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

SERVER_HOST_NAME = 'localhost'
SERVER_PORT = 5050
TABLE_NAME_FOR_PREFERENCE_MODEL = 'user_preference_model'

# float comparison
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def get_preference_for_user(user_id):
    """ Get preference for user in an ordered class list. """
    print("Get preference model for user: %s" % user_id)
    db = mongodb_client.get_db()
    model = db[TABLE_NAME_FOR_PREFERENCE_MODEL].find_one({'userId': user_id})
    # preference is not existing in DB, return empty list for equal possibility of each class
    if model is None:
        return []
    
    # sorted by possibility in descending order
    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    sorted_class_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]

    # no preference
    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []
    
    return sorted_class_list

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST_NAME, SERVER_PORT))
RPC_SERVER.register_function(get_preference_for_user, 'getPreferenceForUser')
print("Starting HTTP server on %s:%d" % (SERVER_HOST_NAME, SERVER_PORT))
RPC_SERVER.serve_forever()

