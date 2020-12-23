import numpy as np
import cv2
import pretty_midi as pm
import os
import copy

INDEX_TO_NOTENUMBER = 21 #0から87にこれを足すとmidiのノートナンバーになる

def EdgeDetection(inputFileName,outputFileName):
	path = './files/images'
	img = cv2.imread(os.path.join(path,inputFileName)) #画像読み込み
	img2 = cv2.resize(img,dsize = (round((88 / img.shape[0]) * img.shape[1]),88))
	gray_img = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) #グレースケールに変換
	edge_img = cv2.Canny(gray_img,50,200) #エッジ検出。
	cv2.imwrite(os.path.join(path,outputFileName),edge_img)
	
def OptToRyukyu(inputFileName,outputFileName):
	path = './files/images'
	img = cv2.imread(os.path.join(path,inputFileName)) #画像読み込み
	n = 0
	while (12 * n + 11 < 88):       #画像の輝度値を琉球音階に適応
		for i in range(img.shape[1]):
			img.itemset((12 * n,i,0),0)
			img.itemset((12 * n + 1,i,0),0)
			img.itemset((12 * n + 4,i,0),0)
			img.itemset((12 * n + 5,i,0),0)
			img.itemset((12 * n + 6,i,0),0)
			img.itemset((12 * n + 9,i,0),0)
			img.itemset((12 * n + 11,i,0),0)
			img.itemset((12 * n,i,1),0)
			img.itemset((12 * n + 1,i,1),0)
			img.itemset((12 * n + 4,i,1),0)
			img.itemset((12 * n + 5,i,1),0)
			img.itemset((12 * n + 6,i,1),0)
			img.itemset((12 * n + 9,i,1),0)
			img.itemset((12 * n + 11,i,1),0)
			img.itemset((12 * n,i,2),0)
			img.itemset((12 * n + 1,i,2),0)
			img.itemset((12 * n + 4,i,2),0)
			img.itemset((12 * n + 5,i,2),0)
			img.itemset((12 * n + 6,i,2),0)
			img.itemset((12 * n + 9,i,2),0)
			img.itemset((12 * n + 11,i,2),0)
		n = n + 1
		
	for i in range(img.shape[1]):
		for j in range(img.shape[0]):
			if img.item(j,i,0) == 0:
				img.itemset((j,i,0),204)
				img.itemset((j,i,1),204)
				img.itemset((j,i,2),204) #カラーコード:c0c0c0
				
	cv2.imwrite(os.path.join(path,outputFileName),img)

def ImageToScore(inputFileName,outputFileName):
	path = './files/images'
	img = cv2.imread(os.path.join(path,inputFileName)) #画像読み込み
	photo_score = pm.PrettyMIDI() #Pretty_MIDIオブジェクトの生成
	js_harp = pm.Instrument(107) #琴(107)の楽譜インスタンスを生成
	start_second = 0 #開始時間
	end_second = 0.5 #終了時間
	for i in range(img.shape[1]):
		for j in range(img.shape[0]):
			if img.item(j,i,0) == 255:
				note = pm.Note(100,j + INDEX_TO_NOTENUMBER,start_second,end_second) #速度、音程、開始時間、終了時間を設定
				js_harp.notes.append(note)
		photo_score.instruments.append(js_harp)
		start_second = start_second + 0.5
		end_second = end_second + 0.5
	photo_score.write(os.path.join('./files/sounds',outputFileName))
	
def MakeImages(inputFileName,outputFileName):
	path = './files/images'
	img = cv2.imread(os.path.join(path,inputFileName)) #画像読み込み
	for i in range(img.shape[1]):
		img2 = copy.copy(img)
		for j in range(88):
			if img2.item(j,i,0) == 255:
				img2.itemset((j,i,0),38)
				img2.itemset((j,i,1),9)
				img2.itemset((j,i,2),201) #カラーコード:c90926
		cv2.imwrite(os.path.join(path,outputFileName + str(i) + '.png'),img2)
		
def IMGCols(FileName):
	path = './files/images'
	img = cv2.imread(os.path.join(path,FileName)) #画像読み込み
	return img.shape[1]
	
def Mp4Maker(inputFileName,outputFileName,cols):
	CLIP_FPS = 2.01
	path = './files/images'
	filepath = os.path.join(path,outputFileName)
	w = cols
	h = 88
	codec = cv2.VideoWriter_fourcc('m','p','4','v')
	video = cv2.VideoWriter(filepath, codec, CLIP_FPS, (w, h))
	for i in range(cols):
		img = cv2.imread(os.path.join(path,inputFileName + str(i) + '.png'))
		if img is None:
			print('cannot read')
			break
		video.write(img)
	video.release()
		
		
				
		
	
		