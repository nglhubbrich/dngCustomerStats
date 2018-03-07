# dngCustomerStats

## Get meaningful data from an existing report and save it in a useful format.

### Features
  - **Gives an accurate count of the amount of customers for a given timeframe.**
    - the timeframe is determined by the report you create. If you choose February 12th - 21st, and run it through this program, it will give you the amount of customers for that timeframe. *this is not reccomended. see usage below*
  - **Writes out each payment transaction to a continuous .csv file.**
    - the master .csv, paymentStats.csv, is located in the program directory, and holds every payment transaction run through the program. A copy of paymentStats.csv is also saved to your desktop.
    - it holds 4 columns, Date of payment, Account Number, Account Name, and Payment amount.
  - **Creates a Monthly Stats .csv**
    - All of the current data that was added to the master .csv will also be saved in a monthly .csv file on your desktop. 
    - Formatted the same as paymentStats.csv, but will only contain the current months payment data.

### Requirements:
  - Payment Report from L-Boss in a text file format.
  - Python installed on your computer (I have not done any testing on versions under 3.6.4, but I can't see anything going wrong if you have anything less)

### Usage

The sole purpose of this program is make it easier to get a monthly customer count(more details on this in a moment) as well as saving that months data in a useful format for analysis, and therefore, it is inteded to only be used monthly. As noted in the features section, it is not reccomended to run on partial dates, as this will add, and potentially duplicate, parts of the data. 

Hopefully in the near future, there will be a feature added that lets you choose if you want to only obtain a customer count, or only write out a data .csv, or a combination of both. check back here to see if that has been added:
  - [ ]Just like Burger King, you can have it your way! 'Choose what you want to do' has been added! 

##### Getting the report to use
In order to use this friendly little helper, you need a text file version of the payment report from L-Boss. This is easy to get: Go to the report section in L-Boss and choose PayPal Payments (the title of this report is misleading, it actually has all payments made to account holders, independant of method.) Once the report loads, in the file menu, choose 'Save report as text file'. Give it a proper name (like: februaryPayments.txt), and save it in an easy to remember place (you need this path name to enter in when you run the program, so choose a place thats simple, like C:/Users/LBoss/februaryPayments.txt as opposed to C:/Users/LBoss/Desktop/PaymentFiles/February Payment Reports/februaryPayments.txt)

##### Running the program
Currently, this is a Command-Line Interface program. In your Human language, that means that there is no pretty windows or click buttons or pictures of cats and things in the background. It is run from the command line and it asks you a question that you need to answer, also known as interfacing, hence: Command-Line Interface. Still super simple though:
  - **open a command prompt**
    - click in the search bar beside the start menu and type 'cmd'. Double click on Command Prompt in the list of results
  - **change directories to the program directory**
    - where ever you saved this program, that is its directory. If it was in C:/Users/Lboss/dngCustomerStats use the 'cd' command by typing:
          `cd C:/Users/Lboss/dngCustomerStats` and hit 'enter'
  - **run the program**
    - Now that you are in the right directory, you can run the program by typing:
          `python dngCustomerStats.py`
  - **enter the name of the payment report text file**
    - It will ask which file you want to run it on, enter in the complete file path as discussed above and hit enter
  - **DONE!**
    - Yay! You are finished! It will return a prompt saying the total amount of customers for that month, and let you know that your files have been saved! Go grab a coffee and hang out for the rest of the day...or work. Probably work, but I'm not telling you what to do. You do you.

Hopefully sometime in the future I will make it all GUI (not Command-Line Interface) and maybe compile a version for windows so you don't have to run it in a command prompt. Check back here to see if it has been added:
  - [ ]Oooooo! It's so GUI! 
  - [ ]Unlike your future prison cell, this suckers got windows!

##### Helpful Hints
  - Save the report in the same directory as the program to alleviate having to type the entire path. You can then just simply type the name of the report without all the file path mumbo-jumbo.
  - That's really all I got. It's a pretty simple program.

##### Fee Removal vs Line Removal for Accurate Customer counts
Here's the business: Getting a customer count is a touch lossy no matter which way you do it. There are two main ways(proabably a whole lot more, but I like these two and I wrote it, so, yeah.): Don't count a line based on whether it contains a fee payment. And, Don't count a line based on whether it appears directly after a line with the same account number. 

Both of these methods will effectively remove unwanted 'Customer Counts' but also have their own drawbacks. We'll go through one at a time.

###### Fee Removal
All this method does is checks whether or not a line *looks* like a fee, and if it does, doesn't count it. The PayPal fees are 2% of the total up to a maximum of $1.25. So, if the payment is $1.25 or lower, don't count that line as an actual payment. The catch: an actual order could be for less than $1.25. You would think, who would bring in only $0.80 to the Drop and G0!?!?! and most people would not, however, it could still happen. So for the 99% of customers, this will work, but you run the risk of eliminating an actual customer payment, causing the customer count to be off.

Good Example:
```
2/17/18   096100000   Some Dude         Account Payment   $12.50
2/20/18   096100001   Another Dude      Account Payment   $22.35
2/25/18   096100002   Different Dude    Account Payment   $42.25
2/25/18   096100002   Different Dude    Account Payment   $0.85
```
Here we see that clearly that second payment for Different Dude is a fee, so we should have 3 customers counted.

Bad Example
```
2/17/18   096100000   Some Dude         Account Payment   $12.50
2/20/18   096100001   Another Dude      Account Payment   $0.35
2/25/18   096100002   Different Dude    Account Payment   $42.25
2/25/18   096100002   Different Dude    Account Payment   $0.85
```
Here, Another Dude has just brought in like 7 beer bottles, so his actual order is only $0.35, but we get rid of things that *look* like fees, so here we would only count 2 customers.

###### Line Removal
The other method is to disregard an entire line if the line just before it had the same account numbers. This works because a fee payment is directly after its sister, the regular payment. it doesn't work if there has been one customer bringing in back to back orders, because the payments will be back to back, causing one to get deleted.
The other fault is that if there are any mistakes made and corrected (dng Cheque entered wrong and then reversed and reentered), they will be recorded as well, causing one to be added. 

Good Example
```
2/17/18   096100000   Some Dude         Account Payment   $12.50
2/20/18   096100001   Another Dude      Account Payment   $0.35
2/25/18   096100002   Different Dude    Account Payment   $42.25
2/25/18   096100002   Different Dude    Account Payment   $0.85
```
Here, it would get rid of that fee payment because of the double account numbers, but doesn't get rid of Another Dude's small payment, so, accurately, we count 3 customers.

Bad example
```
2/17/18   096100000   Some Dude         Account Payment   $12.50
2/18/18   096100000   Some Dude         Account Payment   $22.80
2/20/18   096100001   Another Dude      Account Payment   $0.35
2/25/18   096100002   Different Dude    Account Payment   $42.25
2/25/18   096100002   Different Dude    Account Payment   $0.85
```
Although, here it fails because as you can see, Some Dude comes in on the 17th and the 18th, which would be 2 customers. The program only counts it as one because it will get rid of the second payment and will only count 3 instead of the 4 it should be.

###### So...which to use?
Why not both! I used one of each, but for different tasks. 
For getting a simple count of how many customers used the Drop and Go, I used line removal. There actually aren't that many occasions when we have back to backs. And also, the difference between 137 customers and 139 customers out of 7000 and some is negligble. 
For writing out the results to a csv file, I used the fee removal method. While we may lose a few orders if they end up being tiny, but all of the other errors from line removal will actually get written out, so we can identify the errors if they are present.
Also they both fail on different tests, so I find it useful to use one to verify the other. If the csv file has less lines than the program says customers, then it might have missed one and you can find that. Vice Versa, same thing. If they are the same, WOOHOO!! excellent.

##### Support
If you are having trouble with it or anything, shoot me an email and I can see if I can help out! nglhubbrich.assistance@gmail.com

