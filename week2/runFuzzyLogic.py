import fuzzylogic as fl
from GoogleSheetAPI import SpreadsheetSnippets as ss
from GoogleAPITest import GoogleAPITest


def rearrange2D(input):
    companyInfo = []
    for i in range(len(input)):
        companyInfo.append({"company": input[i][0][0], "sales": input[i][0][1], "profit": input[i][0][2], "profitability": input[i][1]})
    return companyInfo


def inputValue(companyInfo, outputType):
    companyProfit = []
    if outputType == 'singleRow':
        companyProfit = ['']
    for i in range(len(companyInfo)):
        if outputType == 'singleRow':
            companyProfit[0] = companyProfit[0] + str(companyInfo[i]["company"]) + u'\t' + str(companyInfo[i]["profitability"]) + u'\n'
            # companyProfit[1] = companyProfit[1] + str(companyInfo[i]["profitability"]) + u'\n'
        else:
            companyProfit.append([companyInfo[i]["company"], companyInfo[i]["profitability"]])
    if outputType == 'singleRow':
        companyProfit = [[companyProfit[0]]]
    return companyProfit


resultP2 = fl.ffilter(fl.p2, fl.companies)
sortedResult = rearrange2D(resultP2)
value = inputValue(sortedResult, 'singleRow')

googleAPIWrite = GoogleAPITest()
# googleAPIWrite.readWriteGoogleSheet('A2:B7', value)
googleAPIWrite.appendGoogleSheet(value)




