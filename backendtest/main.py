from flask import Flask, request, jsonify, abort , redirect, url_for
from flask_restful import Resource, Api 
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
sound_path = 'music'
model_path = 'weight'
extensions_sound = ['.mp3', '.wav']

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

# Get the list of all files in the folder
def check_file_exist(file_name):
    try:
        # List all files in the directory
        files = os.listdir(sound_path)

        # Check if the file with the specified name exists
        file_exists = any(file.lower() == file_name.lower() for file in files)

        if file_exists:
            print(f"The file '{file_name}' exists in the directory.")
            #return f"The file '{file_name}' exists in the directory."
            return f"True"
        else:
            print(f"No file '{file_name}' found in the directory.")
            return f"False"
    except Exception as e:
        return f"Error: {e}"

#remove file func
def delfile(path):
    try:
        os.remove(path)
        return (f"{path} has been successfully removed.")
    except FileNotFoundError:
        print(f"{path} not found.")
    except PermissionError:
        print(f"Permission error: Unable to remove {path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

#rename file func
def renamefile_func(oldfile,newfile,filepath):
    # Get the file name and extension
    oldfilename, oldfilename_extension = os.path.splitext(oldfile)
    print(oldfilename)

    if oldfilename_extension.lower() in extensions_sound :
        try:
            os.rename(os.path.join(filepath,oldfilename+oldfilename_extension),os.path.join(filepath,newfile+oldfilename_extension))
            data = {
                'status':'rename',
                'oldfilename':oldfilename+oldfilename_extension,
                'newfilename':newfile+oldfilename_extension
            }
            return data
        except Exception as e:
            return f"An error occurred: {e}"
    else :
        return 'False'

def upload_func(maxfilesize,file,savepath):
    if file.content_length <= maxfilesize:
        filename = secure_filename(file.filename)
        file.save(os.path.join(savepath, filename))
        return f'File {file.filename} uploaded successfully',200
    else:
        return f'File {file.filename} save error',406

########################## MODEL METHOD  ############################
def check_model_path(modelname):
    if not os.path.exists(os.path.join(model_path,modelname)):
        print('model not exist')
        os.mkdir(os.path.join(model_path,modelname))
        return 'T'
     
app = Flask(__name__)
api = Api(app)
CORS(app)
#manage-sound
@app.route("/manage-sound/view", methods=['GET'])
def get_sound():
    all_files = os.listdir(sound_path)
    sound_files = [{'id': i + 1, 'text': file} for i, file in enumerate(all_files) if file.lower().endswith(('.mp3', '.wav'))]
    if not sound_files:
        #return 'not have file in directory'
        return 'Null'
    return jsonify(get_paginated_list(
    sound_files, 
    '/manage-sound/view', 
    start=request.args.get('start'), 
    limit=request.args.get('limit')
    ))

@app.route("/manage-sound/del", methods=['DELETE'])
def delete_sound():
    try:
        test = request.args.get("filename", default="", type=str)
        if check_file_exist(test) == "True":
            return delfile(os.path.join(sound_path, test))
    except Exception as error:
        app.logger.error("Error ", error)
        return 'Error'

@app.route("/manage-sound/rename", methods=['PUT'])
def rename_sound():
    try:
        oldfile = request.args.get("oldfile", default="", type=str)
        newfile = request.args.get("newfile", default="", type=str)
        if check_file_exist(oldfile) == "True":
            return  renamefile_func(oldfile,newfile,sound_path)
        else: 
            return f'error'
    except Exception as error:
        app.logger.error("Error ", error)
        return 'Error'

@app.route('/manage-sound/upload', methods=['POST'])
def uploadfile_sound():
    file = request.files['audioFile']
    #filename = request.args.get("oldfile", default="", type=str)
    # Set the maximum file size (70MB in this example)
    MAX_FILE_SIZE = 70 * 1024 * 1024  # Set to 70 MB

    # Get the file name and extension
    #filename, filename_extension = os.path.splitext(oldfile)

    if 'audioFile' not in request.files:
        return 'No file part',406

    if file.filename == '':
        return 'No selected file',406
    fileuploadname, fileupload_extension = os.path.splitext(file.filename)
    print(fileupload_extension,fileuploadname)
    if fileupload_extension.lower() in extensions_sound :
        try:
            print('yes')
            return upload_func(MAX_FILE_SIZE,file,os.path.join(sound_path))
        except Exception as error:
            print(error)
            return f'File {file.filename} not support .wav and .mp3 File size  maximum limit of 70 MB.',406
    


################################### END SOUND MANAGE ##########################
    
@app.route('/manage-model/upload', methods=['POST'])
def uploadfile_model():
    model_name = request.args.get("modelname", default="", type=str)
    pth_file = request.files['pth']
    index_file = request.files['index']
    #pth_filename, pth_file_extension = os.path.splitext(pth_file.filename)
    #index_filename, index_file_extension = os.path.splitext(index_file.filename)
    if 'pth' not in request.files:
        return 'No file part',406
    
    if 'index' not in request.files:
        return 'No file part',406
    
    if check_model_path(model_name) == "T":
        if not index_file :
            upload_func(200 * 1024 * 1024,pth_file,os.path.join(model_path,model_name))
            return {
            'Status':'uploadmodel',
            'ModelName' : model_name ,
            'pth': pth_file.filename,
            }
        elif index_file:
            upload_func(200 * 1024 * 1024,pth_file,os.path.join(model_path,model_name))
            upload_func(200 * 1024 * 1024,index_file,os.path.join(model_path,model_name))
            return { 'Status': 'uploadmodel',
            'ModelName': model_name,
            'pth': pth_file.filename,
            'index': index_file.filename
            }
    else:
        return 'model exist'

@app.route('/manage-model/view', methods=['GET'])
def get_model():
    modelpath_files = os.listdir(model_path)
    model_file = os.listdir(model_path)
    model_structure = []
    for root, dirs, files in os.walk(model_path):
        folder_path = os.path.relpath(root, model_path)
        folder_info = {'folder_name': folder_path, 'files': []}

    # Collect information about files inside the folder
        for file in files:
            if file.lower().endswith(('.pth', '.index')):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, model_path)
                print(relative_path)
                folder_info['files'].append({'file_id': len(folder_info['files']) + 1, 'file_name': relative_path})

    # Add the folder information to the model_structure
        model_structure.append(folder_info)

    # Print the collected information
    # for folder_info in model_structure:
    #     print(f"Folder: {folder_info['folder_name']}")
    #     for file_info in folder_info['files']:
    #         print(f"  File ID: {file_info['file_id']}, File Name: {file_info['file_name']}")

    return jsonify(get_paginated_list(
    model_structure
    ,'/manage-model/view'
    , start=request.args.get('start')
    , limit=request.args.get('limit')
    ))
    #return jsonify(model_structure)



    

    


    #     return jsonify(get_paginated_list(
    # sound_files, 
    # '/manage-sound/view', 
    # start=request.args.get('start'), 
    # limit=request.args.get('limit')
    # ))
    

    



if __name__ == "__main__":
    app.run(host='192.168.1.38', debug=True)



