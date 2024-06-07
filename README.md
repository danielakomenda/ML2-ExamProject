## Create Python-Environment
- CTRL+Shift+p -> Create Environment
- Choose .venv
- Choose Python 3.12.1 (or similar)
- Install Libraries: pip install requirements.txt


## Run Backend-Server
- Go to directory: cd backend
- Start backend-server: litestar run
- Start backend-server in debug-mode: litestar run -rd


## Run Frontend
- Go to directory: cd frontend
- Install dependencies: npm install
- Start frontend: npm run dev


## Get Access to DB nd API
- Create a File with the name .env with the following:
    - MONGODB_URI=<your own mongodb-uri> <-- if you don't have one, you can create one for free
    - OPENAI_APIKEY=<openai-api-key> <-- if you don't have one, contact me


## Create Dummy-Data
- Kernel: Python 3.11 or higher
- Run Jupyter Notebook "Dummy-Data-Input"
- Check your MongoDB, if you can find 3 collections and Data in each collection


# Front-End-Explanation

## Home
Here you find the project-goal and motivation behind the project

## Beurteilen
Here you can choose a student and a semester.
You create an assessment for the student by different criteria.
If you want, you can write down some notes as well.
Per student and semester you can create several assessments.
This is important, so many different teachers can assess the student individually.
All the assessment are stored in a seperate collection in the Database.

## Zusammenführen
Here you can choose a student and a semester.
You can see all the assessment that have been done for a given student and semester.
You can decide how you would like to create the final assessment.
The notes of the different teachers are combined to a note-suggestion, but you are free to create another note-entry.
If you write your own note the Cosine-Similarity will be calculated between the openAI-recommended-note and your own one.
The final-assessment will be stored with the rest of the semester-data to the Database

## Finaler Text
Here you can choose a student and all the semesters with a final assessment.
You can see an overview of the final assessment.
You have the possibility to correct something, if you are not yet happy.
If the final-assessment is ok, you can create a text.
The text is created with the openai-API.
I used prompt engineering with a few shot dataset.
All entries are anonymized, so there will be no name sent to openai.
The text will be displayed in the frontend with the name.
If you are not yet happy with the text, you can write your own prompt to give openai specific information, how you would like to change the text. (TODO)
You can also write your own text.
If you write your own text the Cosine-Similarity will be calculated between the openAI-recommended-text and your own one.
If you are happy with the text, it will be stored in the Database with the rest of the semester-data.



## Student
If you'd like to create your own student, you can use '/base-data'-URL.

## Semester
If you'd like to create your own semester, you can use '/semester-data'-URL.