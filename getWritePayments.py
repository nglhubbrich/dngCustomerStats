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
    This little buddy can be used to grab all of the account information in a given time from the payment report from L-Boss Reports. On prompt it will require a .txt format of the report you want to get info from. Once entered it will give you an accurate customer count as well as write out each customers payment to a csv file. Best use of this script will be to run it monthly to keep a running csv formatted list of all DNG payments. 

    NOTE: writing to the csv file will APPEND to the csv file. If you run this program more than once on the same file it will write the information again, causing multiple rows of the same information!
'''
#IMPOTED MODULES
import csv
import re
import os
import shutil
import datetime as datetime

#INITIALIZATION AND ASSIGNMENTS
currentMonth = datetime.date.today().strftime('%B')
monthlyCSV = currentMonth + 'Customer' + 'Data' + '.csv'

with open(monthlyCSV, 'w+') as mcsv:
    csvWriterMonthly = csv.writer(mcsv)
    setHeader = csv.writer(mcsv)
    setHeader.writerow(['Date', 'Account Number', 'Account Name', 'Payment Amount'])

#try to get the report file name from the user
while True:
    fileFromInput = input('What is the name of the file?(include the full file path! i.e: C:/Users/LBoss/Desktop/februarypayments.txt): ')
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
        none - uses the variable 'data' as set with the input file
    '''
    # Initialize some lists to pack the values into
    starterList = []
    masterList = []
    
    # Grab all the payments that are on the same line as an account number.
    # the List comprehension gets rid of empty values the regex includes
    for line in data:
        accountPayments = re.findall(r'(\d{9}).*?\$(\d+\.\d+)', line)
        starterList.append(accountPayments)
    starterList = [x for x in starterList if x != []]
    
    # Pack our payments left in starterList into the masterList
    for x in starterList:
        masterList.append(x[0])
    
    # Set the initial index for the while loop below
    i = 1

    # this checks whether or not two payments in our masterList have the same
    # account number consecutively. In the file, a fee payment is directly after the actual payment
    # so by checking if two account numbers occur consecutively, we can get rid of one of
    # them so we only count that transaction as one customer. SEE README.md for fee removal vs 
    # line removal
    while i <= (len(masterList)-1):
        if (masterList[i][0]) != (masterList[i - 1][0]):
            i += 1
            continue
        else:
            del(masterList[i])
    
    #print out the count
    print(len(masterList))


def getAndWritePaymentInfo():
    '''
    Gets the payment info from the inputed textfile and writes the relevant data to a csv
    Also saves a copy of the csv to the users desktop
    Arguments:
        none - uses the variable 'data' as set with the input file
    '''
    for line in data:
        # All our relevant lines start with a date, so check if the line starts with a date
        date = re.findall((r'\d+/\d+/\d+'), line)
        if date == []:
            continue
        
        #grab the account number, easy enough
        accountNumber = re.findall((r'(\d{9})'), line)
        
        #grab the account name, this grabs more than it needs to, because it handles weird names
        #and because the names can contain numbers. The most appropriate name is the second item
        #in the list. (accountName[1])
        accountName = re.findall((r'[A-Za-z0-9][A-Za-z0-9]*\s[A-Za-z0-9][A-Za-z0-9]*'), line)
        
        #The account payment is a touh tricky because of the text formatting. Here we grab 
        #the payment, turn it into a string so that we can strip any commas if needed and then 
        #turn that into a float
        accountPayment = re.findall((r'\$(\d*,?\d+\.\d+)'), line)
        accountPayment = str(accountPayment[0])
        if ',' not in accountPayment:
            accountPayment = float(accountPayment)
        else:
            accountPayment = accountPayment.replace(',', '')
            accountPayment = float(accountPayment)
        
        #a little handling in case the name on the account is blank. No idea how there is an
        #account with no name, but it happens so...here
        if len(accountName) < 3:
            accountName = ['', 'None']
        
        #make the list to write out to the csv
        paymentInfo = [date[0], accountNumber[0], accountName[1], accountPayment]
        
        #but only if it isn't a fee payment. SEE README.md for fee removal vs line removal
        if accountPayment > 1.25:
            csvMasterWriter(paymentInfo)
            csvMonthlyWriter(paymentInfo)

    #get OS and desktop path to save a copy of the csv that the user can do with what
    # they choose, leaving a master copy in the directory        
    if os.name == 'posix':
        posixDesktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        shutil.copy('paymentStats.csv', posixDesktop)
        shutil.copy(monthlyCSV, posixDesktop)
        os.remove(monthlyCSV)
        print('The payment stats have been saved to your desktop!')
    else:
        winDesktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shutil.copy('paymentStats.csv', winDesktop)                 
        shutil.copy(monthlyCSV, winDesktop)
        os.remove(monthlyCSV)
        print('The payment stats have been saved to your desktop!')

def csvMasterWriter(paymentInfo):
    '''
    Writes the Payment information to the master csv file kept in the directory. the list to use is generated in the getPaymentInfo function.

    Arguments:
        arg1 - a List with the date, accountnumber, accountname, accountpayment
    '''
    with open('paymentStats.csv', 'a') as ps:
        csvWriterMaster = csv.writer(ps)

        csvWriterMaster.writerow(paymentInfo)

def csvMonthlyWriter(paymentInfo):
    currentMonth = datetime.date.today().strftime('%B')
    monthlyCSV = currentMonth + 'Customer' + 'Data' + '.csv'

    with open(monthlyCSV, 'a') as mcsv:
        csvWriterMonthly = csv.writer(mcsv)
        csvWriterMonthly.writerow(paymentInfo)

getCustomerCount()
getAndWritePaymentInfo()