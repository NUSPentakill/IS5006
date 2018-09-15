import re

companyAll = []
companyProfitableAll = []
companyProfitableHighsalesAll = []
companyFinalList = []
companyFinalDict = {'finalTableHTML': ''}
fuzzyProfit = [10., 100.]
fuzzySales = [70., 300.]
rawInput = input.get('emailBodyPlain')

findInput= rawInput.replace('\r', '').replace('\t', '').replace(' ', '')
regex = r"(company.*?:.*?)(\w+)(.*?\n*.*?profit.*?:.*?)(\w+)(.*?\n*.*?sales.*?:.*?)(\w+)"
result = re.findall(regex, findInput, re.IGNORECASE)
for item in result:
    companyBaseInfo = [item[1], item[3], item[5]]
    companyAll.append(companyBaseInfo)

    company = item[1]
    profit = float(item[3])
    sales = float(item[5])

    if profit < fuzzyProfit[0]:
        profitable = 0.
    elif profit < fuzzyProfit[1]:
        profitable = (profit - fuzzyProfit[0]) / (fuzzyProfit[1] - fuzzyProfit[0])
    else:
        profitable = 1.

    if profitable != 0.:
        companyProfitable = companyBaseInfo[:]
        companyProfitable.append(str(profitable))
        companyProfitableAll.append(companyProfitable)

        if sales < fuzzySales[0]:
            salesFuzzy = 0.
        elif sales < fuzzySales[1]:
            salesFuzzy = (sales - fuzzySales[0]) / (fuzzySales[1] - fuzzySales[0])
        else:
            salesFuzzy = 1.

        if salesFuzzy != 0.:
            companyProfitableHighsales = companyProfitable[:]
            companyProfitableHighsales.append(str(salesFuzzy))
            companyProfitableHighsalesAll.append(companyProfitableHighsales)
            hs=companyProfitableHighsales
            companyFinalDict['finalTableHTML'] = companyFinalDict['finalTableHTML'] \
                                                 + '<tr><td>' + hs[0] \
                                                 + '</td><td>' + hs[3] \
                                                 + '</td><td>' + hs[4] +'</td></tr>'
output = companyFinalDict