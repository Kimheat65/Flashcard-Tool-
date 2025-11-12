The Big Idea: What is the main idea of your project? What topics will you explore and what will you accomplish? Describe your minimum viable product (MVP) and your stretch goal.        
Learning Objectives: Since this is a team project, you may want to articulate both shared and individual learning goals.
Implementation Plan: This part may be somewhat ambiguous initially. You might have identified a library or a framework that you believe would be helpful for your project at this early stage. If you're uncertain about executing your project plan, provide a rough plan describing how you'll investigate this information further.
Project Schedule: You have roughly 4-5 weeks to complete the project. Create a general timeline. Depending on your project, this could be a detailed schedule or just an overview. As the project progresses, you’ll likely need to revise this schedule.
Collaboration Plan: How will you collaborate with your teammates on this project? Will you divide tasks and then incorporate them separately? Will you undertake a comprehensive pair program? Explain how you'll ensure effective team collaboration. This may also entail information on any software development methodologies you anticipate using (e.g. agile development). Be sure to clarify why you've picked this specific organizational structure.
Risks and Limitations: What do you think is the biggest risk to the success of your project?
Additional Course Content: Are there any course topics or content you think would be helpful for your project?

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Answers to the Questions: 

The Big Idea:
Our project aims to develop an interactive question-and-answer practice tool that helps users test their knowledge on any topic by uploading or inputting their own questions and answers. The program will be built entirely in Python and run through a console-based interface. Users will either type their questions and answers directly into the program or upload a text document, which the system will parse using text analysis techniques to separate questions and answers automatically. Once the questions are loaded, the program will randomize the order and present them one at a time in the terminal. The user will type their answer, and the program will immediately display whether the answer was correct or incorrect. After all questions are completed, the program will generate a final score and feedback summary. If the user scores below 80%, the tool will automatically start another round of practice, prioritizing the questions answered incorrectly. This will be done by increasing the probability that missed questions reappear during the next randomized run.
- MVP (Minimum Viable Product): A functional command-line Python program that can import questions,     randomize them, prompt the user for answers, display results, and calculate a final score.
- Strech Goal: Implement adaptive question weighting (missed questions appear more often), detailed performance summaries after each session, and the ability to save results between runs for future study tracking.

Learning Goals: 
- Shared Team Goals:
      - Gain experience developing a Python-based console application from design to testing.
      - Learn to work with file input/output and text parsing using Python’s built-in libraries.
      - Understand how to design logical flow and user interaction through a text-based interface.
      - Practice collaborative coding using GitHub for version control.
- Individual Goals:
      - Saba's Goal: Focus on parsing text documents and separating questions/answers using Python string and regular expression methods.
      - Kimheat's Goal: Develop the question randomization, scoring, and feedback logic and implement performance tracking and question weighting.

Implementation Plan: 
We will use Python 3 as the main programming language. The project will rely primarily on standard libraries, including:
- random for question shuffling and adaptive weighting.
- re for pattern matching and text extraction from uploaded files.
- json for saving user progress or tracking previous attempts.

The console interface will display questions one at a time, accept user input, provide immediate feedback, and calculate the final score once all questions are completed. If time permits, we will enhance the feedback system to highlight areas of weakness and suggest targeted review. If any implementation challenges arise (e.g., parsing complex text structures or calculating adaptive weights), the team will explore documentation, Python forums, and open-source examples of quiz applications for guidance.

Project Schedule: showing weeks and goals per week
Week 1: Nov 6-Nov 10
- Milestone/ Goals: Finalize project proposal, assign team roles, and set up GitHub repository.

Week 2: Nov 11-Nov 17
- Milestone/Goals: Implement text input and parsing functionality. Test reading from both user input and files.

Week 3: Nov 18-Nov 24
- Milestone/ Goal: Build question randomization and response checking system. Test full question–answer flow in console.

Week 4: Nov 25-Dec 1
- Milestone/Goal: Add scoring logic, adaptive practice (weighted randomization), and result summaries.

Week 5: Dec 2- Dec 3
- Milestone/ Goal: Conduct full testing, debug any issues, finalize documentation, and prepare demo.
  
