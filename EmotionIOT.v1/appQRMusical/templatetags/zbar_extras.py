from django import template
import subprocess
import os

from appQRMusical import global_vars

register = template.Library()


@register.simple_tag

def stop_cam():
	print("Stop Cam")

	if global_vars.zbar_status != None:
		os.system("ps -A | grep zbar| awk '{print $1}' | xargs kill -9 $1")
		global_vars.zbar_status = None
		#global_vars.message = 'Get close QR code to cam'
		global_vars.cam = 1

@register.simple_tag
def restart_game_vars():

	#print("Reset game's global vars")

	global_vars.game_fail = 0
	global_vars.game_success = 0
	global_vars.game_initialized = False
	global_vars.last_message = global_vars.message
	global_vars.message_alert = "alert-info"
	global_vars.game_image = "/files/static/Who.png"
	global_vars.game_image = ""
	global_vars.game_file = ""
	global_vars.game_display = "none"
	global_vars.message = 'Get close QR code to cam'
