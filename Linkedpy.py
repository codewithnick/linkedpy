
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
        self.username="bsccs45@gmail.com"
        self.password="bsccs45"
        self.browser=Browser(self.username,self.password)
        self.driver=self.browser.driver
    def keepalive(self):
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
        if(self.already_messaged[profile]=="done"):
            return True
        return False
    def send_message(self,profile,message):
        if self.checkifmessagedalready(profile,message):
            print("already messaged ",profile)
            return
        self.getprofile(profile)
        try:
            #clicking message button
            print("visiting ",profile)
            time.sleep(3)
            #x=self.driver.find_element_by_xpath("/html/body/div[2]/section[1]/a").get_attribute("href")
            #//*[@id="ember1329"]/div[2]/div[3]/div/a
            #/html/body/div[6]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/a
            #<a href="/messaging/thread/new?recipients=List(urn%3Ali%3Afsd_profile%3AACoAADbO7qYBIkgepIc-TGxq2MTXmL5D3RKYM4I)&amp;composeOptionType=CONNECTION_MESSAGE&amp;controlUrn=compose_message_button&amp;referringModuleKey=NON_SELF_PROFILE_VIEW" class="message-anywhere-button pvs-profile-actions__action artdeco-button " disabled="" role="button">
            #<!---->Message</a>
                                                #/html/body/div[5]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/a
            x=self.driver.find_element_by_xpath(
                '/html/body/div[6]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/a'
                +' | '+
                '/html/body/div[5]/div[3]/div/div/div/div/div[3]/div/div/main/div/section/div[2]/div[3]/div/a')
            x.click()
            x=x.get_attribute("href")
            print(x)
            #self.driver.get(x)            
            #sending text
            #time.sleep(1000)    
            
            self.driver.find_element_by_xpath("//*[contains(@aria-label, 'Write a message…')]").send_keys(message)
            #self.driver.find_element_by_tag_name("textarea").send_keys(message)
            #clicking send button
            print("button click")
            time.sleep(3)
            self.driver.find_element_by_xpath("//button[text()='Send']").click()
            print("button clicked")
            time.sleep(3)
            #/html/body/div[6]/aside/div[2]/header/section[2]/button[3]
            #/html/body/div[6]/aside/div[2]/header/section[2]/button[3]
            self.driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']").click()
            print("popup closed")
            #self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/form/div[4]/button").click()
            #id is <textarea id="messaging-reply" class="medium" name="message" placeholder="Write a message…"></textarea>
            time.sleep(3)            
        except:
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
                    #//*[@id="ember189"]/div[2]/div[1]/ul/li[2]/div[1]
                    #/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li[2]/div[1]/a/span[2]
                    #/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li[1]/div[2]/a
                    #/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li[1]/a 
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

        #/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[1]/ul/li/div[2]/a
    def sendmessagetoconnection(self):
        self.getmessagedict()
        count=0
        for i in self.getconnections():
            count+=1
            message=open("message.txt").read()
            self.send_message(i,message)
            writetoexcel('message',col=1,row=count+1,value=str(i))
            writetoexcel('message',col=2,row=count+1,value="done")
            
    def search(self,searchstring,keywords=None,pageno=None):
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
        print(len(x)," links found")
        for j in range(len(x)):
            try:
                element=x[j]
                x[j]=element.get_attribute("href").split("?")[0]
            except:
                traceback.print_exc()
                print("some problem with this obj \n",x[j])
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
obj=Linkedpy()
#obj.search(searchstring,keywords,pageno)
obj.sendmessagetoconnection()
obj.keepalive()