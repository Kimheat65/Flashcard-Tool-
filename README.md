# Flashcard Tool 
This is a software design project that mimics flashcards practice used to help with students' review session for exams, quizzes, and assignments. 

Team Members: Kimheat Chheav and Saba Ali

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