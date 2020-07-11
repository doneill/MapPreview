# -*- encoding: UTF-8 -*-
import codecs
import os
import json
import MapPreview.webmap as wm
import sublime
import sublime_plugin
import tempfile
import webbrowser

def log(msg):
    print("MapPreview: %s" % msg)

def save_utf8(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)
        f.close

def get_temp_preview_path(view):
    settings = sublime.load_settings('MapPreview.sublime-settings')

    tmp_filename = '%s.html' % view.id()
    if settings.get('path_tempfile'):
        if os.path.isabs(settings.get('path_tempfile')):  # absolute path or not
            tmp_dir = settings.get('path_tempfile')
        else:
            tmp_dir = os.path.join(os.path.dirname(view.file_name()), settings.get('path_tempfile'))
    else:
        tmp_dir = tempfile.gettempdir()

    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)

    tmp_fullpath = os.path.join(tmp_dir, tmp_filename)
    return tmp_fullpath

class PreviewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        viewText = view.substr(sublime.Region(0, view.size()))

        try:
            # ensure we have json from view
            validateJson = json.loads(viewText)
            # check if json valid spatial type
            if "type" in validateJson:
                # check if valid GeoJSON
                if validateJson["type"] == "FeatureCollection":
                    type = "geojson"
                    html = wm.render(viewText, type)
                else:
                    type = "topojson"
                    html = wm.render(viewText, type)

                # update output HTML file
                tmp_fullpath = get_temp_preview_path(view)
                save_utf8(tmp_fullpath, html)

                webbrowser.open_new_tab("file:///" + tmp_fullpath)

            else:
                sublime.error_message("Could not convert file.\n\n Not valid spatial type")
        except Exception as ex:
            sublime.error_message("Could not convert file.\n\n %s" % ex)
