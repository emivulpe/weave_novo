import os
import xml.etree.ElementTree as ET
import json


def populate_applications(filepath):

	file = open(filepath,'r')
	tree = ET.parse(file)
	root = tree.getroot()
	for application in root:
		add_application(application)


def add_application(app):
	try:
		applicationAttributesDict = app.attrib
		name = applicationAttributesDict['name']
		layout = applicationAttributesDict['layout']
		application = Application.objects.get_or_create(name = name)[0]
		application.layout = layout
		application.save()
		for panel in app.iter('panel'):
			panelAttributesDict = panel.attrib
			add_panel(application,panelAttributesDict)
	except (IntegrityError, KeyError):
		pass
	
def add_panel(application, attributesDict):
	try:
		number = json.loads(attributesDict['number'])
		type = attributesDict['type']
		documentName = attributesDict['content']
		document = Document.objects.filter(name = documentName)
		if len(document) > 0:
			document = document[0]
			p = Panel.objects.get_or_create(application = application, number = number, type = type, document = document)[0]
	except (IntegrityError, ObjectDoesNotExist, KeyError):
		pass

# Start execution here!
if __name__ == '__main__':
	print "Starting DocumentFragment population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercises_system_project.settings')
	from exerciser.models import Document, Application, Panel
	from django.db import IntegrityError
	from django.core.exceptions import ObjectDoesNotExist
	applications_path = os.path.join(os.path.dirname(__file__), 'cs1ct/Applications.xml')
	populate_applications(applications_path)
