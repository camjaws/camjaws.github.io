from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
import gspread
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

gc = gspread.authorize(credentials)
# sheet = gc.open("ScoreSheet").sheet1
# sheet = gc.create("a new spreadsheet")
# sheet.share('desmondogillman@gmail.com', perm_type='user',role='writer')


def get_num_players():
    sh = gc.open("Score!").sheet1
    num_players = len(sh.row_values(1))
    return num_players

def add_players(list_of_players):
    sheet = gc.open("Score!").sheet1
    num_players = get_num_players()
    for i,x in enumerate(list_of_players,start=num_players+1):
        sheet.update_cell(1,i,x)
        num_players += 1

def update_score(player,score):
    sheet = gc.open("Score!").sheet1
    cell = sheet.find(player)
    oldval = int(sheet.cell(cell.row+1,cell.col).value)
    sheet.update_cell(cell.row+1,cell.col,oldval+score)

def clear_scores():
    sheet = gc.open("Score!").sheet1
    set_frozen(sheet, rows=1)
    num_players = get_num_players()
    for i in range(1,num_players+1):
        sheet.update_cell(2,i,0)
    
def new_game(email):
    sheet = gc.create("Score!")
    sheet.share(email,perm_type='user',role='writer')
    sh = sheet.sheet1
    clear_scores()

def query_scores():
    sh = gc.open("Score").sheet1
    return  sh.row_values(2)

def query_names():
    sh = gc.open("Score").sheet1
    return sh.row_values(1)        


clear_scores()
update_score("jos",65)
update_score("sammi",45)
update_score("sammi",45)
update_score("cam",42)

print(query_names)
print(query_scores)