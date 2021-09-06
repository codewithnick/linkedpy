
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

class Linkedpy:
    def __init__(self):
        self.username="bsccs45@gmail.com"
        self.password="bsccs45"
        self.browser=Browser(self.username,self.password)
        self.driver=self.browser.driver

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
                self.analyse(x[j],getemail=True)
            except:
                traceback.print_exc()
                print("some problem with this link \n",x[j])

    def analyse(self,link,getemail=False,name='',title='',company='',location=''):
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
        if(getemail):
            self.driver.get(link+"/detail/contact-info/")
            contact_page=self.driver.find_element_by_tag_name('body').text
            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", contact_page)
            print(emails)
            '''email number website'''
        saverow("database",link,name,title,company,location)
searchstring="https://www.linkedin.com/search/results/people/?"
#keywords=input("enter the keywords ")
#pageno=int(input("enter no of pages to search "))
obj=Linkedpy()
