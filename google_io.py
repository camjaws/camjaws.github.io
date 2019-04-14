from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import gspread
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

gc = gspread.authorize(credentials)
round_num=1
# sheet = gc.open("ScoreSheet").sheet1
# sheet = gc.create("a new spreadsheet")
# sheet.share('desmondogillman@gmail.com', perm_type='user',role='writer')


def get_num_players():
    sh = gc.open("Score!").sheet1
    num_players = len(sh.row_values(1))
    return num_players

def clear_scores():
    sheet = gc.open("Score!").sheet1
    set_frozen(sheet, rows=1)
    set_frozen(sheet, rows=2)
    num_players = get_num_players()
    for i in range(1,num_players+1):
        sheet.update_cell(2,i,0)

def new_round():
    sheet = gc.open("Score!").sheet1
    num_players = get_num_players()
    for i in range(1,num_players+1):
        cell = sheet.cell(2,i)
        val = cell.value
        sheet.update_cell(2+round_num,i,val)
        sheet.update_cell(2,i,0)


def add_players(list_of_players):
    sheet = gc.open("Score!").sheet1
    num_players = get_num_players()
    for i,x in enumerate(list_of_players,start=num_players+1):
        sheet.update_cell(1,i,x)
        num_players += 1
    clear_scores()

def update_score(player,score):
    sheet = gc.open("Score!").sheet1
    cell = sheet.find(player)
    oldval = int(sheet.cell(cell.row+1,cell.col).value)
    sheet.update_cell(cell.row+1,cell.col,oldval+score)
    
def new_game(email):
    try:
        gc.del_spreadsheet("Score!")
    except:
        print("oops")
    sheet = gc.create("Score!")
    sheet.share(email,perm_type='user',role='writer')

def query_scores():
    sh = gc.open("Score").sheet1
    return  sh.row_values(2)

def query_names():
    sh = gc.open("Score").sheet1
    return sh.row_values(1)
