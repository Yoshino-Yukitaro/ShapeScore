from midi2audio import FluidSynth
import os

path = './files/sounds'

def midi_to_mp3(inputFileName,outputFileName):
	fs = FluidSynth(os.path.join(path,'font.sf2')) #サウンドフォントを指定
	fs.midi_to_audio(os.path.join(path,inputFileName), os.path.join(path,outputFileName)) #midiをmp3に変換、保存