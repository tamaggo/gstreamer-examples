#!/usr/bin/env python
# -*- coding: utf-8
# Record from an RTSP stream containing subtitles, save in an mp4 file

"""

TODO:

- investigate why subtitles are not synchronized
- understand why we need to re-encode the h264

"""

import sys, os, time, re, time

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

if __name__ == '__main__':
	GObject.threads_init()
	Gst.init(None)

	pipeline = Gst.parse_launch("""
	 mp4mux name=mux ! filesink location=capture.mp4
	 rtspsrc location=rtsp://localhost:3002/test latency=0 name=d
	 d. ! capsfilter caps="application/x-rtp,media=video" ! queue ! rtph264depay ! avdec_h264 ! x264enc bitrate=2100 threads=4 ! mux.video_0
	 d. ! capsfilter caps="application/x-rtp,media=audio" ! queue ! rtpmp4adepay ! mux.audio_0
	 d. ! capsfilter caps="application/x-rtp,media=application" ! queue ! rtpgstdepay ! mux.subtitle_0
	""")

	pipeline.set_state(Gst.State.PLAYING)

	t0 = time.time()
	bus = pipeline.get_bus()
	while True:
		msg = bus.poll(Gst.MessageType.ANY, int(1e6))
		if msg is None:
			if time.time() - t0 > 10:
				print("break")
				pipeline.send_event(Gst.Event.new_eos())
				pipeline.set_state(Gst.State.NULL)
				break
			continue
		t = msg.type
		if t == Gst.MessageType.EOS:
			print("EOS")
			break
			pipeline.set_state(Gst.State.NULL)
		elif t == Gst.MessageType.ERROR:
			err, debug = msg.parse_error()
			print("Error: %s" % err, debug)
			break
		elif t == Gst.MessageType.WARNING:
			err, debug = msg.parse_warning()
			print("Warning: %s" % err, debug)
		elif t == Gst.MessageType.STATE_CHANGED:
			pass
		elif t == Gst.MessageType.STREAM_STATUS:
			pass
		else:
			print(t)
			print("Unknown message: %s" % msg)

	print("Bye bye ;)")
