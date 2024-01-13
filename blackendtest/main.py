from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api 
import os
from flask_cors import CORS
folder_path = 'music'

# Get the list of all files in the folder
def check_file_sound_exist(file_name):
    try:
        # List all files in the directory
        files = os.listdir(folder_path)

        # Check if the file with the specified name exists
        file_exists = any(file.lower() == file_name.lower() for file in files)

        if file_exists:
            print(f"The file '{file_name}' exists in the directory.")
            return True
        else:
            print(f"No file '{file_name}' found in the directory.")
            return False
    except Exception as e:
        print(f"Error: {e}")





    
app = Flask(__name__)
api = Api(app)
CORS(app)
@app.route("/rename", methods=['PUT'])
def renamefile():
    #all_files = os.listdir(folder_path)
    try:
        request.args.get('parms') == 'filename'
        print('yes')
        return {
        "Status": "OK",
        "Log" : "Reanme file Succes"
        }
        #return 'True'
        #     print('yes')
        #     if (check_file_sound_exist('music1.mp3')) == True:
        #         print('file exist')
        #         return 'True'
        #     elif (check_file_sound_exist('test.mp3')) == False:
        #         print('file not exist')
        #         return 'False'
        #os.remove(file_path)
    except Exception as error:
        app.logger.error("Error ", error)
        return 'Error'


@app.route("/del", methods=['DELETE'])
def removefile():
    try:
        request.args.get('filename') 
        print('yes')
        return {
        "Status": "OK",
        "Log" : "Delete file Succes"
        }

    except Exception as error:
        app.logger.error("Error ", error)
        return 'Error'

    


def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj

class Employees(Resource):
    def get(self):
        all_files = os.listdir(folder_path)
        mp3_files = [{'id': i + 1, 'text': file} for i, file in enumerate(all_files) if file.lower().endswith(('.mp3', '.wav'))]
        return jsonify(get_paginated_list(
        mp3_files, 
        '/employees', 
        start=request.args.get('start', 1), 
        limit=request.args.get('limit', 5)
    ))

api.add_resource(Employees, '/employees')


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
