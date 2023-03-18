import pygsheets

def isThereFree(sheetPlace)->bool:
    client=pygsheets.authorize()
    sh=client.open('AITU_Answers')
    sheet_to_access = sh.worksheet_by_title("Заключенные")
    if not sheet_to_access.get_value(sheetPlace):
        return sheetPlace
def inputWarningByTelegramId(telegramId,message):
    client=pygsheets.authorize()
    sh=client.open('AITU_Answers')
    sheet_to_access = sh.worksheet_by_title("Заключенные")
    for i in range(1,200):
        currentCell='A'+str(i)
        if isThereFree(currentCell):
            sheet_to_access.update_value(currentCell,telegramId)#колонка с тегом
            sheet_to_access.update_value('B'+str(i),message)#колонка с сообщением
            sheet_to_access.update_value('C'+str(i),1)#колонка с предами
            break
        elif telegramId in sheet_to_access.get_value(currentCell):
            sheet_to_access.update_value('B'+str(i),message+'\n'+sheet_to_access.get_value("B"+str(i)))
            newWarnCount=int(sheet_to_access.get_value('C'+str(i)))+1
            sheet_to_access.update_value('C'+str(i),newWarnCount)
            break
inputWarningByTelegramId("@Ratatoskrrr","Да")
