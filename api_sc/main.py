from lib_vc.process import cli_infer
from flask import Flask,request , jsonify, render_template
#from dotenv import load_dotenv
import os 
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_paginate import Pagination


audio_floder = os.path.join(os.getcwd(), 'audios')
model_provide_floder = os.path.join(os.getcwd(), 'model_provide')
weightsmodel_floder= os.path.join(os.getcwd(), 'weights')

#load_dotenv()


def testnani():
    sample_command = '"serana700_e200_s7200.pth" "./audios/villan.wav" "output_audio.wav" "./weights/serana700_v2.index" 0 6 "rmvpe" 120 5  5 0.0  0.0 0.0'
    cli_infer(sample_command)



app = Flask(__name__)
CORS(app)
app.config['audio_floder'] = audio_floder

@app.route('/', methods=['GET'])
def index():
    return "Hello World!"

@app.route('/test', methods=['GET'])
def testnani():
    #test()
    return "nani"

@app.route('/uploadmusic', methods=['POST'])
def upload_file():
    # Set the maximum file size (70MB in this example)
    MAX_FILE_SIZE = 70 * 1000 * 1000

    if 'audioFile' not in request.files:
        return 'No file part',406

    file = request.files['audioFile']

    if file.filename == '':
        return 'No selected file',406

    # Check if the file size is within the limit
    if file.content_length <= MAX_FILE_SIZE:
        if file and allowed_file(file.filename):
        # Perform any necessary processing on the file
        # For example, save it to a folder or perform further actions
        # You can access the file name using file.filename
        # You can access the file content using file.stream.read()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['audio_floder'], filename))
            return 'File uploaded successfully',200
        else:
            return 'File support .wav and .mp3 File size  maximum limit of 70 MB.',406
        



    return 'Invalid file type',406

def allowed_file(filename):
    # Check if the file has an allowed extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3', 'wav'}


# Define the number of items per page
#ITEMS_PER_PAGE = 10

@app.route('/viewmusic', methods=['GET'])
def view_audio():
    return viewfiles(audio_floder,5)

@app.route('/viewweightsmodel', methods=['GET'])
def view_weightsmodel():
    return viewfiles(weightsmodel_floder,5)

def viewfiles(path,filesperpage):
    # Get the current page from the query parameters or set it to 1
    page = request.args.get('page', 1, type=int)

    # Get all files in the folder
    #audio_folder = os.path.join(os.getcwd(), 'audios')
    file_names = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # Paginate the file names
    pagination = Pagination(page=page, total=len(file_names), per_page=filesperpage, bs_version=4)

    # Get the current page of file names
    current_files = file_names[(page - 1) * filesperpage: page * filesperpage]

    # Render the template with the paginated file names
    return render_template('tableviewfiles.html', file_names=current_files, pagination=pagination)

@app.route('/renamefile', methods=['PUT'])
def renamefile():
    #rename_files_by_extension
    current_filename = request.args.get('currentfilename')
    new_filename = request.args.get('newfilename')
    # Split the filename and extension
    name, extension = os.path.splitext(new_filename)
    # Create a new filename based on the extension
                                #new_filename = extension[1:] + '_' + name + extension
    new_filename = name + extension
    #return f'{new_filename}',200
    return func_rename( current_filename,new_filename,audio_floder)

def func_rename(current_name,new_name,pathfile):
    # Full path to the file
    current_path = os.path.join(pathfile, current_name)
    new_path = os.path.join(pathfile, new_name)

    try:
        # Rename the file
        os.rename(current_path, new_path)
        return jsonify(f"File '{current_name}' has been renamed to '{new_name}' in the 'audios' directory."),200

    except FileNotFoundError:
        return (f"Error: The file '{current_name}' does not exist in the 'audios' directory.")
    except PermissionError:
        return (f"Error: Permission denied. Check if you have the necessary permissions.")
    except Exception as e:
        return (f"An unexpected error occurred: {e}")
    


@app.route('/removefile', methods=['DELETE'])
def delfile():
    return viewfiles(audio_floder,5)


# main driver function
if __name__ == '__main__':
    #test()
    app.run(host='192.168.1.50', port=5555, debug=True)


