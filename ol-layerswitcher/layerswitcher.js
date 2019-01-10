(function() {

	// thanks to https://github.com/martgnz/bcn-geodata

    $.when(
        $.getJSON("./bcn-geodata.json", {})
        .done (function( data ) {
            var overlays = data;
            //console.log(overlays);

            var layerOverlays = getLayerTree(overlays);
            //console.log(layerOverlays);

            var qgisLayers = [
                new ol.layer.Group({
                    'title': 'Capes de referència',
                    layers: [
                        new ol.layer.Tile({
                            title: 'Cap fons',
                            type: 'base'
                        }),
                        new ol.layer.Tile({
                            title: 'Topogràfic 1:5.000 (by ICGC)',
                            type: 'base',
                            visible: false,
                            source: new ol.source.TileWMS({
                                url: 'http://geoserveis.icgc.cat/icc_mapesbase/wms/service?',
                                params: {'LAYERS': 'mtc5m', 'VERSION': '1.1.1'}
                            })
                        }),
                        new ol.layer.Tile({
                            title: 'OpenStreetMap, estilo Positron (by Carto)',
                            type: 'base',
                            visible: true,
                            source: new ol.source.XYZ({
                                url: 'http://{1-4}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
                            })
                        })
                    ]
                }),
                new ol.layer.Group({
                    title: 'Capes temàtiques',
                    layers: layerOverlays
                })
            ];

            var map = new ol.Map({
                target: 'map',
                layers: qgisLayers,
                view: new ol.View({
                    center: [220636,5082816],
                    zoom: 13,
                    minZoom: 12,
                    maxZoom: 20
                })
            });

            var layerSwitcher = new ol.control.LayerSwitcher({
                tipLabel: 'Légende' // Optional label for button
            });
            map.addControl(layerSwitcher);
        })
        .fail(function(data) {    
            console.log("json error in layertree.json");  
        })
    ).then(function() { 
        console.log("json file layertree.json loaded!");
    });

})();

function getLayerTree(overlays) {
    var layerOverlays = [];

    for (var i=overlays.length-1; i>=0; i--) {

        //console.log(overlays[i].name, overlays[i].type, overlays[i].children);

        layerOverlays.push(
            new ol.layer.Tile({
                title: overlays[i].name,
                source: getLayerSource(overlays[i].name),
                visible: overlays[i].visible,
                hidden: overlays[i].hidden,
                type: 'overlay'
            })
        );
    }

    return layerOverlays;
}

function getLayerSource(layerName) {
    return(
        new ol.source.TileWMS({
            //url:        'http://127.0.0.1:8080/service?',   // qgis
			url:		'http://localhost/cgi-bin/bcn-geodata/qgis_mapserv.fcgi?',	//qgis
            params: {
                        'LAYERS': layerName,
                        'TRANSPARENT': true,
            },
            serverType: 'qgis',
        })
    );
}
