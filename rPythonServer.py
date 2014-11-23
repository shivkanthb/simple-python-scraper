#!/usr/bin/python2.7
import requests
import MySQLdb #apt-get install python-mysqldb 

from BeautifulSoup import BeautifulSoup
from pprint import pprint

# the follwing three lines are use for the get/post method 
import cgi

form = cgi.FieldStorage() 
value = form.getvalue('infos') # infos is the paramater name of the text box in client side

print "Content-Type: text/html\r\n\r\n" # this must be the first print line to make the following print statements as html code 

linkList=[]
aList=[]
insertList=[]
imgList=[]

# FOR PROXY
# proxy = { "http" : "http://proxy.ssn.net:8080" , "https":"https://proxy.ssn.net:8080"}
# html_code = requests.get('http://www.bseindia.com/markets/Equity/SensexData.aspx', proxies = proxy)

html_code = requests.get('http://www.liveauctioneers.com/') #this is used get the source code of the url provided 

# print html.text  || this will print the obtained source code 
data = html_code.text
soup = BeautifulSoup(data)

# this is for the database connection
conn = MySQLdb.connect(host= "localhost",user="root",passwd="password",db="pythondb") 
cur=conn.cursor() 

# the html code
print "<html>"
print "<body>"
print "<p>"
print "the data from client is :"
print value # this is the data from the client 
print "<hr/>"

cur.execute("delete from pythontable") # this is to remove the existing records from the table

f = open('pythondata.txt', 'w') # this is for creating a file

for base in soup.findAll('div',{"class":"auction_box ml20 online"}):
    for link in base.findAll('div', {"class":"box_title"}):
        al1=link.find('a', {"class":"dark_text text_link"})
        print al1.string # this will print the tag value
        f.write(al1.string) # writing data into the file where f is the file handling object
        f.write('\n')
         
        al2=link.find('a', {"class":"normal_text text_link"})
        print al2.string

        ttime1=base.find('div', {"class":"datetimestamp"})
        print ttime1.string

        ttime2=base.find('abbr')
        print ttime2.string
		
        print "<br/><hr/>"
        try: 
            cur.execute("INSERT IGNORE INTO pythontable VALUES (%s,%s)",(al2.string,ttime1.string))
            # create database perldb;
 		    # use perldb;
            # create table pythontable(item varchar(100),time varchar(100)); 
            conn.commit() 
        except: 
            conn.rollback() 
            

f.close()

conn.commit() 
#print "a tag content:" 
#pprint(aList) 
#print "links :" 
#pprint(linkList) 

conn.close()

# extracting images (also extracting the tag attribute value)

for imgsrc in soup.findAll('img', {"class":"box_image"}):
    print imgsrc.get('src') 
    imgList.append(imgsrc.get('src'))

for i in imgList:
    print "<img src='"+i+"'/>"
    print "<hr/>"    
    
print "</p>"
print "</body>"
print "</html>"