import pygsheets
gc = pygsheets.authorize(service_file='creds.json')
wks = gc.create("Score_from_PYTHON", folder="My Drive/scoresheets/").sheet1

# create a new sheet with 50 rows and 60 colums
values_mat = wks.get_values(start=(1,1), end=(20,20), returnas='matrix')

# Get all values of sheet as 2d list of cells
cell_matrix = wks.get_all_values(returnas='matrix')

# update a range of values with a cell list or matrix
wks.update_values(crange='A1:E10', values=values_mat)

# Insert 2 rows after 20th row and fill with values
wks.insert_rows(row=20, number=2, values=values_list)

# resize by changing rows and colums
wks.rows=30

# use the worksheet as a csv
for row in wks:
    print(row)

# get values by indexes
A1_value = wks[0][0]

# clear all values
wks.clear()

# Search for a table in the worksheet and append a row to it
wks.append_table(values=[1,2,3,4])

# export a worksheet as csv
wks.export(pygsheets.ExportType.CSV)

# Find/Replace cells with string value
cell_list = worksheet.find("query string")

# Find/Replace cells with regexp
filter_re = re.compile(r'(small|big) house')
cell_list = worksheet.find(filter_re, searchByRegex=True)
cell_list = worksheet.replace(filter_re, 'some house', searchByRegex=True)

# Move a worksheet in the same spreadsheet (update index)
wks.index = 2 # index start at 1 , not 0

# Update title
wks.title = "NewTitle"

# Update hidden state
wks.hidden = False

# working with named ranges
wks.create_named_range('A1', 'A10', 'prices')
wks.get_named_range('prices')
wks.get_named_ranges()  # will return a list of DataRange objects
wks.delete_named_range('prices')

# Plot a chart/graph
wks.add_chart(('A1', 'A6'), [('B1', 'B6')], 'Health Trend')