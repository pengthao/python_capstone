# Intro
    Hi, my name is Peng,  Having worked as a data analyst, I'm excited to leverage my skills as I journey into software development. This Python programming class has been a lot of fun, and I'm looking forward to learning more. To continue my growth, I find myself looking for new opportunities. I thought I would create an application that could help me with finding a job.

## Elevator Pitch
    My capstone project aims to centralize job searches by scraping the postings from multiple sites and aggregating them into one location where you can more easily manage them. You can select your favorite listings and update your current interest or application status here.

## Demo
    This application is built using python's Flask framework and the loginManager, Blueprints, and FlaskForms extensions.

    The loginManager decorates my functions that manage access to certain features. We can register and log in to access these features. 

    The password is encrypted using the bcrypt extension which generates a hash and salts the password entered and saves it to the postgres database. Upon login the password  submitted is salted and compared to see if we should be authenticated.

    Once we're logged in we have access to the myJobs link above that shows us jobs that we have selected as our favorites. We are redirected to our search page where we can search using keywords, location and radius of your search.

    I'll test with python, minneapolis, 5 miles

    I built a spinning animation in css to let the user know the program is thinking while we wait since the scraping takes a bit of time to gather all the jobs.

    This search engine goes through a proxy browser called Bright Data to bypass anti-bot measures and pulls the html of the target site using Playwright. From there I use Beautiful Soup to parse through the HTML to extract the data and send it to my database. 
    
    This was actually the most difficult part of my project. I had to do a bit of digging before I could figure out a way to bypass botcontrols.

    The search keyword pulls the entries from the database and the jobs render on to the page. I used jinja templates to construct my html pages and flask forms for any forms that require submitting information. My favorites toggle feature uses ajax to pass information to the server and add or delete favorites jobs to the user_jobs table.

    I can change the status of the job im interested in, to applied or accepted or uninterested if I want to remove it from my list.

    I also have a sorting feature that organizes my list by status or last modified date.

## Thoughful End
    My favorite thing about the project was the little loading animation I built. I was anxious about how long the page would be blank waiting for my program to process and that simple animation made me feel a little bit better about the wait. Thanks for looking at my project.
