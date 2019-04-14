# Import the libraries.
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from mako.template import Template
from mako.lookup import TemplateLookup
from urllib import parse
from pyswip import Prolog
import cgi
import csv
import time

# HTTPServer parameters.
host = ''
port = 8000

# Initialize Prolog.
prolog = Prolog()
prolog.consult('model/data.pl')

# Get the fields.
def getFields():
	fields = []

	with open('uploads/fields.csv', 'r') as file:
		data = csv.reader(file)
					
		for row in data:
			fields.append({'id': row[0], 'description': row[1], 'isCategory': row[2]})

		return fields

# Get all the datasets.
def getAllDatasets():
	datasets = []

	with open('uploads/filelist.csv', 'r') as file:
		csvData = csv.reader(file)
					
		for row in csvData:
			datasets.append({'id': row[0], 'name': row[1]})

		return datasets

# Get the name of a dataset.
def getDatasetName(id):
	with open('uploads/filelist.csv', 'r') as file:
		csvData = csv.reader(file)
					
		for row in csvData:
			if row[0] == id:
				return row[1]

		return ''

# Request handler.
class OdpRequestHandler(SimpleHTTPRequestHandler):
	# Handle GET request.
	def do_GET(self):
		# List of pages.
		pages = ['home', 'add', 'datasets', 'detector']

		# Homepage on root.
		if self.path == '/':
			self.path = '/home'

		# Selected page.
		page = self.path.split('/')[1]

		# Check if the current request is a page.
		if page in pages:
			# Get the response page template.
			lookup = TemplateLookup(directories=['templates/'])
			template = lookup.get_template(page + '.mako')

			# Set the response page headers.
			self.send_response(200)
			self.send_header('Content-Type', 'text/html; charset=utf-8')
			self.end_headers()

			# Page specific fields.
			fields = {}

			if page == 'datasets':
				# Datasets page, get the list of datasets.
				fields['datasets'] = getAllDatasets()
			elif page == 'detector':
				# Detector page, get the dataset id.
				datasetId = self.path.split('/')[2]

				# Get the dataset name.
				name = getDatasetName(datasetId)

				# Add the name to the fields.
				fields['name'] = name

				# Open the dataset.
				with open('uploads/' + datasetId + '.csv', 'r') as file:
					# Read the CSV column names.
					columnIdsLine = file.readline().rstrip()
					columnIds = columnIdsLine.split(',')

					# Make a dictonary for the column names.
					columnNames = {}

					# Get the column names.
					allFields = getFields()
					category = ''

					# Get the descriptions for the columns.
					for field in allFields:
						if field['isCategory'] == '1':
							category = field['description']
						elif field['id'] in columnIds:
							label = ''

							if category != '':
								label += category + ' - '

							label += field['description']

							columnNames[field['id']] = label
					
					# Add the column names to the fields.
					fields['columns'] = columnNames

			# Render the response page template.
			self.wfile.write(bytes(template.render(fields=fields), 'utf-8'))

			# Get response is ready.
			return

		# Else, give back the file from the public folder.
		self.path = 'public' + self.path
		return SimpleHTTPRequestHandler.do_GET(self)

	def do_POST(self):
		# Get the selected page.
		page = self.path.split('/')[1]

		if page == 'upload':
			# The user uploads a dataset.

			# Get the request info.
			ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
			clength = self.headers.get('Content-Length')

			pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
			pdict['CONTENT-LENGTH'] = clength

			# Get the uploaded file.
			uploads = cgi.parse_multipart(self.rfile, pdict)
			uploadedFile = uploads.get('file')[0]

			# Create a filename using the current timestamp.
			filename = str(time.time())

			# Save the uploaded data set.
			with open('uploads/' + filename + '.csv', 'wb') as file:
				file.write(uploadedFile)
				file.close()

			# Open the dataset.
			with open('uploads/' + filename + '.csv', 'r') as file:
				# Read the CSV column names.
				columnNamesLine = file.readline().rstrip()
				columnNames = columnNamesLine.split(',')

				# Get the standard column names.
				standardColumnNames = getFields()

				# Get the auto sugested column names.
				sugestedColumnNames = ['PersonIdentifier', 'PersonFullName', 'PersonBirthName', 'PersonCountryOfBirthLocationGeometry']

				# Get the response page template.
				lookup = TemplateLookup(directories=['templates/'])
				template = lookup.get_template('upload.mako')

				# Set the response page headers.
				self.send_response(200)
				self.send_header('Content-Type', 'text/html; charset=utf-8')
				self.end_headers()

				# Render the response page template.
				self.wfile.write(bytes(template.render(filename=filename, columns=columnNames, sugestedColumns=sugestedColumnNames, standardColumns=standardColumnNames), 'utf-8'))
			
			# Upload response is ready.
			return
		elif page == 'submit':
			# The user submits a dataset.

			# Get the request info.
			clength = self.headers.get('Content-Length')
			cdata = self.rfile.read(int(clength))

			# Get the submitted data.
			data = parse.parse_qs(cdata)
			filename = data[b'filename'][0].decode('utf-8')
			displayname = data[b'displayname'][0].decode('utf-8')
			columnNames = data[b'column']

			# Read the current state of the file.
			file = open('uploads/' + filename + '.csv', 'r')
			dataset = file.readlines()
			file.close()

			# Save the new column names to the file.
			with open('uploads/' + filename + '.csv', 'w') as file:
				# Note if it's the first line.
				firstLine = True

				# Loop through the dataset line.
				for line in dataset:
					# Check if it's the first line.
					if firstLine:
						# Write the column names.
						columnNamesLine = b','.join(columnNames)
						file.write(columnNamesLine.decode('utf-8'))

						# Add a new line.
						file.write('\n')

						# Not the first line anymore.
						firstLine = False
					else:
						# Write the line.
						file.write(line)

				# Close the file.
				file.close()

			# Save the dataset name in the filelist.
			with open('uploads/filelist.csv', 'a') as filelist:
				filelist.write(filename + ',' + displayname + '\n')

			# Go to the datasets page.
			self.send_response(302)
			self.send_header('Location', '/datasets')
			self.end_headers()

			# Submit response is ready.
			return
		elif page == 'detector':
			# Check for a data breach.

			# Get the request info.
			clength = self.headers.get('Content-Length')
			cdata = self.rfile.read(int(clength))

			# Get the submitted data.
			data = parse.parse_qs(cdata)
			columns = data[b'columns']

			# Format the fields for Prolog.
			prologQuery = 'breach(['

			# Create the Prolog query.
			allFields = getFields()
			currentCategory = ''
			fields = []

			for field in allFields:
				if field['isCategory'] == '1':
					prologQuery += ','.join(fields)
					prologQuery += "],["
					fields = []
					currentCategory = field['id']
				elif field['id'].encode('utf-8') in columns:
					fieldName = field['id'].replace(currentCategory, '', 1)
					fields.append(fieldName[0].lower() + fieldName[1:])

			prologQuery += ','.join(fields)

			prologQuery += '])'

			print(prologQuery)
			
			# Excecute the Prolog query.
			prologResult = prolog.query(prologQuery)

			# Parse the Boolean result.
			if list(prologResult):
				breach = True
			else:
				breach = False

			# Get the dataset id.
			datasetId = self.path.split('/')[2]

			# Get the response page template.
			lookup = TemplateLookup(directories=['templates/'])
			template = lookup.get_template('result.mako')

			# Set the response page headers.
			self.send_response(200)
			self.send_header('Content-Type', 'text/html; charset=utf-8')
			self.end_headers()

			# Render the response page template.
			self.wfile.write(bytes(template.render(breach=breach), 'utf-8'))

			# Detector response is ready.
			return

		# Else, give back the GET response.
		return self.do_GET()

# Create the handler.
handler = OdpRequestHandler

# Create the HTTP server.
with HTTPServer((host, port), handler) as httpd:
	# Start the HTTP server.
	httpd.serve_forever()