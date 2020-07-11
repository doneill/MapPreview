def render(data, type):
    messageBegin = """
    <html>
      <head>
        <title>Map Preview</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
          integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
          crossorigin=""/>

          <style>
              .info { padding: 6px 8px; font: 12px/14px Arial, Helvetica, sans-serif; background: white; background: rgba(255,255,255,0.8); box-shadow: 0 0 15px rgba(0,0,0,0.2); border-radius: 5px; } .info h4 { margin: 0 0 5px; color: #777; }
          </style>

        <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"
          integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew=="
          crossorigin=""></script>
          <script src="http://d3js.org/topojson.v1.min.js"></script>
          <script src="https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"></script>
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
        var info = L.control();
    """
    if type == "geojson":
        feature = "    var geojsonFeature = {};".format(data)

        messageEnd = """
              var map = L.map('map');
              tiles.addTo(map);
              var layerGroup = L.geoJSON(geojsonFeature, {
                  onEachFeature: function (feature, layer) {
                      layer.on({
                        'mouseover': featureProps
                      });
                  }
              }).addTo(map);

              map.fitBounds(L.geoJSON(geojsonFeature).getBounds())

              function featureProps(e) {
                  var layer = e.target;
                  props = layer.feature.properties;
                  attrs = Object.keys(props);
                  var str = '';
                  for (var i = 0; i < attrs.length; i += 1) {
                      attribute = attrs[i];
                      value = props[attribute];
                      str += '<b>' + attribute + '</b> : ' + value + '<br>'
                  }

                  layer.bindPopup(str);
              }

              info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info');

                this._div.innerHTML = ('Layer Type: GeoJSON');

                return this._div;
              };

              info.addTo(map);
            </script>
          </body>
        </head>
        """
    else:
        feature = "    var topojsonFeature = {};".format(data)

        messageEnd = """
              L.TopoJSON = L.GeoJSON.extend({
                addData: function(jsonData) {
                  if (jsonData.type === "Topology"){
                    for (key in jsonData.objects){
                      geojson = topojson.feature( jsonData, jsonData.objects[key]);
                      L.GeoJSON.prototype.addData.call(this, geojson);
                    }
                  }
                  else{
                    L.GeoJSON.prototype.addData.call(this, jsonData);
                  }
                }
              });

              var map = L.map('map',
                  colorScale = chroma
                  .scale(['#fafa6e','#2A4858'])
                  .domain([0,1]));

              tiles.addTo(map);

              topoLayer = new L.TopoJSON();
              topoLayer.addData(topojsonFeature);
              topoLayer.addTo(map);
              topoLayer.eachLayer(styleLayer)

              map.fitBounds(topoLayer.getBounds())

              function styleLayer(layer){
                  var randomValue = Math.random(),
                  fillColor = colorScale(randomValue).hex();
                  layer.setStyle({
                      fillColor : fillColor,
                      fillOpacity: 0.65,
                      color:'#990000',
                      weight:0.25,
                      opacity:0.9
                  });

                layer.on({
                  'mouseover': highlightOn,
                  'mouseout': highlightOff
              });
              }

              function highlightOn() {
                  this.bringToFront();
                  this.setStyle({
                    fillOpacity: 0.65,
                    color:'#ffffff',
                    weight:2,
                    opacity:0.9
                });
              }

              function highlightOff() {
                  this.bringToBack();
                  this.setStyle({
                    fillOpacity: 0.65,
                    color:'#990000',
                    weight:0.25,
                    opacity:0.9
                  });
              }

              info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info');

                this._div.innerHTML = ('Layer Type: TopoJSON');

                return this._div;
              };

              info.addTo(map);
            </script>
          </body>
        </head>
        """

    return messageBegin + feature + messageEnd
