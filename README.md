# Map Preview

Preview map layer files in your web browser using [Sublime Text 3](https://www.sublimetext.com/).

## Features

  - Interactive Map preview powered by [LeafletJS](https://leafletjs.com/)

## Supported Formats

  - [GeoJSON](https://geojson.org/)
  - [TopoJSON](https://github.com/topojson/topojson/wiki)

## Installation

Map Preview is currently under review to be available as a package in [Package Manager](https://packagecontrol.io/).  Instructrions will be updated once we are included in the package controll system.  Until then you can manually install using this repository as follows:

### Manual Install
- Clone the **st3-map-preview** repo into the Sublime Text packages location: 

```bash
# move to default Mac location
$ cd ~/Libary/Application Support/Sublime Text 3/Packages
# clone directly into the pakcages directory with folder name mappreview
$ git clone git@github.com:doneill/st3-map-preview.git mappreview

```

## Preview Map in Browser

With an open valid GeoJSON or TopoJSON file in Sublime Text 3:

- Right click and select **Map Preview > Preview in Browser**
- Select **Map Preview: Preview in Browser** from the command palette.

## Troubleshooting

- If your files are being alerted as not valid, plase try at another source, e.g. [geojson.io](https://geojson.io) to confirm. If you feel like your json file is valid and should be shown please ceate an issue and we will take a look.

## Licensing
A copy of the license is available in the repository's [LICENSE](LICENSE) file.