from tkinter import *
from bs4 import BeautifulSoup
import requests
import time
import threading



def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    job_list = ""
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(" ", "")
            skills = job.find('span', class_='srp-skills').text.replace(' ', '')
            more_info = job.header.h2.a['href']
            if unfamiliar_skill.get() not in skills:
                job_list += f'Company Name: {company_name.strip()} \n'
                job_list += f"Required Skills: {skills.strip()} \n"
                job_list += f'More Info: {more_info} \n' + "\n"
                print(f"File saved: {index}")
    text_area.config(state=NORMAL)      
    text_area.delete(1.0, END)
    text_area.insert(END, job_list)
    text_area.config(state=DISABLED)
        
    if  __name__ == "__main__":
        while True:
            find_jobs()
            time_wait = 10
            print(f"Waiting {time_wait} minutes...")
            time.sleep(time_wait*60)

def start_scraping():
    # Start the scraping function in a separate thread to avoid blocking the GUI
    thread = threading.Thread(target=find_jobs, daemon=True)
    thread.start()


root = Tk()
root.title("JOB FINDER")
label = Label(root, text =" Enter Unfamiliar Skills").grid(row = 0, column= 0)


button = Button(root, text="Generate Recent Jobs", command=start_scraping).grid(row=1, column=0, columnspan=2)
unfamiliar_skill = Entry(root)
unfamiliar_skill.grid(row=0, column= 1)
text_area = Text(root, wrap=WORD, height=20, width=170)
text_area.grid(row=2, column=0, columnspan=2)
text_area.config(state = DISABLED)
root.mainloop()