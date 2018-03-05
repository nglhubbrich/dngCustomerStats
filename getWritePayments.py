'''
Created: March 1, 2018
@author: nglhubbrich    
modified on: March 2, 2018
modifications:
    --cleaned up comments
    --fixed getAccountInfo function
modified on: March 5, 2018
modifications:
    -- handled errors noted in TODO file

summary:
    This little buddy can be used to grab all of the account information in a given time from the payment report from L-Boss Reports. On prompt it will require a .TXT format of the report you want to get info from. Once entered it will give you an accurate customer count as well as write out each customers payment to a csv file. Best use of this script will be to run it monthly to keep a running csv formatted list of all DNG payments. 

    NOTE: writing to the csv file will APPEND to the csv file. If you run this program more than once on the same file it will write the information again, causing multiple rows of the same information!
'''
#IMPOTED MODULES
import csv
import re
import os
import shutil

#try to get the report file name from the user
while True:
    fileFromInput = input('What is the name of the file?(include the file extension!) ')
    try:
        with open(fileFromInput) as doc:
            data = doc.readlines()
        break
    except FileNotFoundError:
        print('That doesn\'t seem to be right. Check the file path and make sure it is correct')
        continue
        
def getCustomerCount():
    '''
    gets all payments and then gets rid of fee payments to determine a customer count. 

    Arguments:
        none - uses the global variable 'data' as set with the input file
    '''
    starterList = []
    masterList = []
    for line in data:
        accountPayments = re.findall(r'(\d{9}).*?\$(\d+\.\d+)', line)
        starterList.append(accountPayments)
    starterList = [x for x in starterList if x != []]
    for x in starterList:
        masterList.append(x[0])
    i = 1
    while i <= (len(masterList)-1):
        if (masterList[i][0]) != (masterList[i - 1][0]):
            i += 1
            continue
        else:
            del(masterList[i])
    
    print(len(masterList))


def getAndWritePaymentInfo():
    '''
    Gets the payment info from the inputed textfile and writes the relevant data to a csv
    Also saves a copy of the csv to the users desktop
    Arguments:
        none - uses the global variable 'data' as set with setData(fileInput)
    '''
    for line in data:
        date = re.findall((r'\d+/\d+/\d+'), line)
        if date == []:
            continue
        accountNumber = re.findall((r'(\d{9})'), line)
        accountName = re.findall((r'[A-Za-z0-9][A-Za-z0-9]*\s[A-Za-z0-9][A-Za-z0-9]*'), line)
        accountPayment = re.findall((r'\$(\d*,?\d+\.\d+)'), line)
        accountPayment = str(accountPayment[0])
        if ',' not in accountPayment:
            accountPayment = float(accountPayment)
        else:
            accountPayment = accountPayment.replace(',', '')
            accountPayment = float(accountPayment)
        if len(accountName) < 3:
            accountName = ['', 'None']
        paymentInfo = [date[0], accountNumber[0], accountName[1], accountPayment]
        if accountPayment > 1.25:
            csvWriter(paymentInfo)
    if os.name == 'posix':
        posixDesktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        shutil.copy('paymentStats.csv', posixDesktop)
        print('The payment stats have been saved to your desktop!')
    else:
        winDesktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shutil.copy('paymentStats.csv', winDesktop) 
        print('The payment stats have been saved to your desktop!')

def csvWriter(paymentInfo):
    '''
    Writes the Payment information to a csv. the list to use is generated in the getPaymentInfo function.

    Arguments:
        arg1 - a List with the date, accountnumber, accountname, accountpayment
    '''
    with open('paymentStats.csv', 'a') as ps:
        csvWriter = csv.writer(ps)

        csvWriter.writerow(paymentInfo)

getCustomerCount()
getAndWritePaymentInfo()