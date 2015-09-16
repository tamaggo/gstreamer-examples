#!/usr/bin/env python
# -*- coding:utf-8 vi:ts=4:noexpandtab
# Simple RTSP server. Run as-is or with a command-line to replace the default pipeline

import sys
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

loop = GObject.MainLoop()
GObject.threads_init()
Gst.init(None)

class MyFactory(GstRtspServer.RTSPMediaFactory):
	def __init__(self):
		GstRtspServer.RTSPMediaFactory.__init__(self)

	def do_create_element(self, url):
		s_src = "v4l2src ! video/x-raw,rate=30,width=320,height=240 ! videoconvert ! video/x-raw,format=I420"
		s_h264 = "videoconvert ! vaapiencode_h264 bitrate=1000"
		s_src = "videotestsrc ! video/x-raw,rate=30,width=320,height=240,format=I420"
		s_h264 = "x264enc tune=zerolatency"
		pipeline_str = "( {s_src} ! queue max-size-buffers=1 name=q_enc ! {s_h264} ! rtph264pay name=pay0 pt=96 )".format(**locals())
		if len(sys.argv) > 1:
			pipeline_str = " ".join(sys.argv[1:])
		print(pipeline_str)
		return Gst.parse_launch(pipeline_str)

class GstServer():
	def __init__(self):
		self.server = GstRtspServer.RTSPServer()
		f = MyFactory()
		f.set_shared(True)
		m = self.server.get_mount_points()
		m.add_factory("/test", f)
		self.server.attach(None)

if __name__ == '__main__':
	s = GstServer()
	loop.run()

