from flask import Flask, request
import re, json
from face_util import compare_faces, face_rec

app = Flask(__name__)


@app.route('/face_match', methods=['POST'])
def face_match():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file1' in request.files) and ('file2' in request.files):
            file1 = request.files.get('file1')
            file2 = request.files.get('file2')
            ret = compare_faces(file1, file2)
            resp_data = {"match": bool(ret)}  # convert numpy._bool to bool for json.dumps
            return json.dumps(resp_data)


def print_request(request):
    # Print request url
    print(request.url)
    # print relative headers
    print('content-type: "%s"' % request.headers.get('content-type'))
    print('content-length: %s' % request.headers.get('content-length'))
    # print body content
    body_bytes = request.get_data()
    # replace image raw data with string '<image raw data>'
    body_sub = re.sub(b'(\r\n\r\n)(.*?)(\r\n--)', br'\1<image raw data>\3', body_bytes, flags=re.DOTALL)
    print(body_sub.decode('utf-8'))


@app.route('/face_rec', methods=['POST', 'GET'])
def face_recognition():
    if request.method == 'POST':
        print_request(request)
        # check if the post request has the file part
        if 'file' in request.files:
            file = request.files.get('file')
            name = face_rec(file)
            resp_data = {'name': name}
            return json.dumps(resp_data)

    return '''
   <!DOCTYPE html>
<html>
  <head>
    <title>
      HTML Webcam Capture Demo
    </title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <script src="1-basics.js"></script>
    <style>
      #vid-show, #vid-canvas, #vid-take {
        display: block;
        margin-bottom: 20px;
      }
      html, body {
        padding: 0;
        margin: 0;
      }
    </style>
  </head>
  <body>
    <div id="vid-controls">
      <video id="vid-show" autoplay></video>
      <input id="vid-take" type="button" value="Take Photo"/>
      <div id="vid-canvas"></div>

        <script>
        
          window.addEventListener("load", function(){
  // [1] GET ALL THE HTML ELEMENTS
  var video = document.getElementById("vid-show"),
      canvas = document.getElementById("vid-canvas"),
      take = document.getElementById("vid-take");

  // [2] ASK FOR USER PERMISSION TO ACCESS CAMERA
  // WILL FAIL IF NO CAMERA IS ATTACHED TO COMPUTER
  navigator.mediaDevices.getUserMedia({ video : true })
  .then(function(stream) {
    // [3] SHOW VIDEO STREAM ON VIDEO TAG
    video.srcObject = stream;
    video.play();

    // [4] WHEN WE CLICK ON "TAKE PHOTO" BUTTON
    take.addEventListener("click", function(){
      // Create snapshot from video
      var draw = document.createElement("canvas");
      draw.width = video.videoWidth;
      draw.height = video.videoHeight;
      var context2D = draw.getContext("2d");
      context2D.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
      // Output as file
      var anchor = document.createElement("a");
      anchor.href = draw.toDataURL("image/png");
      anchor.download = "webcam.png";
      anchor.innerHTML = "Click to download";
      canvas.innerHTML = "";
      canvas.appendChild(anchor);
    });
  })
  .catch(function(err) {
    document.getElementById("vid-controls").innerHTML = "Please enable access and attach a camera";
  });
});
      </script>
   

    <title>Face Recognition</title>
    <h1>Upload an image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Login> 
    </form>
    
        </div>
  </body>
</html>  
    '''
#since im using my localhost
app.run(debug=True)

#if you using a web host use follow
#app.run(host='0.0.0.0', port='5001', debug=True)
