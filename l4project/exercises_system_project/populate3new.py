import os
import xml.etree.ElementTree as ET
import json
import sys


# A method that takes an xml ducument containing information about the doc types and stores it in the database
def populate_doc_types(filepath):

	file = open(filepath,'r')
	tree = ET.parse(file)
	root = tree.getroot()
	for document_type in root: #Get the documentType element
		document_type_attr_dict=document_type.attrib # Get the attributes for the document type
		document_id = document_type_attr_dict['ID'] # Get the id
		document_type_name = document_type_attr_dict['name'] # Get the name
		# Add the document type to the database
		doc_type = add_document_type(document_type_attr_dict)
		if doc_type is not None:
			# Add the fragment types for the document type
			for fragment_type in document_type:
				fragment_type_attr_dict=fragment_type.attrib 
				fragment_type_name = fragment_type_attr_dict['name']
				frag_type = add_fragment_type(doc_type,fragment_type_attr_dict)
				if frag_type is not None:
					# Add the text style for the fragment type
					for text_style in fragment_type:
						text_style_attr_dict = text_style.attrib
						add_fragment_style(doc_type,frag_type,text_style_attr_dict)


# A method to add the fragment style to the database
def add_fragment_style(document_type,fragment_type, text_style_attr_dict):
	font = text_style_attr_dict['font']
	font_size = text_style_attr_dict['size']
	str_to_bool(text_style_attr_dict['bold'])
	bold = str_to_bool(text_style_attr_dict['bold'])
	italic = str_to_bool(text_style_attr_dict['italic'])
	underlined = str_to_bool(text_style_attr_dict['underline'])
	fragmet_style = FragmentStyle.objects.get_or_create(font = font,bold = bold, italic = italic, underlined = underlined, font_size = font_size,type=fragment_type)[0]
	return fragmet_style
	
def add_document_type(document_type_attr_dict):
	name = document_type_attr_dict['name']
	kind = document_type_attr_dict['kind']
	document_type = DocumentType.objects.get_or_create(name=name)[0]
	document_type.kind = kind
	document_type.save()
	return document_type

	
def add_fragment_type(document_type,fragment_type_attr_dict):
	name = fragment_type_attr_dict['name']
	kind = fragment_type_attr_dict['kind']
	fragment_type = FragmentType.objects.get_or_create(document_type=document_type,name=name,kind=kind)[0]
	return fragment_type
	

def str_to_bool(s):
	if s == 'true':
		 return True
	elif s == 'false':
		 return False
	else:
		 raise ValueError
# Start execution here!
if __name__ == '__main__':
	print "Starting DocumentFragment population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exercises_system_project.settings')
	from exerciser.models import FragmentStyle, Document, DocumentType, FragmentType
	from django.db import IntegrityError
	#if len(sys.argv) <= 1:
	#	print "Please specify the path for the file Doc Types.xml"
	#else:
	#print 'Argument List:', str(sys.argv)
	doc_types_path = os.path.join(os.path.dirname(__file__), 'cs1ct/Doc Types.xml')
	populate_doc_types(doc_types_path)