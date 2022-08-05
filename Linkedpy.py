
from re import search
from time import sleep
from traceback import print_exc
from Browser import *
def saverow(sheet_name,*args):
    '''
    enter in the following manner
    ********sheet name**********
    link
    name
    title
    company
    location
    any other
    '''
    row=getmaxrow(sheet_name)+1
    col=1
    for arg in args:
        writetoexcel(sheet_name,row,col,arg)
        col+=1

class Linkedpy(Browser):
    def __init__(self):
        self.username=open("username.txt").read()
        self.password=open("password.txt").read()
        self.browser=Browser(self.username,self.password)
        self.driver=self.browser.driver
    def keepalive(self):
        print("\nall work done , keeping bot alive\n")
        while True:
            time.sleep(1)
    def getprofile(self, link):
        self.driver.get(link)
    def getmessagedict(self):
        max=getmaxrow("message")
        already_messaged={}
        for i in range(1,max+1):
            already_messaged[readfromexcel("message",i,1)]=readfromexcel("message",i,2)
        print("already messaged \n",already_messaged)
        self.already_messaged=already_messaged
    def checkifmessagedalready(self,profile,message):
        try:
            if(self.already_messaged[profile]=="done"):
                return True
        except KeyError:
            pass
        return False
    def send_message(self,profile,message,sleeptimeinseconds):
        if self.checkifmessagedalready(profile,message):
            print("already messaged ",profile)
            return
        self.getprofile(profile)
        try:
            #clicking message button
            print("visiting ",profile)
            time.sleep(3)
            #find message button
            x=self.driver.find_element_by_xpath(
                '/html/body/div[6]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/a'
                +' | '+
                '/html/body/div[5]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/a')
            x.click()
            x=x.get_attribute("href")
            print(x)            
            self.driver.find_element_by_xpath("//*[contains(@aria-label, 'Write a message…')]").send_keys(message)
            #clicking send button
            print("button click")
            time.sleep(3)
            self.driver.find_element_by_xpath("//button[text()='Send']").click()
            print("button clicked")
            time.sleep(3)
            self.driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']").click()
            print("popup closed")
            print("sleeping for ",sleeptimeinseconds," seconds")
            time.sleep(sleeptimeinseconds)
        except:
            print("\ncritical error\n")
            traceback.print_exc()
            time.sleep(1000)  
        
    def getconnections(self):
        try:
            print("getting connections")
            self.driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
            time.sleep(3)
            i=0
            a=[]
            while True:
                i+=1
                try:                                            #/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li[1]/a                                  
                    elements=self.driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li['+str(i)+']/a'
                    +' | '+
                    '/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li['+str(i)+']/a')
                    a.append(elements)
                    print(elements,i)
                except:
                    #traceback.print_exc()
                    break
            elements=[i.get_attribute('href') for i in a]
            print(elements)
            
        except:
            #traceback.print_exc()
            print("limit reached")
        finally:
            pass
        return elements
    def sendmessagetoconnection(self, sleeptimeinseconds=10,limit=10):
        self.getmessagedict()
        count=0
        message=open("message.txt").read()
        for i in self.getconnections():
            count+=1
            self.send_message(i,message,sleeptimeinseconds)
            writetoexcel('message',col=1,row=count+1,value=str(i))
            writetoexcel('message',col=2,row=count+1,value="done")
            if(count==limit):
                print("reached process limit ending")
                break
    def sendinvitetokeywords(self,keywords="programmer",startpage=0,pageno=2,limit=10):
        
        
        f=open("connected.txt","r")
        visited=f.read().split("\n")
        print("already visited ",visited)
        for page in range(startpage,pageno+1):
            links=self.searchforlinks("https://www.linkedin.com/search/results/people/?",keywords,page)
            print("links fetched ",links)
            for link in links:
                if link in visited:
                    print("already invited this person skipping ",link)
                    continue
                if(limit==0):
                    print("limit reached exiting process")
                    break
                print("visiting ",link)
                self.driver.get(link)
                time.sleep(3)
                print("clicking connect button")
                    #/html/body/div[5]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/button[1]
                try:
                    x=self.driver.find_element_by_xpath(
                        '/html/body/div[6]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/button[1]'
                        +' | '+
                        '/html/body/div[5]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/button[1]')
                    x.click()
                    time.sleep(2)
                    self.driver.find_element_by_xpath("//*[contains(@aria-label, 'Send now')]").click()
                    f=open("connected.txt","a")
                    f.write("\n"+link)
                    f.close()
                    limit-=1
                    visited.append(link)
                except:
                    traceback.print_exc()
                    print("could not connect ",link)

    def searchforlinks(self,searchstring="https://www.linkedin.com/search/results/people/?",keywords=None,pageno=None):
        if(keywords):
            if(searchstring!="https://www.linkedin.com/search/results/people/?"):
                searchstring+="&"
            searchstring+="keywords="
            searchstring+=keywords
        if(pageno) :
            if pageno>1:
                searchstring+="&page="
                searchstring+=str(pageno)
        print(searchstring)
        self.driver.get(searchstring)
        time.sleep(3)
        for i in range(1,4):
            time.sleep(2)
            if(i==1):
                self.driver.execute_script("window.scrollTo(0, 0);")                
            else:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/"+str(4-i)+");")
        x=self.driver.find_elements_by_xpath("//a[@class='app-aware-link']")
        
        x=list(set(x))
        #removing duplicates
        for j in range(len(x)):
            try:
                element=x[j]
                x[j]=element.get_attribute("href").split("?")[0]
            except:
                traceback.print_exc()
                print("some problem with this obj \n",x[j])
        print(len(x)," links found")
        
        return x
    def search(self,searchstring,keywords=None,pageno=None):
        x=self.searchforlinks(searchstring,keywords=None,pageno=None)
        
        for j in range(len(x)):
            try:
                self.analyse(x[j],getadvancedinfo=True)
            except:
                traceback.print_exc()
                print("some problem with this link \n",x[j])

    def analyse(self,link,getadvancedinfo=False,name='',title='',company='',location=''):
        array=[]
        try:
            self.driver.get(link)
        except:
            print("link invalid")
            print(link)
            return
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            name=self.driver.find_element_by_class_name('text-heading-xlarge').text
            print(name)
        except:
            traceback.print_exc()
        try:
            job=self.driver.find_element_by_class_name('text-body-medium').text
            if(' at ' in job):
                job=job.split(' at ')
                title=job[0]
                company=job[1]
            else:
                title=job
                
        except:
            traceback.print_exc()  
        try:
            location=self.driver.find_element_by_class_name('pb2').text
            rstring="Contact info"
            if rstring in location:
                location=location.replace(rstring,"")
            print(location.split('\n'))
        except:
            traceback.print_exc()
        time.sleep(3)
        if(getadvancedinfo):
            self.driver.get(link+"/detail/contact-info/")
            contact_page=self.driver.find_element_by_tag_name('body').text
            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", contact_page)
            print(emails)
            for i in emails:
                array.append(i)

            '''email number website'''
            phno = re.findall(r"\+[-()\s\d]+?(?=\s*[+<])", contact_page)  
            print(phno)
            for i in phno:
                array.append(i)
                
            webiste = re.findall(r"[A-Za-z0-9]+\.[A-Za-z0-9]+\.*[A-Za-z0-9]*", contact_page)  
            print(webiste)
            for i in webiste:
                i.lower()
                if 'linkdein' not in i:
                    array.append(i) 
        saverow("database",link,name,title,company,location,*array)
#searchstring="https://www.linkedin.com/search/results/people/?"
#keywords=input("enter the keywords ")
#pageno=int(input("enter no of pages to search "))
#obj.search(searchstring,keywords,pageno)
def loop():
    obj=Linkedpy()
    #sending message to connections
    obj.sendmessagetoconnection(sleeptimeinseconds=60)
    obj.sendinvitetokeywords()
    obj.leave()
import schedule
schedule.every().day.at("08:30").do(loop)

while True:
    schedule.run_pending()
    time.sleep(1)