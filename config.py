#
# IPs for different MQTT servers.
# Only uncomment one, depending on which server you desire.
#
# mqtt_server="127.0.0.1"	# loopback
# mqtt_server="172.30.35.102"	# Pat's desk
# mqtt_server="172.30.38.181"	# SURF Pi
mqtt_server="172.17.185.234"     # underwater SURF WSL

#
# IPs for different QTM servers.
# Only uncomment one, depending on which server you desire.
#
# qtm_server="127.0.0.1"	# loopback
# qtm_server="10.0.0.118" # Prof DeVries' environment
# qtm_server="172.30.35.102"	# Pat's desk
# qtm_server="172.30.38.181"	# SURF Pi
# qtm_server="172.17.168.3"     # underwater SURF WSL
qtm_server="172.30.35.229"    # underwater SURF Win10


# pick a unique clientname to prevent collisions with other clients
# Only uncomment one, depending on which server you desire.
# clientname="mydesk"			# Pat's desk
# clientname="surfpi_sub"		# SURF Pi
# clientname="reddwarf"		# submarine
clientname="underwater_qtm"   # SURF underwater NUC


#
# Pick the default folder for environment / OS you're running in.
# Only uncomment one, depending on server configuration.
#
default_folder="/mnt/c/Python/Qualisys_MQTT"		# WSL on Win10
#default_folder="/home/pi/mqtt/"	                # RasPi
#default_folder="/Users/Levi DeVries/Downloads/"    #Win10
