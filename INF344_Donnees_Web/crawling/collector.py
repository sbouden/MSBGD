# -*- coding: utf-8 -*-
# écrit par Jean-Claude Moissinac, structure du code par Julien Romero

from sys import argv
import sys
import urllib.request
import requests
from bs4 import BeautifulSoup
import time
import re

if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode

class Collecte:
    """pour pratiquer plusieurs méthodes de collecte de données"""

    def __init__(self):
        """__init__
        Initialise la session de collecte
        :return: Object of class Collecte
        """
        # DO NOT MODIFY
        self.basename = "collecte.step"
        self.name = "sbouden"

    def collectes(self):
        """collectes
        Plusieurs étapes de collectes. VOTRE CODE VA VENIR CI-DESSOUS
        COMPLETER les méthodes stepX.
        """
        self.step0()
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()

    def step0(self):
        # cette étape ne sert qu'à valider que tout est en ordre; rien à coder
        stepfilename = self.basename+"0"
        print("Comment :=>> Validation de la configuration")
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(self.name)
        
    def step1(self):
        stepfilename = self.basename+"1"

        # votre code ici
       
        # ----------- method 1:
        url = urllib.request.Request("http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&query_txt=video&submit=&patents=on")
        
        with urllib.request.urlopen(url) as response:
            result = str(response.read())
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
        
        #----------- method 2:
        # url = "http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&query_txt=video&submit=&patents=on"
        # r = requests.get(url)
        # result = r.text
        # print(result)

        
    def step2(self):
        stepfilename = self.basename+"2"
        result = ""
        
        # votre code ici
        links = []
        resfile = open(self.basename+"1", 'r').read()
        soup = BeautifulSoup(resfile, 'html.parser')
        
        for link in soup.findAll('a'):
            l = str(link.get('href'))
            if l != 'None':
                links.append(l)
        # print('----------------------links step2 -----------------------\n', links)
        res_step2 = "\n".join(links)
        
        print("length links step 2: -------------------> ",len(links))
        print("length step 2 set(result): -----------------> ", len(set(res_step2)))
        print("--------------- result step2 ------------------------\n", res_step2)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(res_step2)
        
    def linksfilter(self, links):
        #flinks = links
        
        # votre code ici
        filt = ['/', '/services.html', '/contact.html', '/privacy.html', '/register.html', '/tools-resources.html', 'https://twitter.com/FPOCommunity', 'http://www.linkedin.com/groups/FPO-Community-4524797', 'http://www.sumobrainsolutions.com/']
        flinks = []
        
        for l in sorted(set(links)):
            if not l in filt and not l.startswith("result.html") and not l.startswith('http://research') and not l.startswith('/search.html'):
                flinks.append(l)
        
        flinks = [l for l in flinks if "result.html" not in l] 
        return sorted(flinks)
        
    def step3(self):
        stepfilename = self.basename+"3"
        result = ""
        # votre code ici
        result = self.linksfilter(open(self.basename+"2", 'r').read().splitlines())
        
        res_step3 = "\n".join(result)
        print('----------result step3 ----------------------------------------')
        print(res_step3)

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(res_step3)
        
    def step4(self):
        stepfilename = self.basename+"4"
        result = ""
        
        # votre code ici
        # resfile3 = open(self.basename+"3", 'r').read().splitlines()
        # step3_links10 = list(resfile3)[:10]
        resfile3 =  list(open(self.basename+"3", "r", encoding="utf-8").read().splitlines())[:10]

        res = []
        for link in resfile3:
            url = urllib.request.Request('http://www.freepatentsonline.com/' + str(link))
            
            with urllib.request.urlopen(url) as response:
                result = str(response.read())
            soup = BeautifulSoup(result, 'html.parser')
            
            links = []
            for link in soup.findAll('a'):
                links.append(str(link.get('href')))
    
            result = "\n".join(self.linksfilter(links))
        
            res.append(result)
            time.sleep(2)
            
        res = list(dict.fromkeys(res))
        res_step4 = '\n'.join(sorted(res))
        print('-----------resultat step4: ---------\n', res_step4)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(res_step4)
    
    
    def contentfilter(self, link):
        soup = BeautifulSoup(link, 'html.parser')
        
        # interest=[]
        
        inventors = soup.find_all(text=re.compile('Inventors:'))
        title = soup.find_all(text=re.compile('Title:'))
        AN = soup.find_all(text=re.compile('Application Number:'))
        
        if inventors is not None and title is not None and AN is not None:
            return True
        else:
            return False


    def step5(self):
        stepfilename = self.basename+"5"
        result = ""
        # votre code ici
        
        # for link in sorted(links_html):
        #     while len(links) < 10:
        #         url = 'http://www.freepatentsonline.com' + str(link)
        #         result = str(urllib.request.urlopen(url).read())
            
        #         if self.contentfilter(result) and result not in links:
        #             links.append(result)
        #             if len(links)>10:
        #                 break
        
        
        resfile4 =  list(open(self.basename+"4", "r", encoding="utf-8").read().splitlines())
        links_html = sorted([l for l in resfile4 if "html" in l])
        links=[]
        for link in links_html:
            if len(links)>10:
                break
            url = urllib.request.Request('http://www.freepatentsonline.com' + str(link))
            with urllib.request.urlopen(url) as response:
                result = str(response.read())
                
            soup = BeautifulSoup(result, 'html.parser')
             # if self.contentfilter(link) and result not in links:
                #     links.append(link)
            for div in soup.findAll('div'):
                # if self.contentfilter(link) and result not in links:
                #     links.append(link)
                inventors = div.find_all(text=re.compile('Inventors:'))
                title = div.find_all(text=re.compile('Title:'))
                application = div.find_all(text=re.compile('Application Number:'))
                if inventors is not None and title is not None and application is not None:
                    links.append(link)
                    links = list(set(links))
                    if len(links) > 10:
                        break
    
        res_step5 ='\n'.join(sorted(set(links))[:10])
        print('---------- step5: ---------\n', res_step5)


        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(res_step5)
        
    def step6(self):
        stepfilename = self.basename+"6"
        result = ""
        inventorlist = []

        # votre code ici
        resfile5 =  list(open(self.basename+"5", "r", encoding="utf-8").read().splitlines())[:5]
        
        for link in resfile5:
            url = urllib.request.Request('http://www.freepatentsonline.com' + str(link))
            
            with urllib.request.urlopen(url) as response:
                result = (response.read()).decode('utf-8')
            
            soup = BeautifulSoup(result, 'html.parser')

            inventors = soup.find_all(text=re.compile('Inventors:'))
            divs = [inventor.parent.parent for inventor in inventors]
        
            for d in divs[0].descendants:
                if d.name == 'div' and d.get('class', '') == ['disp_elm_text']:
                    inventorlist.append(d.text)
                    print(inventorlist)
        
        result = '\n'.join(inventorlist)
        print(result)
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)

        
if __name__ == "__main__":
    collecte = Collecte()
    collecte.collectes()
