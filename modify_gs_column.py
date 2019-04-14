import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(service_file='creds.json')
sh = gc.open('ScoreSheet')
wks = sh.sheet1
header = wks.cell('A1')
header.value = 'Names'
header.text_format['bold'] = True # make the header bold
header.update()

# or achive the same in oneliner
wks.cell('B1').set_text_format('bold', True).value = 'heights'

# set the names
wks.update_values('A2:A5',[['name1'],['name2'],['name3'],['name4']])

# set the heights
heights = wks.range('B2:B5', returnas='range')  # get the range as DataRange object
heights.name = "heights"  # name the range
heights.update_values([[50],[60],[67],[66]]) # update the vales
wks.update_value('B6','=average(heights)') # set the avg value of heights using named range