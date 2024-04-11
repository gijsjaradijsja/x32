from pydub import AudioSegment
import os, sys, time

#folders
import_folder = '/Users/jochemsmaal/Desktop/X-live_Convert/Input/'
export_folder = '/Users/jochemsmaal/Desktop/X-live_Convert/Output/'
temp_folder = '/Users/jochemsmaal/Desktop/X-live_Convert/Temp/'

#tracknames
names = """
01.Kick
02.Snare
03._
04._
05.Tom_
06.Floor_
07.OHL
08.OHR
09.Bass+Moog
10.Git
11.Sax
12._
13.V roelof
14.V drums_
15.V lars
16.V jochem
17.SPDL
18.SPDR
19.Click
20._
21.AccL
22.AccR
23._
24._
25.TeunL_
26.TeunR_
27.LukasL_
28.LukasR_
29.TommyL_
30.TommyR_
31.L
32.R
"""

#bewerk names
names = names[1:-1]
names = list(names.split("\n"))

#check lengte
if len(names) != 32:
	print('Make sure list is 32 channels! \n')
	sys.exit()

#maak folders aan
for f in [import_folder, export_folder, temp_folder]:
	try:
		os.makedirs(f)
	except:
		pass

#folderlijst maken
def makefileslist(import_folder):
	files = []
	for root, dirs, f in os.walk(import_folder):
		for file in f:
			if file[-4:].lower()=='.wav':
				files = files + [str(os.path.join(root,file))]
	files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
	return files

#maak input files lijst
input_files_list = makefileslist(import_folder)

#geen input is exit
if len(input_files_list)==0:
	print('Input map is empty, g-bye')
	sys.exit()

#laat input files zien
print('Files to be converted:')
[print(i) for i in input_files_list]

#pak een multitrack, selecteer kanaal, naam_nummer, naamlijst en bestemming
def exporttrack(input_file, channel, number, names_list, export_folder):
	print('.')
	sound = AudioSegment.from_file(input_file, format='wav')
	print('..')
	sound = sound.set_sample_width(2)
	print('...')
	sound = sound.split_to_mono()
	export_name = export_folder + names_list[channel] + str(number+1) + '.wav'
	print(f'exporting {names_list[channel]}{str(number+1)} ({str(number+1)} of {len(input_files_list)} tracks)')
	sound[channel].export(export_name, format='wav')

#van alle tracks in filelijst, pak een kanaal en exporteer naar export_folder
def exporttracks(filelist, ch, export_folder):
	for j in range(len(filelist)):
		exporttrack(filelist[j], ch, j, names, export_folder)

#van alle wav's in fileslist, exporteer naar folder, met name
def glue_files(fileslist, export_folder, name):
	sound = AudioSegment.from_file(fileslist[0], format='wav')
	#print(f'adding {fileslist[0]}')
	for k in range(len(fileslist)-1):
		#print(f'adding {fileslist[k+1]}')
		sound = sound + AudioSegment.from_file(fileslist[k+1], format='wav')
	print(f'\nexporting to total file: {name + '.wav'}\n')
	sound.export(export_folder + name + '.wav', format='wav')

def emptychannel(n):
	if names[n].endswith('_'):
		return True
	return False

howmanytracks = len([x for x in names if not x.endswith('_')])

def sec_to_hours(sec_remaining):
	m, s = divmod(sec_remaining, 60)
	h, m = divmod(m, 60)
	h, m, s = int(h), int(m), int(s)
	return (f'{h:02d}:{m:02d}:{s:02d}')
	print(f'====== estemated remaining time:  ======== \n')

#start de stopwatch
c = 1
starttime = time.time()

for i in range(len(names)):
	if emptychannel(i):
		print(f'{i+1} is empty')
	else:
		print(f'\nprocessing {names[i][3:]} ({c} of {howmanytracks})')
		roundtime = time.time()
		#exporteer per kanaal naar temp_folder
		exporttracks(input_files_list, i, temp_folder)

		#voeg samen naar export_folder
		temp_files_list = makefileslist(temp_folder)
		glue_files(temp_files_list, export_folder, names[i])

		#verwijder temp bestanden
		[os.remove(x) for x in temp_files_list]
		c += 1
		
		#print progress
		tracks_left = (howmanytracks + 1 - c)
		if tracks_left == 1:
			print(f'{tracks_left} track left')
		print(f'{tracks_left} tracks left')
		sec_remaining = int(time.time() - roundtime) * tracks_left
		print(f'====== estemated remaining time: {sec_to_hours(sec_remaining)} ========')

#print einde
print(f'Finished in {sec_to_hours(int(time.time() - starttime))}')

