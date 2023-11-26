import  torch, os, traceback, sys, warnings, shutil, numpy as np

now_dir = os.getcwd()
#parent_directory = os.path.abspath()
sys.path.append(now_dir)
tmp = os.path.join(now_dir , "TEMP")
shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/infer_pack" % (os.path.join(now_dir, "infer_pack")), ignore_errors=True)
os.makedirs(tmp, exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), "logs"), exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), "weights"), exist_ok=True)
os.environ["TEMP"] = tmp
warnings.filterwarnings("ignore")
torch.manual_seed(114514)
import ffmpeg


from infer_pack.models import (   #in get vc
    SynthesizerTrnMs256NSFsid,
    SynthesizerTrnMs256NSFsid_nono,
    SynthesizerTrnMs768NSFsid,
    SynthesizerTrnMs768NSFsid_nono,
)
from fairseq import checkpoint_utils
import logging
from .vc_infer_pipeline import VC
from .config import Config
from .my_utils import load_audio  #Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
config = Config()
logging.getLogger("numba").setLevel(logging.WARNING)

hubert_model = None
def load_hubert():
    """Load hubert file"""
    global hubert_model
    models, _, _ = checkpoint_utils.load_model_ensemble_and_task(
        ["hubert_base.pt"],
        suffix="",
    )
    hubert_model = models[0]
    hubert_model = hubert_model.to(config.device)
    if config.is_half:
        hubert_model = hubert_model.half()
    else:
        hubert_model = hubert_model.float()
    hubert_model.eval()

#load pth and index
weight_root = "weights"
index_root = "logs"
names = []
for name in os.listdir(weight_root):
    if name.endswith(".pth"):
        names.append(name)
        print(names)
index_paths = []
for root, dirs, files in os.walk(index_root, topdown=False):
    for name in files:
        if name.endswith(".index") and "trained" not in name:
            index_paths.append("%s/%s" % (root, name))
            print(index_paths)



def vc_single(
    sid,
    input_audio_path,
    f0_up_key,
    f0_file,
    f0_method,
    file_index,
    #file_index2,
    # file_big_npy,
    index_rate,
    filter_radius,
    resample_sr,
    rms_mix_rate,
    protect,
    crepe_hop_length,
):  # spk_item, input_audio0, vc_transform0,f0_file,f0method0
    global tgt_sr, net_g, vc, hubert_model, version
    if input_audio_path is None:
        return "You need to upload an audio", None
    f0_up_key = int(f0_up_key)
    try:
        audio = load_audio(input_audio_path, 16000)
        audio_max = np.abs(audio).max() / 0.95
        if audio_max > 1:
            audio /= audio_max
        times = [0, 0, 0]
        if hubert_model == None:
            load_hubert()
        if_f0 = cpt.get("f0", 1)
        file_index = (
            (
                file_index.strip(" ")
                .strip('"')
                .strip("\n")
                .strip('"')
                .strip(" ")
                .replace("trained", "added")
            )
        )  # 防止小白写错，自动帮他替换掉
        # file_big_npy = (
        #     file_big_npy.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        # )
        audio_opt = vc.pipeline(
            hubert_model,
            net_g,
            sid,
            audio,
            input_audio_path,
            times,
            f0_up_key,
            f0_method,
            file_index,
            # file_big_npy,
            index_rate,
            if_f0,
            filter_radius,
            tgt_sr,
            resample_sr,
            rms_mix_rate,
            version,
            protect,
            crepe_hop_length,
            f0_file=f0_file,
        )
        if resample_sr >= 16000 and tgt_sr != resample_sr:
            tgt_sr = resample_sr
        index_info = (
            "Using index:%s." % file_index
            if os.path.exists(file_index)
            else "Index not used."
        )
        return "Success.\n %s\nTime:\n npy:%ss, f0:%ss, infer:%ss" % (
            index_info,
            times[0],
            times[1],
            times[2],
        ), (tgt_sr, audio_opt)
    except:
        info = traceback.format_exc()
        print(info)
        return info, (None, None)








#get model pth in floder weight  load all  
def get_vc(sid):
    global n_spk, tgt_sr, net_g, vc, cpt, version
    if sid == "" or sid == []:
        global hubert_model
        if hubert_model != None:  # 考虑到轮询, 需要加个判断看是否 sid 是由有模型切换到无模型的
            print("clean_empty_cache")
            del net_g, n_spk, vc, hubert_model, tgt_sr  # ,cpt
            hubert_model = net_g = n_spk = vc = hubert_model = tgt_sr = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            ###楼下不这么折腾清理不干净
            if_f0 = cpt.get("f0", 1)
            version = cpt.get("version", "v1")
            if version == "v1":
                if if_f0 == 1:
                    net_g = SynthesizerTrnMs256NSFsid(
                        *cpt["config"], is_half=config.is_half
                    )
                else:
                    net_g = SynthesizerTrnMs256NSFsid_nono(*cpt["config"])
            elif version == "v2":
                if if_f0 == 1:
                    net_g = SynthesizerTrnMs768NSFsid(
                        *cpt["config"], is_half=config.is_half
                    )
                else:
                    net_g = SynthesizerTrnMs768NSFsid_nono(*cpt["config"])
            del net_g, cpt
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            cpt = None
        return {"visible": False, "__type__": "update"}
    person = "%s/%s" % (weight_root, sid)
    print("loading %s" % person)   #load model select
    cpt = torch.load(person, map_location="cpu")
    tgt_sr = cpt["config"][-1]
    cpt["config"][-3] = cpt["weight"]["emb_g.weight"].shape[0]  # n_spk
    if_f0 = cpt.get("f0", 1)
    version = cpt.get("version", "v1")
    if version == "v1":
        if if_f0 == 1:
             net_g = SynthesizerTrnMs256NSFsid(*cpt["config"], is_half=config.is_half)
        else:
             net_g = SynthesizerTrnMs256NSFsid_nono(*cpt["config"])
    elif version == "v2":
         if if_f0 == 1:
             net_g = SynthesizerTrnMs768NSFsid(*cpt["config"], is_half=config.is_half)
         else:
             net_g = SynthesizerTrnMs768NSFsid_nono(*cpt["config"])
    del net_g.enc_q
    print(net_g.load_state_dict(cpt["weight"], strict=False))
    net_g.eval().to(config.device)
    if config.is_half:
        net_g = net_g.half()
    else:
        net_g = net_g.float()
    vc = VC(tgt_sr, config)
    n_spk = cpt["config"][-3]
    return {"visible": False, "maximum": n_spk, "__type__": "update"}





def clean():
    return {"value": "", "__type__": "update"}






import re as regex
import scipy.io.wavfile as wavfile

#cli_current_page = "HOME"

def cli_split_command(com):
    exp = r'(?:(?<=\s)|^)"(.*?)"(?=\s|$)|(\S+)'
    split_array = regex.findall(exp, com)
    split_array = [group[0] if group[0] else group[1] for group in split_array]
    print(split_array)
    return split_array

def execute_generator_function(genObject):
    for _ in genObject: pass

def cli_infer(com):
    # get VC first
    com = cli_split_command(com)
    model_name = com[0]
    source_audio_path = com[1]
    output_file_name = com[2]
    feature_index_path = com[3]
    f0_file = None # Not Implemented Yet

    # Get parameters for inference
    speaker_id = int(com[4])
    transposition = float(com[5])
    f0_method = com[6]
    crepe_hop_length = int(com[7])
    harvest_median_filter = int(com[8])
    resample = int(com[9])
    mix = float(com[10])
    feature_ratio = float(com[11])
    protection_amnt = float(com[12])


    print("Mangio-RVC-Fork Infer-CLI: Starting the inference...")
    vc_data = get_vc(model_name)
    print(vc_data)
    print("Mangio-RVC-Fork Infer-CLI: Performing inference...")
    conversion_data = vc_single(
        speaker_id,
        source_audio_path,
        transposition,
        f0_file,
        f0_method, 
        feature_index_path,
        feature_ratio,
        harvest_median_filter,
        resample,#5
        mix,
        protection_amnt,
        crepe_hop_length,        
    )
    if "Success." in conversion_data[0]:
        print("Mangio-RVC-Fork Infer-CLI: Inference succeeded. Writing to %s/%s..." % ('audio-outputs', output_file_name))
        wavfile.write('%s/%s' % ('audio-outputs', output_file_name), conversion_data[1][0], conversion_data[1][1])
        #print("Mangio-RVC-Fork Infer-CLI: Finished! Saved output to %s/%s" % ('audio-outputs', output_file_name))
        return "Mangio-RVC-Fork Infer-CLI: Finished! Saved output to %s/%s" % ('audio-outputs', output_file_name)
    else:
        print("Mangio-RVC-Fork Infer-CLI: Inference failed. Here's the traceback: ")
        print(conversion_data[0])



#vc_single(int(0),'./audios/someguy.mp3',float(12),None,'dio','./logs/serana700_e200_s7200\serana700_v2.index',float(0.0),int(0),int(50),float(0.0),float(0.0),int(10))
# sample_command = '"serana700_e200_s7200.pth" "./audios/someguy.mp3" "output_audio.wav" "./logs/serana700_e200_s7200\serana700_v2.index" 0 12 "dio" 120 5  5 0.0  0.0 0.0'
# nani = cli_infer(sample_command)         
                
# from flask import Flask,jsonify,request
# from flask_ngrok2 import run_with_ngrok
# import subprocess
# from flask_cors import CORS


#sample_command = '"serana/serana700_e200_s7200.pth" "./audios/someguy.mp3" "output_audio.wav" "./logs/serana700_e200_s7200\serana700_v2.index" 0 12 "dio" 120 5  5 0.0  0.0 0.0'
#nani = cli_infer(sample_command) 
#get_vc("serana/serana700_e200_s7200.pth")
#get_vc([])

# app = Flask(__name__)
# cors = CORS(app)
# '''Token ngrok '''
# run_with_ngrok(app=app, auth_token="2TzDxTPxT4PsN12y1dTd4RAjz1A_4QQQ9bAUrJ1uS6kmmKnJ4")

# ##################### MODULE #####################################
# '''This is module for chat '''

# def process_chat(getinstruction,getinput,getmodel_name):
#   try :
#     print('chat processing')

#     return 'Error'
#   except Exception as e:
#     return  {"Error": e}




# @app.route("/test", methods=["POST"])
# def test():
#   try:

#       content_type = request.headers.get('Content-Type')
#       if (content_type == 'application/json'):
#         print('yes')
#         json = request.json
#         print(json)

#         if (json):
#           result = process_chat(json['instruction'], json['input'],json['model'])
#           return {'output': result }
#         else:
#           return {'output': 'Error' }
#   except Exception as e:
#       print(e)
#       return {
#         "Error": e,
#       }

# @app.route("/nani", methods=["GET"])
# def nani():
#   try:

#     content_type = request.headers.get('Content-Type')
#     #sample_commands = "serana700_e200_s7200.pth output_audio.wav feature_index_path 1 0.5 f0_method 256 5 44100 0.8 1.0 0.2"
#     sample_command = '"serana700_e200_s7200.pth" "./audios/someguy.mp3" "output_audio.wav" "./logs/serana700_e200_s7200\serana700_v2.index" 0 12 "pm" 120 5  5 0.0  0.0 0.0'

#     nani = cli_infer(sample_command) 
#     return {'output':  nani  }
#     #   if (content_type == 'application/json'):
#     #     print('yes')
#     #     json = request.json
#     #     print(json)

#     #     if (json):
#     #       result = process_chat(json['instruction'], json['input'],json['model'])
#           #return {'output': result }
#   except Exception as e:
#       print(e)
#       return {
#         "Error": e,
#       }

# if __name__ == '__main__':
#     app.run()
