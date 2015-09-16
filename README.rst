##################
Gstreamer examples
##################

This is a collection of generic gstreamer (1.x) usage examples that can be useful.


Usage
#####


Preparation
***********

Python code uses OpenCV (``cv2``), numpy, and the gstreamer bindings (GObject-introspection).


Running the Code
****************

You'll find the following examples:

.. list-table::

   * - Name
     - Description

   * - ``test_gst_appsrc_testvideo_mp4mux.py``
     - Demonstrates how to create a synthetic test video, that can be used
       to test synchronization features.

   * - ``test_gst_rtsp_subtitles_server.py``
     - gst-rtsp-server demo, offering subtitles

   * - ``test_gst_rtsp_subtitles_client.py``
     - client for ``test_gst_rtsp_subtitles_server.py``

   * - ``test_gst_rtsp_server.py``
     - Server for ``gst-launch-1.0 playbin uri=rtsp://localhost:8554/test``
       or ``gst-launch-1.0 rtspsrc location=rtsp://localhost:8554/test latency=50 ! decodebin ! autovideosink``

License
#######

MIT license; see the accompanying LICENSE file.

