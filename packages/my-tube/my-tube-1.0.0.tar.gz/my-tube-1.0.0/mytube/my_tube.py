import os
import sys
from pytube import YouTube
from pytube.cli import on_progress

class Video:

	@classmethod
	def tela_clean(cls):
		if sys.platform == "win32":
			os.system("cls")
		elif sys.platform == "linux":
			os.system("clear")

	@classmethod
	def carregar_video(cls,link_url):
		global video
		video = YouTube(link_url,on_progress_callback=on_progress)

	@staticmethod
	def mostrar_titulo():
		print("Nome do vídeo a ser baixado é: {}".format(video.title))

	@staticmethod
	def baixar_video():
		stream = video.streams.get_highest_resolution()
		stream.download(output_path="Videos")
# end