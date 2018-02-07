# -*- coding: utf-8 -*-
import Image, ImageDraw, ImageFont,ImageOps
import time
import datetime
import sys
# font = ImageFont.truetype( "/usr/share/fonts/truetype/freefont/FreeMono.ttf", 24 )
datelist=[] #Gobal var -date data for deal dict hash
timelist=[] #Gobal var -time data for deal dict hash
def FileToDict(FileLocation):
	tempdata={}
	csvfile=open(FileLocation,'r')
	for line in csvfile:
		timestamp,watt=line.split(',')
		dateValue,timeValue=timestamp.split(' ')
		# dateValue=time.mktime(datetime.datetime.strptime(dateValue, "%Y/%m/%d").timetuple())
		# timeValue=time.mktime(datetime.datetime.strptime(timeValue, "%H:%M:%S").timetuple())
		if dateValue not in tempdata:
			tempdata[dateValue]={}
		if dateValue not in datelist:
			datelist.append(dateValue)
		if timeValue not in timelist:
			timelist.append(timeValue)
		tempdata[dateValue][timeValue]=float(watt)
	datelist.sort()
	timelist.sort()
	return tempdata

def Normalization(dictData):
	Max=float('-inf')
	Min=float('inf')
	for dateValue in dictData:
		for timeValue in dictData[dateValue]:
			if dictData[dateValue][timeValue]>Max:
				Max=dictData[dateValue][timeValue]
			if dictData[dateValue][timeValue]<Min:
				Min=dictData[dateValue][timeValue]
	dist=Max-Min
	for dateValue in dictData:
		for timeValue in dictData[dateValue]:
			dictData[dateValue][timeValue]=(dictData[dateValue][timeValue]-Min)/dist*512
	return dictData

def DictToImage(dictData,PointSizeX,PointSizeY,TimeStampX,TimeStampY):
	tmpImg=Image.new( "RGB", (len(datelist)*PointSizeX+TimeStampX,len(timelist)*PointSizeY+TimeStampY) , "White")
	pix = tmpImg.load()
	x=0 #date count
	y=0 #time count

	toolbar_width = 40
	dis=len(datelist)/toolbar_width
	sys.stdout.write("[%s]" % (" " * toolbar_width))
	sys.stdout.flush()
	sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

	for dateValue in datelist:
		for timeValue in timelist:
			try:
				value=int(Povondata[dateValue][timeValue])
			except KeyError:
				value=0
			if value>=256:
				G=value-256;
				for i in range(0,PointSizeX):
					for j in range(0,PointSizeY):
						pix[PointSizeX*x+i+TimeStampX,PointSizeY*y+j]=(0,G,255)
			elif value<256 and value>0:
				for i in range(0,PointSizeX):
					for j in range(0,PointSizeY):
						pix[PointSizeX*x+i+TimeStampX,PointSizeY*y+j]=(0,255,value)
			else:
				for i in range(0,PointSizeX):
					for j in range(0,PointSizeY):
						pix[PointSizeX*x+i+TimeStampX,PointSizeY*y+j]=(255,255,255)
			y+=1
		x+=1
		y=0
		if x%dis==0 and x/dis <=toolbar_width:
			sys.stdout.write(">")
			sys.stdout.flush()

	sys.stdout.write("\n")

	return tmpImg

def ImagePlusTimestamp(img,PointSizeX,PointSizeY,shiftDate,shiftTime,TimeStampX,TimeStampY):
	# draw = ImageDraw.Draw(img)
	count=0
	Shiftcount=0
	first=True
	for timeValue in timelist:
		if Shiftcount==shiftTime or first:
			first=False
			# draw.text((0, count*PointSizeY),time,(0,0,0))
			# =================================================================
			f = ImageFont.load_default()
			txt=Image.new('L', (TimeStampX,PointSizeY))
			d = ImageDraw.Draw(txt)
			d.text( (0, 0),timeValue,  font=f, fill=255)
			# w=txt.rotate(0,  expand=1)
			img.paste( ImageOps.colorize(txt, (0,0,0), (0,0,0)), (0, count*PointSizeY),  txt)
			# =================================================================
			Shiftcount=0
		Shiftcount+=1
		count+=1

	Y=len(timelist)*PointSizeY
	count=0
	Datecount=0
	Datefirst=True
	for dateValue in datelist:
		if Datecount==shiftDate or Datefirst:
			Datefirst=False
			# draw.text((count*PointSizeX, Y),date,(0,0,0))
			# =================================================================
			f = ImageFont.load_default()
			txt=Image.new('L', (TimeStampY,PointSizeX))
			d = ImageDraw.Draw(txt)
			d.text( (0, 0),dateValue,  font=f, fill=255)
			w=txt.rotate(270,  expand=1)
			img.paste( ImageOps.colorize(w, (0,0,0), (0,0,0)), (TimeStampX+count*PointSizeX, Y),  w)
			# =================================================================
			Datecount=0
		Datecount+=1
		count+=1

	return img

def inputQuerry():
	floor = raw_input("Floor (7-9): ")
	timeinterval = raw_input("Time interval (60s,600s,3600s): ")
	return str(floor),str(timeinterval)

def EndCheck():
	while(True):
		check = str(raw_input("Continue ? [Y/n]"))
		if check =='n' or check=='N':
			return True
		elif check=='Y' or check=='y':
			return False

print("---------------------Process start-----------------------")
while (True):
	Flo,timeInter=inputQuerry()
	filename=Flo+"-"+timeInter+".csv"
	Povondata=FileToDict(filename)
	Povondata=Normalization(Povondata)
	im = DictToImage(Povondata,PointSizeX=20,PointSizeY=20,TimeStampX=50,TimeStampY=100)
	im = ImagePlusTimestamp(im,PointSizeX=20,PointSizeY=20,TimeStampX=50,TimeStampY=100,shiftDate=2,shiftTime=5)
	imagename=Flo+"-"+timeInter+".jpg"
	im.save(imagename)
	print (imagename +"	saved")
	if EndCheck():
		print("---------------------Process End-----------------------")
		break
