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

# Comment out lines 85 and 86 in the specified file
RUN sed -i.bak '85s/^/# /; 86s/^/# /' /var/lang/lib/python3.11/site-packages/robin_stocks/robinhood/authentication.py

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]