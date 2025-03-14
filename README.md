# PwC Exercise

## Overview
I'm Luciano Ganzero, and this is my implementation of the **Technical Challenge: Backend Developer** for PwC.

This project was built using **FastAPI** for the backend, as required, and **SQLite** as the database to keep the development environment lightweight and minimal.

## Technologies Used
- FastAPI – A modern, high-performance web framework for building APIs with Python 3.
- SQLite – A lightweight and self-contained relational database.
- SQLAlchemy – ORM for database interactions.
- Alembic – Database migrations tool.
- Uvicorn – ASGI server for running the FastAPI application.
- Poetry – Dependency management and packaging.
- Docker – Containerized deployment.  

## Setup Instructions
### Prerequisites
Ensure you have the following installed:

- Python 3.10+
- git
- Docker & Docker Compose (for containerized execution)
- Poetry (for dependency management)

### Local Installation
1. **Clone the repository**  
    ```bash
    git clone git@github.com:LucianoGanzero/PwCExercise.git
    ```
2. **Navigate to repository**  
    ```bash
    cd pwcexercise
    ```
3. **Install dependencies**  
    ```bash
    poetry install
    ```
4. **Run the application**  
    ```bash
    poetry run uvicorn app:app --reload
    ```
5. **Optional - You can seed the database**  
    ```bash
    poetry run seed-db
    ```

### Running whit Docker
The application is dockerized for an easy an uniform use
1. **Build and start the containers**  
    ```bash
    docker compose up --build (optional --watch for following)
    ```
    

### Access the API at
    http://localhost:8000

### API Documentation
Once the application is running, you can explore the API documentation at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
I've also uploaded the .json at **swaggerhub** just in case. The public link is https://app.swaggerhub.com/apis/LucianoGanzero/exercise-for_pw_c/1.0.0


### DATABASE Documentation
Database diagram can be accesed at:
- **SVG Link:** https://www.mermaidchart.com/raw/81b5a38e-0357-4842-a30b-b863c98c67f3?theme=light&version=v0.1&format=svg
- **Editor Link:** https://www.mermaidchart.com/app/projects/8b7904e6-9f40-4317-baa4-93465a81b0b6/diagrams/81b5a38e-0357-4842-a30b-b863c98c67f3/version/v0.1/edit

### Integration 
- **Editor Link:** https://www.mermaidchart.com/app/projects/8b7904e6-9f40-4317-baa4-93465a81b0b6/diagrams/e95fb27f-7647-4ff5-b932-763ff20a2b63/version/v0.1/edit
- **SVG Link:** https://www.mermaidchart.com/raw/e95fb27f-7647-4ff5-b932-763ff20a2b63?theme=light&version=v0.1&format=svg

I've placed both diagrams in the 'diagrams' directory in case the links stop working.

### Dataset
The dataset used in this project is located at the root of the project under the name **HR_Analytics.csv**, as requested. It is a public dataset sourced from Kaggle. The link is https://www.kaggle.com/datasets/anshika2301/hr-analytics-dataset

## Requirements

The application is a small simulation of some personnel management at some bussiness. It has five tables (employees, departments, job_titles, salaries and performance_reviews) that are related through the employees, so all the information is, in some way, information about the employees.  
Departments and job_titles are kind of independent, in the way that both *contain* employees and exist beyond them, but the things you can say about them are, in fact, things about the employees they contain.  
In addition to implementing CRUD operations for all tables, I have added extra routes to simulate potential client requirements. These include:
- Retrieve the active or current salary for a employee
- Retrieve the last performance review for a employee
- Calculate the aguinaldo for a employee
- Calculate the amount of hours worked in a month for a employee
- Retrieve all the employees in a department
- Calculate the average salary for a department
- Calculate the average score for the performance reviews of all the employees in a deparment
- Calculate the average of all the salaries in the history of the bussiness
- Calculate the average of the current salaries
- Retrieve all the employees that have the same job title
- Calculate the average salary for all the employees that have the same job title
- Calculate the average score for all the performance reviews of the employees with the same job title