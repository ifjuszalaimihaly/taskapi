# 🗂️ Task Manager API (Django REST)

This project is a simple task management backend API built with Django and Django REST Framework.  
It supports task creation, retrieval, update, deletion, filtering, sorting, and smart AI-based suggestions.

---

## 🚀 Features

- Full CRUD API for task management
- Filter tasks by status or due date
- Sort tasks by creation or due date (asc/desc)
- Smart task suggestion endpoint using LLM (optional)
- Pydantic schema compatibility (for FastAPI or AI use)

---

## 🤖 OpenAI API Key (for Smart Suggestions)

This project uses OpenAI's GPT API to generate smart task suggestions based on your existing to-do list.

To use this feature, you'll need an OpenAI API key. You can get one here (minimal cost applies):

🔗 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

Once you have your key (it starts with `sk-`), create a `.env` file in the project root and add the following line:

OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX

> ⚠️ Do **not** share this key publicly or commit it to version control.

You can then access the smart suggestion endpoint at:


## 🛠️ How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Navigate into the Django project
cd taskproject

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver


## The site in running

Base URL: http://127.0.0.1:8000/taks

Enpoint list:

- `/` – API Overview
- `/all/` – View All
- `/create/` – Add
- `/update/pk` – Update
- `/pk/delete` – Delete
- `/smart_task_suggestions/` – Smart Task Suggestions
