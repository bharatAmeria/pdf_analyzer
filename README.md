# Resume Analyzer

The **Resume Analyzer** is a Streamlit-based web application designed to analyze resumes in PDF or DOCX format. It extracts text from uploaded resumes and uses the Groq API to provide a structured analysis based on user-selected criteria such as designation, experience level, and domain. The app offers features like text extraction, resume scoring, logging, caching, and the ability to download the analysis.

## Technologies Used
- **Python**: Core programming language for the application.
- **Streamlit**: Framework for building the interactive web interface.
- **Groq API**: AI-powered text analysis for resume evaluation.
- **PyMuPDF (fitz)**: Library for extracting text from PDF files.
- **python-docx**: Library for extracting text from DOCX files.
- **python-dotenv**: For managing environment variables (e.g., API keys).
- **Git**: Version control for tracking project changes.
- **Logging**: Custom logging system for debugging and monitoring.

---

## Project Setup Steps

### STEP 1: Project Setup and Initial Git Repository
**GOAL**: Set up the project structure and initialize a Git repository.

#### **Project Setup and Initial Git Repository**
1. **Create the Project Directory and Clone the Empty Repo**
   ```bash
   git clone "URL" 
2. **Navigate to the Project Directory**
    ```bash
   cd resume_analyzer
   ```
3. **Open Project in VS Code**
    ```bash
   code .
   ```

#### **Create the Directory Structure**
- This structure separates app logic (main), reusable libraries (lib), utilities (utils), and data files (data).
``` bash
python template.py
```

#### **Add a README**
- Create this README.md file with initial content:
``` bash
# Resume Analyzer
A Streamlit app to analyze resumes using the Groq API.
```

#### **Initialize Git**
``` bash 
git add README.md
git status
git commit -m "Initial commit: Project setup with README"
git push origin main
```

### STEP 2: Set Up Dependencies
**GOAL**: Install required packages and configure the environment.

#### **Edit requirements.txt**
``` bash
streamlit
groq
pymupdf
python-docx
python-dotenv
```

#### **Install Dependencies**
``` bash
pip install -r requirements.txt
```

#### **Set Up .env for the Groq API Key**
- Visit Groq Console: https://console.groq.com/keys , sign up/login, and generate an API key.
- Add it to .env:
``` bash
GROQ_API_KEY=your_key_here
``` 

- Add .env to .gitignore to keep secrets safe.

#### **Now our main forcus is on serverless deployment using lambda-function**

### STEP 2: Create Dockerfile add 

```  bash
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]

```
- The above configuration specifically to build and test docker image locally. If it is working properly.

```  bash
FROM public.ecr.aws/lambda/python:3.11

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . ./

# Set the CMD to your handler
CMD ["app.main.lambda_handler"]
```

- public.ecr.aws/lambda/python:3.11 -> This python image lambda function specific only.
- app.main.lambda_handler -> This command looks for and invokes when the service triggers your Lambda function.



## Running the Application
1. Ensure all dependencies are installed: ```pip install -r requirements.txt```
2. Set up your ```.env``` file with the Groq API key.
3. Run the app: ```streamlit run main/app.py```
4. Open your browser to ```localhost:8501``` to use the app.