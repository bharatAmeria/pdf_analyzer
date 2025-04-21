FROM public.ecr.aws/lambda/python:3.11

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY app/ ./app

# Set the CMD to your handler
CMD ["app.main.lambda_handler"]
