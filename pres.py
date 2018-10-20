import pypresence
import time
from config import credents
from plexapi.myplex import MyPlexAccount


def process_alert(data):
	if (data.get("type") == "playing"):
		print("playing")
		session_data = data.get('PlaySessionStateNotification', [])[0]
		state = session_data.get('state', 'stopped')
		session_key = session_data.get('sessionKey', None)
		rating_key = session_data.get('ratingKey', None)
		view_offset = session_data.get('viewOffset', 0)
		if session_key and session_key.isdigit():
			session_key = int(session_key)
		else:
			return
		if rating_key and rating_key.isdigit():
			rating_key = int(rating_key)
		else:
			return
		metadata = plex.fetchItem(rating_key)
		media_type = metadata.type

		if (media_type == "movie"):
			title = metadata.title
			activity = "Watching A Movie"
			#get timestamp info, plex API seems to send every 5 seconds
			if (state == "playing"):
				timestamp = str(time.strftime("%Hh %Mm %Ss", time.gmtime(view_offset / 1000)))
			else:
				timestamp = str(time.strftime("%Hh %Mm %Ss", time.gmtime(view_offset / 1000))) + "/" + str(time.strftime("%Hh %Mm %Ss", time.gmtime(metadata.duration / 1000)))
		elif (media_type == "episode"):
			title = f'{metadata.grandparentTitle} - {metadata.title}'
			subtitle = f'S{metadata.parentIndex} · E{metadata.index}'
		RPC.update(state=timestamp, 
			details = title,
			large_image = "plex",
			large_text = activity,
			small_image = "plex",
			small_text = activity)


if __name__ == "__main__":
	client_id = credents.CONFIG["client_id"]
	PLEX_USERNAME = credents.CONFIG["PLEX_USERNAME"]
	PLEX_PASSWORD = credents.CONFIG["PLEX_PASSWORD"]
	PLEX_SERVER = credents.CONFIG["PLEX_SERVER"]
	RPC = pypresence.Presence(client_id)
	RPC.connect()
	account = MyPlexAccount(PLEX_USERNAME, PLEX_PASSWORD)
	plex = account.resource(PLEX_SERVER).connect()
	print(account)
	plex_admin = (account.email == plex.myPlexUsername or account.username == plex.myPlexUsername)
	plex.startAlertListener(process_alert)
	try:
		while True:
			time.sleep(3600)
			continue
	except KeyboardInterrupt:
		print("Exiting Discord RPC")
