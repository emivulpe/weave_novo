import os
import xml.etree.ElementTree as ET
import json


def populate(filepath):

	file = open(filepath,'r')
	tree = ET.parse(file)
	root = tree.getroot()
	for application in root:
		add_application(application)


	# Print out what we have added to the user.
	for a in Application.objects.all():
		for p in Panel.objects.filter(application = a):
			print "- {0} - {1}".format(str(a), str(p))



def add_application(element):
	try:
		applicationAttributesDict = element.attrib
		name = applicationAttributesDict['name']
		layout = applicationAttributesDict['layout']
		a = Application.objects.get_or_create(name = name, layout = layout)[0]
		for panel in element.iter('panel'):
			panelAttributesDict = panel.attrib
			add_panel(a,panelAttributesDict)
	except (IntegrityError, KeyError):
		pass
	
def add_panel(application, attributesDict):
	try:
		number = json.loads(attributesDict['number'])
		type = attributesDict['type']
		documentName = attributesDict['content']
		document = Document.objects.get(name = documentName)
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
	fn = os.path.join(os.path.dirname(__file__), 'cs1ct/Applications.xml')
	populate(fn)
