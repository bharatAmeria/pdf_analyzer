# FROM public.ecr.aws/lambda/python:3.11

# WORKDIR /app

# # Copy requirements and install
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Copy source code
# COPY . ./

# # Set the CMD to your handler
# CMD ["app.main.lambda_handler"]


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]

