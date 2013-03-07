import sys
import math
import datetime


class GPX():

	def __init__(self,location):
		'''Readies variables for use.
		
		Keyword arguments:
		location -- the directory of the file to be opened
		
		'''
		self.gpx_doc = ''
		self.gpx_location = location
		self.route_position = -1
		self.route_points = []
		self.route_distance = 0
		self.route_five = []
		self.track_size = 0
		self.unit_measure = None

	def track_start(self):
		'''Creates a new track file for future use.'''
		self.gpx_file = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')) + '.gpx'
		out = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n<gpx>\n\t<trk>\n\t\t<name>NAVSTAT TRACK</name>\n\t\t<trkseg>\n'
		self.gpx_doc = open(self.gpx_location + self.gpx_file, 'a')
		self.track_out(out)

	def track_point(self,lat,lon,ele,tme):
		'''Readies a track point to be outputted to the track file.
		
		Keyword arguments:
		lat -- the latitude to output
		lon -- the longitude to output
		ele -- the elevation to output
		tme -- the time to output
		
		'''
		out = '\t\t\t<trkpt lat="' + str(lat) + '" lon="' + str(lon) + '">\n' + '\t\t\t\t<ele>' + str(ele) + '</ele>\n' + '\t\t\t\t<time>' + str(tme) + '</time>\n\t\t\t</trkpt>\n'
		self.track_out(out)

	def track_out(self, out):
		'''Outputs track text to the track gpx file.
		
		Keyword arguments:
		out -- the string to be outputted
		
		'''
		self.gpx_doc.write(out)
		self.track_size = self.track_size + sys.getsizeof(out)

	def track_close(self):
		'''Closes the current track gpx file.'''
		out = '\t\t</trkseg>\n\t</trk>\n</gpx>'
		self.track_out(out)
		self.gpx_doc.close()

	def route_start(self,gpx_file):
		'''Reads the entire GPX route file, and creates a list from it.
		
		Keyword arguments:
		gpx_file -- the GPX route file to open
		
		'''
		lat_lon = [0,0,'',0,0]
		#Open the gpx route file
		self.gpx_doc = open(self.gpx_location + gpx_file, 'r')
		#Create a local version of functions
		route_append = self.route_points.append
		haversine = self.haversine
		con = 0
		#Run through each line of the route file
		for line in self.gpx_doc:
			line = line.lstrip()
			#Extract route point lat/long
			if line[1:6] == 'rtept':
				line = line.split('"')
				lat_lon[0] = float(line[1])
				lat_lon[1] = float(line[3])
				con = 1
			#Extract route point name
			elif line[1:5] == 'name':
				line = line.split('name>')
				lat_lon[2] = line[1][:-2]
				#As long as its not the first point
				if self.route_points:
					#Calculate the distance from the last point, to this point
					haversine_info = haversine(self.route_points[-1][0],self.route_points[-1][1],lat_lon[0],lat_lon[1])
					#Place distance in last point info
					self.route_points[-1][3] = haversine_info
					#Add to the total distance
					self.route_distance = haversine_info + self.route_distance
				route_append([lat_lon[0],lat_lon[1],lat_lon[2],0])
				con = 0
		self.gpx_doc.close()

	def route_get(self):
		'''Returns the next point in the route list.'''
		x = 1
		#Empties the next five point list
		self.route_five = []
		#Moves the route position forward
		self.route_position = self.route_position + 1
		#Creates a new list of the next five points
		while x < 6:
			self.route_five.append(self.route_points[self.route_position + x])
			x += 1
		#Recalculates the route distance
		self.route_calc()
		#Returns the route point info
		return self.route_points[self.route_position]

	def route_calc(self):
		'''Calculates the distance between the next route position, and all points after.'''
		#Removes the current route point from calculation
		x = self.route_position + 1
		self.route_distance = 0
		length = len(self.route_points) - 1
		#Adds the distance info
		while x < length:
			self.route_distance = self.route_distance + self.route_points[x][3]
			x += 1

	def haversine(self,lat_1,lon_1,lat_2,lon_2):
		'''Calculates the distance between two coordinates.
		
		Keyword arguments:
		lat_1 -- the base coordinate latitude
		lon_1 -- the base coordinate longitude
		lat_2 -- the alternate coordinate latitude
		lon_2 -- the alternate coordinate longitude
		
		'''
		#Earth radius
		radius = 6378.137
		lon_1, lat_1, lon_2, lat_2 = map(math.radians, [lon_1, lat_1, lon_2, lat_2])
		dst_lon = lon_2 - lon_1
		dst_lat = lat_2 - lat_1
		a = math.sin(dst_lat/2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(dst_lon/2)**2
		c = 2 * math.asin(math.sqrt(a))
		dis_out = radius * c
		return round(dis_out,2)



#gpx_route = GPX('/home/home/NAVSTAT/Routes/')
#gpx_route.route_start('Example.gpx',1)
#hello = gpx_route.route_get()

#print gpx_route.route_points
#print gpx_route.route_distance
#print gpx_route.route_five
#print gpx_route.route_position
#print hello
