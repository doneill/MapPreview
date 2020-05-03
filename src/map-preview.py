# -*- encoding: UTF-8 -*-
import codecs
import os
import sublime
import sublime_plugin
import webbrowser

def log(msg):

    print("MapPreview: %s" % msg)

def save_utf8(filename, text):

    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)
        f.close

def get_temp_preview_path(view):

    tmp_filename = '%s.html' % view.id()
    tmp_dir = os.path.dirname(view.file_name())

    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_fullpath = os.path.join(tmp_dir, tmp_filename)
    return tmp_fullpath

class PreviewCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view

        geojson = view.substr(sublime.Region(0, view.size()))

        messageBegin = """
          <html>
            <head>
              <title>ST-Map Preview</title>
              <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
                integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
                crossorigin=""/>
              <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"
                integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew=="
                crossorigin=""></script>
              <style>
                #map{ height: 100% }
              </style>
            </head>
            <body>
              <div id="map"></div>
              <script>
                mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
                var tiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; ' + mapLink + ' Contributors'
               });
        """

        geojsonFeature = "    var geojsonFeature = {};".format(geojson)

        messageEnd = """
              var map = L.map('map');
              tiles.addTo(map);
              L.geoJSON(geojsonFeature).addTo(map);
              map.fitBounds(L.geoJSON(geojsonFeature).getBounds())
            </script>
          </body>
        </head>
        """

        html = messageBegin + geojsonFeature + messageEnd

        # update output HTML file
        tmp_fullpath = get_temp_preview_path(self.view)
        save_utf8(tmp_fullpath, html)

        webbrowser.open_new_tab("file:///" + tmp_fullpath)
