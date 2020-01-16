# qgs-layer-parser

Parse QGIS 3 project files and write a JSON config file with layer information.

## Getting started

Start the script using `python3 parseQGS.py project.qgs`

It creates a JSON configuration file called `project.qgs.json`.

A typical output for a layer could look like this:

```json
  {
    "hidden": false,
    "indentifiable": true,
    "actions": [],
    "name": "barris",
    "type": "layer",
    "showLegend": true,
    "external": false,
    "visible": true,
    "fields": [
      {
        "name": "N_Distri"
      },
      {
        "name": "N_Barri"
      },
      {
        "name": "Coord_X"
      },
      {
        "name": "Coord_Y"
      }
    ]
  },
```

## Configuration

- `project_path` defines the path to the local project directory where .qgs file is located.
- `dest_path` defines the path to the output directory.

## Special characters

- `@` to hide layers: You can use character `@` in front of layer/group names in QGIS to set `"hidden": true`. This tells layerswitcher to avoid showing layer/group but renders layer/groups by default.
- `~` to hide legend: You can use character `~` in front of layer/group names in QGIS to set `"showLegend": false`. This can be used to avoid rendering the legend.
- `¬` to load WMS layers directly: You can use character `¬` in front of layer/group names in QGIS to set `"external": true`. This option also looks up layer source and writes the following parameters:
  - `"wmsUrl": ''`
  - `"wmsLayers": ''`
  - `"wmsProjection": ''`

## More info

The project includes a test QGIS 3 project called [bcn-geodata.qgs](https://github.com/geraldo/qgs-layer-parser/blob/master/bcn-geodata.qgs) and it's geojson sources. It uses [Open Data from Barceclona](https://github.com/martgnz/bcn-geodata) with information about districts and neighbourhoods.

It also includes an exmaple using [ol-layerswitcher](https://github.com/walkermatt/ol-layerswitcher) using the produced [bcn-geodata.json](https://github.com/geraldo/qgs-layer-parser/blob/master/bcn-geodata.json) file to configure layers. You can see the result opening [layerswitcher.html](https://go.yuri.at/infovis/ol-layerswitcher/layerswitcher.html).

