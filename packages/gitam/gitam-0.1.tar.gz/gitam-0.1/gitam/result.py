import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

class Result:
    
    
    def __init__(self, roll_id, semester=1):
        self.roll_id = roll_id
        self.semester = semester
        soup = self.__retrieve_data(semester)
        name = soup.find(id='lblname').text
        branch = soup.find(id='lblbranch').text
        cgpa = soup.find(id="lblcgpa").text
        try:
            self.cgpa = float(cgpa)
            self.name = name if name != 'lblname' else None
            self.branch = branch if branch != 'lblbranch' else None
        except:
            print("Invalid ID")
    
    def __retrieve_data(self, semester):
        
        def payload(semester, roll_id):
            return {'__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': '/wEPDwULLTE3MTAzMDk3NzUPZBYCAgMPZBYCAgcPDxYCHgRUZXh0ZWRkZKKjA/8YeuWfLRpWAZ2J1Qp0eXCJ',
                    '__VIEWSTATEGENERATOR': '65B05190',
                    '__EVENTVALIDATION': '/wEWEwKj/sbfBgLnsLO+DQLIk+gdAsmT6B0CypPoHQLLk+gdAsyT6B0CzZPoHQLOk+gdAt+T6B0C0JPoHQLIk6geAsiTpB4CyJOgHgLIk5weAsiTmB4CyJOUHgKL+46CBgKM54rGBmNcJmDHh2N2wm5IIEW9ehmrpyHJ',
                    'cbosem': str(semester),
                    'txtreg': str(roll_id),
                    'Button1': 'Get Result'}
        
        with requests.Session() as s:
            r = s.post('https://doeresults.gitam.edu/onlineresults/pages/newgrdcrdinput1.aspx',
                       data = payload(semester, self.roll_id))
            r = s.get('https://doeresults.gitam.edu/onlineresults/pages/View_Result_Grid.aspx')
            return BeautifulSoup(r.text, "html.parser")
        
    def __extract_data(self, soup):
        try:
            df = pd.read_html(str(soup.find("table", {"class": "table-responsive"})))[0]
            subjects = []
            gpa = float(soup.find(id="lblgpa").text)
            cgpa = float(soup.find(id="lblcgpa").text)
            subjects = []
            for i in df.values:
                subjects.append(dict(zip(["code","name","credits","grade"],i)))
            return {
                "subjects": subjects,
                "gpa": gpa,
                "cgpa": cgpa
            }
        except Exception as e:
            return None
        
    def plot_cgpa(self):
        gpa = []
        sem = []
        for i in range(1,9):
            soup = self.__retrieve_data(i)
            data = self.__extract_data(soup)
            if data != None:
                gpa.append(data["gpa"])
                sem.append(str(i))
        print(gpa)
        fig, ax = plt.subplots()
        plt.ylim(0,10)
        ax.set(title = "Academic Graph",
               xlabel = "Semesters", 
               ylabel = "GPA")
        ax.bar(sem, gpa)
        plt.show();