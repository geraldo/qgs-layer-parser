# qgs-layer-parser
Parse QGIS 3 project file and create JSON config file

Start the script using `/usr/bin/python3.5 -b parseQGS.py [file.qgs]`

Creates a JSON configuration file called `[file.json]` in the same directory.

The project includes a test QGIS 3 project called [bcn-geodata.qgs](https://github.com/geraldo/qgs-layer-parser/blob/master/bcn-geodata.qgs) and it's geojson sources. It uses [Open Data from Barceclona](https://github.com/martgnz/bcn-geodata) with information about districts and neighbourhoods.

A typical output for a layer could look like that:

```json
  {
    "hidden": false,
    "indentifiable": true,
    "actions": [],
    "name": "barris",
    "type": "layer",
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

It also includes an exmaple using [ol-layerswitcher](https://github.com/walkermatt/ol-layerswitcher) using the produced [bcn-geodata.json](https://github.com/geraldo/qgs-layer-parser/blob/master/bcn-geodata.json) file to configure layers. You can see the result opening [layerswitcher.html](https://go.yuri.at/infovis/ol-layerswitcher/layerswitcher.html).

You can use character `@` in front of layer/group names in QGIS to set `"hidden": true`. This tells layerswitcher to avoid showing layer/group but renders layer/groups by default.
