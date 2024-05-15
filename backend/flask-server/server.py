from flask import Flask, request
import dynamo
from flask_cors import CORS, cross_origin
import pipeline


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/site", methods = ["GET"])
@cross_origin()
def site():
    path = '../shazam-temalab-2024/xd.wav'
    list = pipeline.pipeline_func_list(path)
    return dynamo.searchinDict(list)
@app.route("/zene", methods = ["GET","POST"])
@cross_origin()
def zene():
   uploadAudio(request)
   return {"g":["asd"]}

def uploadAudio(request):

  # Get params
  audio_file = request.files.get('audio_data')
  file_type = request.form.get("type", "wav")
  
  # You may want to create a uuid for your filenames
  filename = "myAudioFile." + file_type
  
  # Save it on your local disk
  target_path = ("xd.wav")
  audio_file.save(target_path)


  


if __name__ == "__main__":
    app.run(debug=False)