import os
import csv
import re

cleanCSV = open('paymentStats.csv', 'w+')
headerReset = csv.writer(cleanCSV)
headerReset.writerow(['Date', 'Account Number', 'Account Name', 'Payment Amount'])
cleanCSV.close()


