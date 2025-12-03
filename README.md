# Flashcard Tool 
This is a software design project that mimics flashcards practice used to help with students' review session for exams, quizzes, and assignments. 

Team Members: Kimheat Chheav and Saba Ali

# OIM 3640: Final Reflection 

## Section 1: Big Idea & Purpose: 
Modern students often study from scattered materials—lecture notes, PDFs, and shared documents—without a simple way to turn that content into active recall practice. Our project aims to solve that problem by building a browser-based flashcard quiz tool where users can upload their own question sets or create them manually, then practice in an interactive, structured way. Instead of relying on a fixed, pre-built deck, the tool lets users define their own “flashcard sets” as .txt or .json files and reuse them across multiple sessions. We designed the system to emphasize mastery, not just completion: missed questions are automatically repeated at the end of a quiz, so learners get extra exposure to the material they struggle with. At the same time, we wanted to practice real-world software design skills by building a full Flask web app with routes, templates, file handling, and session management. The end goal was to create something both useful as a study tool and meaningful as a portfolio piece that shows we can design, implement, and refine a small but complete web application.

## Section 2: User Instructions/ ReadME
1. Make sure you have Python 3 installed
2. Install the required Flask: pip install flask
3. From the project root (the folder containing quiz_app.py and the templates folder), run: python quiz_app.py
4. Open your browser and go to: http://127.0.0.1:5000/
5. You’ll see the home page with navigation to:
- Upload a question file
- Add your own questions
- Select a quiz set and start practicing

Supported Question Formats: 
- Text files (.txt)
    - Each question must end with a ?
    - The next line is the answer
    - Blank lines are allowed between Q&A pairs

    Ex: 
    What is the capital of France?
    Paris

    Who founded Babson College?
    Roger Babson
- JSON files (.json) created by the app when you add your own questions are stored in the flashcard_sets folder with this structure:
{
  "questions": [
    { "question": "What is 2 + 2?", "answer": "4" },
    { "question": "What color is the sky?", "answer": "blue" }
  ]
}

Basic User Flow
- Upload: Go to the Upload page, submit a .txt file, and the app stores it as a set in flashcard_sets/.
- Add Question: Use the Add Question page to either create a new set or add questions to an existing one; these are saved as .json sets.
- Select Set: On the Select Quiz Set page, choose from all available .txt and .json sets.
- Quiz: The app shows one question at a time, checks your answer, and gives instant feedback. At the end of the pool, any questions you missed are automatically repeated until you’ve cycled through them again, and then you see your final score.

## Section 3: Implementation Information
Our flashcard tool is implemented as a Flask web application that manages question sets, quiz state, and user interaction through a set of clearly defined routes. All sets are stored in a flashcard_sets directory, and the helper functions load_questions() and save_questions() handle reading and writing questions from .txt and .json files. The upload route (/upload) lets users submit a .txt file; the app parses it into question–answer pairs and saves it as a named set. The Add Question route (/add_question) supports either creating a brand-new set or appending to an existing one, storing everything in a consistent JSON structure under the "questions" key. When a user selects a set via /select_quiz_set, the app loads that set into session["quiz_pool"], initializes the quiz index and score, and then /question handles the main quiz loop.

During the quiz, each POST to /question checks the answer against the correct one, updates the score, and stores any missed questions in session["wrong_questions"]. Once the user has gone through the entire pool, the app checks whether there are missed questions: if so, it replaces the quiz pool with only the wrong questions and continues quizzing; if not, it redirects to /result. The /result route calculates the total score and percentage, displays the summary, and finally clears the session. Structurally, this creates a clear separation of concerns:
- Routes manage HTTP requests and page transitions
- Helper functions handle file parsing and persistence
- Session data tracks quiz progress and performance

High-Level Architecture (Markdown Diagram)

+-------------------------+
|        Browser          |
| (HTML templates/forms)  |
+-----------+-------------+
            |
            v
+-------------------------+
|        Flask App        |
+-----------+-------------+
            |
   +--------+--------+
   |                 |
   v                 v
+--------+     +---------------------+
| Routes |     |  Helper Functions   |
| (/,    |     | - load_questions    |
| /upload, etc)| - save_questions    |
+--------+     +---------------------+
   |
   v
+------------------------------+
|  Session State (per user)    |
| - quiz_pool                  |
| - index                      |
| - score                      |
| - wrong_questions            |
+------------------------------+
   |
   v
+------------------------------+
|     flashcard_sets/ folder   |
| - *.txt (uploaded sets)      |
| - *.json (manual sets)       |
+------------------------------+
## Section 4: Project's Results
At the end of each quiz practice, the user can see the result of their scores. We created an html page to showcase the user's score based on the number of questions they answered correctly in addition to the percentage of the correct questions. In flask, we decided to automatically take the user to the next questions they did incorrectly until they answered all the questions correctly. Once they have accomplished that, flask will take them to the result page where they can see their results practice. 

## Section 5: Projects Evolution/Exploring 
Our project evolution involves three main stages: 
- Creating a console-based question-and-answer
- Working with flask to create a website
- Adding html and css for styling and interactiveness
  
First, we begin with the minimum viable product. For the MVP, we begin to do a console-based question-and-answer practice tool. Once, we completed that, we decided to add the practice tool in flask because we wanted to make it more interactive to our user. The goal of the flask is that we want to create a website public where people especially students go practice for their exams and quizzes. Having a website is also convienient for those who may not have python to work with. The initial website was very bland, we had no color and all the texts and images are on the top-left side. We ended by adding colors and images to make the website more appealing using html and css. 

## Section 6: Attribution
We would like to acknowledge that AI especially Copilot and chatGPT are an integral part of our learning process. We had so many errors and working with so many files, so Copilot helped us debug so many of our codes. 
HTML is something we touched upon in class, but Copilot really helped us structure our code with the styling and heading. Working with a lot of html helped us see how rendering works. 
Our website multiple times because we sometimes forgot to return an empty list, so Copilot suggested ways for us to fix our code. 

# OIM3640 Final Project-Q&A Practice Tool

## Overview

This project is a console-based question-and-answer practice tool written in Python for the OIM3640: Problem Solving & Software Design course (Fall 2025).

The goal is to help users test themselves on any subject-- we have added trivia questions for now by loading or entering custom questions and answers. The tool then runs interactive quizzes, tracks performance, and gives extra practice on questions the user gets wrong.

---

## Big Idea

As students, we often create our own study guides and question banks in Word, Notion, or Google Docs, but there is no simple way to **turn those into interactive quizzes** without manually building flashcards in another app.

This tool solves that problem by letting users:

- **Upload their own questions** from a simple text file  
- **Or type questions directly into the program**  
- Practice in an **interactive quiz format** in the terminal  
- See **instant feedback** and **scores**  
- Automatically re-practice missed questions more often  

### Minimum Viable Product (MVP)
- Load questions and answers from a text file or manual input  
- Randomize question order  
- Prompt the user for answers in the console  
- Show whether each answer is correct or incorrect  
- Display a final score at the end of the quiz  


### Stretch Features Implemented

- **80% rule**: If a quiz score is below 80%, the program offers another round of practice.
- **Adaptive weighting**: Questions missed more often are more likely to appear in the next round.
- **Persistence**: Quiz results (score, round number, etc.) are saved to a `quiz_results.json` file so users can see their past performance for each quiz name.

---

## How to Run the Project

### Prerequisites

- Python 3.x installed (we used Python 3.13)
- A terminal (Command Prompt, PowerShell, or VS Code terminal)

### Project Structure

```text
Flashcard-Tool-/
│
├── proposal.md
├── README.md
└── quiz_app/
    ├── quiz_app.py
    ├── questions.txt
    └── quiz_results.json   (created automatically after first run) --> you will be asked to label the time you are studying for so you can go back and track progress
