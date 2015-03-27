import os
import xml.etree.ElementTree as ET
import json



def populate(filepath):

	file = open(filepath,'r')
	tree = ET.parse(file)
	root = tree.getroot()
	for document in root:
		docAttrDict = document.attrib
		docName = docAttrDict['name']
		doc_id = docAttrDict['ID']
		doc = add_document(doc_id,docAttrDict)
		if doc is not None:
			print "OK"
			for fragment in document:
				fragAttrDict = fragment.attrib
				add_fragment(doc,fragAttrDict)

	# Print out what we have added to the user.
	for d in Document.objects.all():
		for f in Fragment.objects.filter(document = d):
			print "- {0} - {1}".format(str(d), str(f))



def add_document(document_id,attributesDict):
	try:
		type = attributesDict['type']
		kind = attributesDict['kind']
		document_type=DocumentType.objects.filter(name=type, kind=kind)[0]
		document_name = attributesDict['name']
		fixOrder = json.loads(attributesDict['FixOrder'])
		d = Document.objects.get_or_create(id = document_id, name = document_name, document_type = document_type, fixOrder = fixOrder)[0]
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
		f = Fragment.objects.get_or_create(document = doc,id = id, text = text, style = fragment_style, type = fragment_type, order = order)[0]

	except (IntegrityError, IndexError, KeyError):
		print "exception"
		pass

# Start execution here!
if __name__ == '__main__':
	print "Starting DocumentFragment population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercises_system_project.settings')
	from exerciser.models import Document, Fragment, FragmentType, DocumentType, FragmentStyle
	from django.db import IntegrityError
	fn = os.path.join(os.path.dirname(__file__), 'cs1ct/Documents.xml')
	populate(fn)