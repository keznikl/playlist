import gdata.youtube
import gdata.youtube.service
import gdata.alt.appengine

yt_service = gdata.youtube.service.YouTubeService()
gdata.alt.appengine.run_on_appengine(yt_service)

# The YouTube API does not currently support HTTPS/SSL access.
yt_service.ssl = False

def YoutubeSearch(videoid):
	return yt_service.GetYouTubeVideoEntry(video_id=videoid)
	

def YoutubeIdFromURL(url):
	ytIDlen = 11
	idStarts = url.find("?v=")
	if idStarts < 0:
		return None
	idStarts += 3
	return url[idStarts:idStarts+ytIDlen]
