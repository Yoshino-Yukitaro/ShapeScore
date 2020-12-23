from flask import Flask, flash, redirect, request, url_for
from flask import render_template, send_file
from werkzeug.utils import secure_filename
import werkzeug
import moviepy.editor as mp
import os, time, uuid
import score_maker
import midi_to_mp3

UPLOAD_FOLDER = './files/images' #画像の保存先
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} #許可する拡張子
global scoreName #スコープ拡張のため
scoreName = ''
global cols
cols = 0

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 #ファイル容量は5MBまで

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST','GET'])
def index():
	if request.method == 'POST':
		upfile = request.files.get('upfile')
		kind = request.form.get('kind')
		if upfile is None:
			flash('No File Part')
			return redirect('/')
			
		if upfile.filename == '':
			flash('No selected file')
			return redirect('/')
			
		if kind is None:
			flash('No kinds of music')
			return redirect('/')
			
		if allowed_file(upfile.filename):
			filename = secure_filename(upfile.filename)
			upfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			id = 'IM_' + uuid.uuid4().hex
			score_maker.EdgeDetection(filename,id + '_edge.png')
			if kind == 'ryukyu':
				score_maker.OptToRyukyu(id + '_edge.png',id + '_ryukyu.png')
				scoreName = id + '_ryukyu.'

			score_maker.ImageToScore(scoreName + 'png',scoreName + 'mid')
			score_maker.MakeImages(scoreName + 'png',scoreName)
			midi_to_mp3.midi_to_mp3(scoreName + 'mid',scoreName + 'mp3')
			cols = score_maker.IMGCols(scoreName + 'png')
			score_maker.Mp4Maker(scoreName,scoreName + 'mp4',cols)
			clip = mp.VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], scoreName + 'mp4')).subclip()
			#video = clip.set_audio(mp.AudioFileClip('./files/sounds/' + scoreName + 'mp3'))
			#video.write_videofile(filename = os.path.join(app.config['UPLOAD_FOLDER'], 'second_' + scoreName + 'mp4'), codec = 'mpeg4', audio =  './files/sounds/' + scoreName + 'mp3', audio_codec = 'libmp3lame')
			audioFile = mp.AudioFileClip('./files/sounds/' + scoreName + 'mp3')
			clip.write_videofile(filename = os.path.join(app.config['UPLOAD_FOLDER'], 'second_' + scoreName + 'mp4'), codec = 'mpeg4', audio = audioFile, audio_codec = 'libmp3lame')
			clip.close()
			#video.close()
			return redirect('/viewer')
	return render_template('index.html')
	
@app.route('/viewer')
def viewer():
	return render_template('view.html',image='../files/images/'+scoreName+'png',video='../files/images/'+scoreName+'mp4')
	
@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge) #ファイル容量超過
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'result : file size is overed.'
	
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')

	
