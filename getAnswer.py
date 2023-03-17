import pygsheets
client = pygsheets.authorize()
sh = client.open('AITU_Answers')
sheet_to_access = sh.worksheet_by_title("Говно")
print(sheet_to_access.get_value("A1"))


