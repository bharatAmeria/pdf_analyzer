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

### STEP 3: Create Dockerfile

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
- To build loaclly launch your Docker desktop.
- In terminal give command 
``` bash

docker build -t streamlit-test . 
docker run --env-file .env -p 8501:8501 streamlit-test
```

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
- The code for lambda_handler in lambda_handler.py  

### STEP 4: AWS IAM user

- Log in to the AWS Management Console.
- Go to IAM (search for IAM in the Services menu). In the left sidebar, click Users.
- Click the "Add users" button.
- Enter a username.
- Select Access type:
   ✅ Programmatic access -> if you want access via CLI, SDK, etc.
   ✅ AWS Management Console access -> if the user needs to sign in to the AWS console.
- Set Console password (auto-generated or custom).Click Next: Permissions.
- Choose how to assign permissions:
- Attach existing policies directly (e.g., AdministratorAccess, AmazonS3FullAccess, etc.). Give AdministratorAccess if you are new user.
- Or add to a group with pre-defined policies (Optional) Add tags (key-value pairs).
- Click Next: Review. Click Create user.

Note .:- ✅ After Creation
- Download Save the Access Key ID and Secret Access Key (if programmatic access was selected).

### STEP 5: ECR (Elastic Contioner Registry). Docker for AWS

- Navigate to Elastic Container Registry (ECR) (search for it in Services).
- In the left sidebar, click Repositories.
- Click "Create repository".
- Choose Private or Public (usually Private).
- Enter a repository name. (Optional) Configure settings:
- Enable tag immutability, image scanning, or encryption as needed.
- Click Create repository.

✅ Authenticate Docker with ECR (using AWS CLI)
- Make sure AWS CLI and Docker are installed.If not
  1. Install AWS CLI (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
  2. open terminal paste command.
  ```bash  
  aws configure
  ```
  3. Give Access Key ID and Secret Access Key. All other parameter as default.

- Run this to authenticate Docker with ECR: 
  ```bash
  aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<your-region>.amazonaws.com
  ```

  Note .:- Replace: 
           <your-region> → e.g.(us-east-1)
           <account-id> → your AWS account ID

- Tag and Push Docker Image to ECR
   - Build your Docker image (if not done already):
      ```bash
      docker build -t your-image-name .
      ```
   - Tag the image with your ECR repo URI:
      ```bash
      docker tag your-image-name:latest <account-id>.dkr.ecr.<region>.amazonaws.com/your-repo-name
      ```
   - Push the image to ECR:
      ```bash
      docker push <account-id>.dkr.ecr.<region>.amazonaws.com/your-repo-name
      ```

### STEP 6: AWS Lambda.

- Go to AWS Lambda service.
- Click Create function.
- Choose: Container image
- Give Function name.
- Container image URI (paste your ECR image URI)
- Set Execution Role (you can let AWS create one or use existing)
- Click Create function

Or other way is using AWS CLI.

```bash
aws lambda create-function \
  --function-name my-lambda-container-func \
  --package-type Image \
  --code ImageUri=<your-ecr-image-uri> \
  --role arn:aws:iam::<account-id>:role/<your-lambda-execution-role>
```

Note .:- Replace: <your-ecr-image-uri> = your ECR image URI
                  <account-id> = your AWS Account ID 
                  <your-lambda-execution-role> = IAM role with Lambda permissions (like AWSLambdaBasicExecutionRole)

#### ✅ Test Your Lambda
- Go to Lambda Console → your function → Test.
- Configure a test event → click Test.
- View logs/output in CloudWatch Logs.

#### Update Lambda with new image:
If you push a new version of the image to ECR:
```bash
aws lambda update-function-code \
  --function-name my-lambda-container-func \
  --image-uri <your-updated-ecr-image-uri>
```

### STEP 7: AWS API Gateway.

1. Go to AWS Console > API Gateway
   - In the AWS Console, search for and open API Gateway.
   - Choose “HTTP API” (simpler and faster than REST API).
   - Click Create API.

2. Create a New HTTP API
   - Choose "Build" under HTTP API.
   - Under Integrations, click Add integration → choose Lambda function.
   - Select your Lambda function from the list.
   - Click Next.

3. Configure Routes
   - Define a route:
   - Method: ANY or specific (GET, POST, etc.)
   - Resource path: / or /your-path
   - Click Next.

4. Deploy the API
   - Create a new Stage (e.g., prod).
   - Click Next and then Create.

## Running the Application
1. Ensure all dependencies are installed: ```pip install -r requirements.txt```
2. Set up your ```.env``` file with the Groq API key.
3. Run the app: ```streamlit run main/app.py```
4. Open your browser to ```localhost:8501``` to use the app.