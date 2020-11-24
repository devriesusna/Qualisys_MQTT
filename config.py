#
# IPs for different MQTT servers.
# Only uncomment one, depending on which server you desire.
#
# mqtt_server="127.0.0.1"	# loopback
# mqtt_server="172.30.35.102"	# Pat's desk
# mqtt_server="172.30.38.181"	# SURF Pi
# mqtt_server="172.30.35.229"      # underwater SURF Win10
mqtt_server="172.30.35.230"      # overhead SURF Win10

#
# IPs for different QTM servers.
# Only uncomment one, depending on which server you desire.
#
# qtm_server="127.0.0.1"	# loopback
# qtm_server="10.0.0.118" # Prof DeVries' environment
# qtm_server="172.30.35.102"	# Pat's desk
# qtm_server="172.30.38.181"	# SURF Pi
# qtm_server="172.30.35.229"    # underwater SURF Win10
qtm_server="172.30.35.230"      # overhead SURF Win10

# pick a unique clientname to prevent collisions with other clients
# Only uncomment one, depending on which server you desire.
# sub_clientname="mydesk"			# Pat's desk
# sub_clientname="surfpi_sub"		# SURF Pi
# sub_clientname="reddwarf"		# submarine
sub_clientname="overhead_qtm"   # SURF underwater NUC

# pick a unique clientname to prevent collisions with other clients
# Only uncomment one, depending on which server you desire.
# pub_clientname="underwater_qtm"   # SURF underwater NUC
pub_clientname="overhead_pub"   # SURF overhead NUC

#
# Pick the default folder for environment / OS you're running in.
# Only uncomment one, depending on server configuration.
#
default_folder="/mnt/c/Python/Qualisys_MQTT"		# WSL on Win10
#default_folder="/home/pi/mqtt/"	                # RasPi
#default_folder="/Users/Levi DeVries/Downloads/"    #Win10

