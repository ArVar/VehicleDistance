from flask import Flask, redirect, url_for, request, render_template, Response
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from webapp import VehicleDistance
import cv2

 
camera_id = {}
app = Flask(__name__)
@app.route("/" ) 
def main():
    
    return render_template("index.html")

def gen(camera):

    make_video_file = 10 # Make video of first n frames

    if make_video_file > 0:
        fc = 0
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (camera.width, camera.height))

    while True: 
        jpg_bytestream, frame = camera.main()
        if jpg_bytestream != "":
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytestream + b'\r\n\r\n')
        
        if make_video_file > 0:
            if fc <= make_video_file:
                out.write(frame)
                fc = fc + 1
            elif fc == make_video_file + 1:
                out.release()


@app.route('/video_feed/<path:streamPath>')
def video_feed(streamPath):
    if not streamPath:
        id = 'rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa'
    else:
        id = str(streamPath)
    #id = 'https://www.youtube.com/watch?v=EbyOoMg191Y'
    #id  = 2    # Webcam with id 2
    if int(id) in range(10):
        id = int(id)
        
    return Response(gen(VehicleDistance(id)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_response', methods = ['POST']) 
def get_response():
    json = request.get_json()
    print(json)
    if json is not None:
        h = json['status']
        print(h)  
    return print(camera_id)
    
if __name__ == '__main__':
    # Serve the app with gevent
    app.run(host='0.0.0.0', threaded=True, debug = True)