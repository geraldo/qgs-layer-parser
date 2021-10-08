from qgis.core import *
from qgis.gui import *
from PyQt5.QtCore import QFileInfo
import json
import unicodedata
import sys

def run():
	project_name = 'ctbb'
	project_path = '/home/ubuntu/'+project_name+'/'
	dest_path = '/var/www/mapa/'+project_name+'/js/data/'
	#project_path = '/home/gerald/Documents/PSIG/ctbb/wfs/'
	#dest_path = project_path

	prj_file = sys.argv[1]
	project_file = prj_file.replace('.qgs', '')

	# mapproxy proyect name
	mapproxy_name = project_file
	if len(sys.argv) > 2:
		mapproxy_name = sys.argv[2]

	# create a reference to the QgsApplication, setting the
	# second argument to False disables the GUI
	qgs = QgsApplication([], False)

	# supply path to qgis install location
	qgs.setPrefixPath("/usr", True)

	# load providers
	qgs.initQgis()

	# Get the project instance
	project = QgsProject.instance()
	gui = QgsGui.instance()

	# Load qgis project
	if not project.read(project_path+prj_file):
	    print('Something went wrong with the project file!')
	    print('You have to call the script adding the absolute path of the project file like: /home/qgis/project.qgs')

	print("Project title:", project.title())
	print("Project file:", project.fileName())

	wfsList = project.readListEntry("WFSLayers", "/")[0]
	#print("Vector layers:", wfsList);

	def replaceSpecialChar(text):
	    chars = "!\"#$%&'()*+,./:;<=>?@[\\]^`{|}~¬·"
	    for c in chars:
	        text = text.replace(c, "")
	    return text

	def stripAccents(s):
	   return ''.join(c for c in unicodedata.normalize('NFD', s)
	                  if unicodedata.category(c) != 'Mn')

	def layertree(node, vectorial=False):
		#print(node.dump())
		#print(node.name(), type(node))
		obj = {}

		if isinstance(node, QgsLayerTreeLayer):
			obj['name'] = node.name()
			obj['qgisname'] = node.name()	# internal qgis layer name with all special characters
			obj['mapproxy'] = project_name+"_"+mapproxy_name+"_layer_"+replaceSpecialChar(stripAccents(obj['name'].lower().replace(' ', '_')))
			obj['type'] = "layer"
			obj['indentifiable'] = node.layerId() not in nonidentify
			obj['visible'] = node.isVisible()
			obj['hidden'] = node.name().startswith("@")	# hide layer from layertree
			if obj['hidden']:
				obj['visible'] = True 	# hidden layers/groups have to be visible by default
			obj['showlegend'] = not node.name().startswith("~") and not node.name().startswith("¬")	# don't show legend in layertree

			vectorial = False
			if node.layerId() in wfsList:
				vectorial = True

			obj['vectorial'] = vectorial
			obj['fields'] = []
			obj['actions'] = []
			obj['external'] = node.name().startswith("¬")

			# remove first character
			if not obj['showlegend']:
				obj['name'] = node.name()[1:]

			# fetch layer directly from external server (not from QGIS nor mapproxy)
			if obj['external']:
				obj['name'] = node.name()[1:]
				src = project.mapLayer(node.layerId()).source()
				
				# wms url
				istart = src.index("url=")+4
				try:
					iend = src.index("&", istart)
				except ValueError:
					iend = len(src)
				obj['wmsUrl'] = src[istart:iend]
				
				# wms layers
				istart = src.index("layers=")+7
				try:
					iend = src.index("&", istart)
				except ValueError:
					iend = len(src)
				obj['wmsLayers'] = src[istart:iend]
				
				# wms srs
				istart = src.index("crs=")+4
				try:
					iend = src.index("&", istart)
				except ValueError:
					iend = len(src)
				obj['wmsProjection'] = src[istart:iend]

			#print("- layer: ", node.name())

			layer = project.mapLayer(node.layerId())

			if vectorial:
				print("write sld to:", dest_path+"sld/"+prj_file+'_'+node.name()+".sld")
				layer.saveSldStyle(dest_path+"sld/"+prj_file+"_"+node.name()+".sld")

			if obj['indentifiable'] and isinstance(layer, QgsVectorLayer):

				fields = []

				# get all fields like arranged using the Drag and drop designer
				edit_form_config = layer.editFormConfig()
				root_container = edit_form_config.invisibleRootContainer()
				for field_editor in root_container.findElements(QgsAttributeEditorElement.AeTypeField):
					i = field_editor.idx()
					if i >= 0 and layer.editorWidgetSetup(i).type() != 'Hidden':
						#print(i, field_editor.name(), layer.fields()[i].name(), layer.attributeDisplayName(i))

						f = {}
						f['name'] = layer.attributeDisplayName(i)
						obj['fields'].append(f)

				for action in gui.mapLayerActionRegistry().mapLayerActions(layer):
					a = {}
					a['name'] = action.name()
					a['action'] = action.action()
					obj['actions'].append(a)

			return obj

		elif isinstance(node, QgsLayerTreeGroup):
			obj['name'] = node.name()
			obj['qgisname'] = node.name()	# internal qgis layer name with all special characters
			obj['mapproxy'] = project_name+"_"+mapproxy_name+"_group_"+replaceSpecialChar(stripAccents(obj['name'].lower().replace(' ', '_')))
			obj['type'] = "group"
			obj['visible'] = node.isVisible()
			obj['hidden'] = node.name().startswith("@")
			if obj['hidden']:
				obj['visible'] = True 	# hidden layers/groups have to be visible by default
			obj['showlegend'] = not node.name().startswith("~")	# don't show legend in layertree
			#print("- group: ", node.name())
			#print(node.children())

			# remove first character
			if not obj['showlegend']:
				obj['name'] = node.name()[1:]

			vectorial = False
			#if node.name() in groups_vectorial:
			#	vectorial = True
			obj['vectorial'] = vectorial
			obj['children'] = []

			for child in node.children():
				obj['children'].append(layertree(child, vectorial))

		return obj

	info=[]
	nonidentify = project.nonIdentifiableLayers()
	root = project.layerTreeRoot()
	for group in root.children():
		obj = layertree(group)
		info.append(obj)

	# identifiable <Identify>
	#print(project.readEntry("qgis", "Identify"))

	# write to json file
	f=open(dest_path+prj_file+'.json', 'w+')
	f.write(json.dumps(info))
	f.close()

	# When your script is complete, call exitQgis() to remove the
	# provider and layer registries from memory
	qgs.exitQgis()

	print("Layer tree written to:", dest_path+prj_file+'.json')

run()
