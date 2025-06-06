FROM public.ecr.aws/lambda/python:3.11

# Set the working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy AWS Lambda RIE into the container
ADD aws-lambda-rie /usr/local/bin/aws-lambda-rie

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Overwrite the file in robin_stocks with your custom one
COPY authentication.py /var/lang/lib/python3.11/site-packages/robin_stocks/robinhood/authentication.py

# Set the CMD to your handler
CMD [ "lambda_function.lambda_handler" ]
