import pygsheets
client=pygsheets.authorize()
sh=client.open('AITU_Answers')
wks=sh.sheet1
print(wks.get_value('A1'))
