import os
import xml.etree.ElementTree as ET
import json



def populate_documents(filepath):

	file = open(filepath,'r')
	tree = ET.parse(file)
	root = tree.getroot()
	for document in root:
		docAttrDict = document.attrib
		doc = add_document(docAttrDict)
		if doc is not None:
			for fragment in document:
				fragAttrDict = fragment.attrib
				add_fragment(doc,fragAttrDict)


def add_document(attributesDict):
	try:
		document_id = attributesDict['ID']
		type = attributesDict['type']
		kind = attributesDict['kind']
		document_type=DocumentType.objects.filter(name=type, kind=kind)[0]
		document_name = attributesDict['name']
		fixOrder = json.loads(attributesDict['FixOrder'])
		d = Document.objects.get_or_create(id = document_id)[0]
		d.name = document_name
		d.document_type = document_type
		d.fixOrder = fixOrder
		d.save()
		return d
	except (IntegrityError, IndexError, KeyError):
		return None

# ASK how to populate style depending on fragment type automatically
def add_fragment(doc, attributesDict):
	try:
		type = attributesDict['type']
		document_type=doc.document_type
		fragment_type=FragmentType.objects.filter(name=type,document_type=document_type)[0]
		fragment_style=FragmentStyle.objects.filter(type=fragment_type)[0]
		id = attributesDict['ID']
		text = attributesDict['value']
		text = text.replace(' ','&nbsp')
		text = text.replace('<','&lt')
		text = text.replace('>','&gt')
		if text.endswith(';'):
			text = text[:text.rfind(";"):] + "<br/>"

		order = json.loads(attributesDict['order'])
		f = Fragment.objects.get_or_create(id = id)[0]
		f.document = doc
		f.text = text
		f.style = fragment_style
		f.type = fragment_type
		f.order = order
		f.save()

	except (IntegrityError, IndexError, KeyError):
		pass

# Start execution here!
if __name__ == '__main__':
	print "Starting DocumentFragment population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercises_system_project.settings')
	from exerciser.models import Document, Fragment, FragmentType, DocumentType, FragmentStyle
	from django.db import IntegrityError
	documents_path = os.path.join(os.path.dirname(__file__), 'cs1ct/Documents.xml')
	populate_documents(documents_path)