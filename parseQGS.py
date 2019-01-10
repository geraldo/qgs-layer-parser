from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import QFileInfo
import json
import unicodedata

project_path = '/home/gerald/prog/qgs-layer-parser/'
project_file = 'bcn-geodata'

# create a reference to the QgsApplication
qgs = QgsApplication([], True)

# supply path to qgis install location
qgs.setPrefixPath("/usr", True)

# load providers
qgs.initQgis()

# get the project instance
project = QgsProject.instance()
gui = QgsGui.instance()

# load QGIS project
if not project.read(project_path+project_file+".qgs"):
    print('Something went wrong with the project file!')

print("Project file:", project.fileName())
print("Project title: ", project.title())

def layertree(node):
	#print(node.dump())
	print(node.name(), type(node))
	obj = {}

	if isinstance(node, QgsLayerTreeLayer):
		obj['name'] = node.name()
		obj['type'] = "layer"
		obj['indentifiable'] = node.layerId() not in nonidentify
		obj['visible'] = node.isVisible()
		obj['hidden'] = node.name().startswith("@")
		if obj['hidden']:
			obj['visible'] = True 	# hidden layers/groups have to be visible by default
		obj['fields'] = []
		obj['actions'] = []
		print("- layer: ", node.name())
		
		layer = project.mapLayer(node.layerId())

		aliases = layer.attributeAliases()

		if obj['indentifiable']:
			for index in layer.attributeList():
				if layer.editorWidgetSetup(index).type() != 'Hidden':
					#print(layer.fields()[index].name(), layer.attributeDisplayName(index))
					f = {}
					f['name'] = layer.attributeDisplayName(index)
					obj['fields'].append(f)

			for action in gui.mapLayerActionRegistry().mapLayerActions(layer):
				a = {}
				a['name'] = action.name()
				a['action'] = action.action()
				obj['actions'].append(a)
		
		return obj

	elif isinstance(node, QgsLayerTreeGroup):
		obj['name'] = node.name()
		obj['type'] = "group"
		obj['visible'] = node.isVisible()
		obj['hidden'] = node.name().startswith("@")
		if obj['hidden']:
			obj['visible'] = True 	# hidden layers/groups have to be visible by default
		obj['children'] = []
		print("- group: ", node.name())

		for child in node.children():
			obj['children'].append(layertree(child))

	return obj

info=[]
print("Project tree:")
nonidentify = project.nonIdentifiableLayers()
root = project.layerTreeRoot()

# iterate over layer tree
for group in root.children():
	obj = layertree(group)
	info.append(obj)

# write to json file
f=open(project_file+'.json', 'w+')
f.write(json.dumps(info))
f.close()

qgs.exitQgis()
