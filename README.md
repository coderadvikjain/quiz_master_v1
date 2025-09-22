## Readme

 
  <h3 align="center">MAD1 Project </h3>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#technology-used">Technology-Used</a>
    </li>
    <li>
      <a href="#installation-guide">Installation Guide</a>
    </li>
    <li><a href="#usage">Usage of application</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

This Project is made by Jatin Nahata,
for Modern Application Development 1 (MAD-I) course project.

Main theme of this project is to make a Quiz Master application, 
which help students to prepare for various courses,
enabling it for users(students) to explore quizzes that are available for
courses, chapters and can see there scores after attending a quiz.
admin has CRUD control over Courses, Chapters, Quizzes and Questions.
admin can see users which registered themself for preparation.

<p align="right">(<a href="#readme">go to top</a>)</p>

## Technology Used

* Flask: for request handling, rendering templates, defining views/routes to the application
* Flask Sqlalchemy: defining models, doing query operations on the database, committing changes to the database.
* Jinja2 (automatically integrated by flask): for templating, provides more flexibility to the html document.
* Sqlite: for database tables
* Datetime:  useful to track timer
* Flask Restful: useful for building APIs


<p align="right">(<a href="#readme">go to top</a>)</p>

## Installation Guide

To run the application install create a virtual environment by using ‘python -m venv venv'
Now, enable created the environment you have, by running “venv\Scripts\activate” command on terminal.
After creating a virtual environment, run command 'pip install -r requirements.txt' and then all required packages will be installed. and then run the “app.py” file using the “python” command on the terminal. 
               Or
Simply, run command 'pip install -r requirements.txt' and then all required packages will be installed. and then run the “app.py” file using the “python” command on the terminal. 

<p align="right">(<a href="#readme">go to top</a>)</p>

## Usage

The app has two types of roles:
1. User : By registering, anyone can get a user role, with user role users can explore quizzes that are available, attempt a quiz, can see there scores after completion.
2. Admin : Admin can only be added in the backend (auto created when database is setup), admin can login as normal users and they will be redirected to the admin page. With an admin role, admin can have CRUD control over courses, chapters, quizzes and questions.
admin can see users which registered themself for preparation.

default admin credentials is username: 'admin' and password is 'iitm@1705'

<p align="right">(<a href="#readme">go to top</a>)</p>

## Contact

Jatin Nahata - 23f2001705@ds.study.iitm.ac.in

Project Report: [Project Report](https://github.com/23f2001705/quiz_master_v1/blob/main/Project%20Report.pdf)

<p align="right">(<a href="#readme">go to top</a>)</p>
