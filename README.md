# Travo.ai Recommendation Engine

Travo.ai ([Website](https://eclectic-brioche-a372fe.netlify.app/)) is a travel planning app that generates personalised travel itineries based on user provided text prompts that describe what the user wants to do on their trip! The app has access to over 120,000 activities, across 130 cities, that have been scraped from TripAdviser (more information [here](https://github.com/mattwheeler092/tripadvisor-scraper)). 

This GitHub repo covers the code used to generate the personalised recommendations, as well as the deployment of the recommendation API to AWS. It will cover:

- [Project Description](#project-description)
- [Recommender Architecture](#recommender-architecture)
- [Dev Installation](#dev-installation)
- [Deployment to AWS](#deployment-to-aws)


![](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/images/travo-ai-demo.gif)

## Project Description

## Recommender Architecture

## Dev Installation

## Deployment to AWS

The following steps are intended to show how the recommendation API can be deployed onto an AWS EC2 instance. Once these steps are complete, you will be able to access the recommendation engine via the Python `requests` library, as detailed [here](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/tutorial.ipynb).

1. Create an AWS EC2 instance and save the corresponding `.pem` file. 
   **NOTE:** Ensure "read-only" permissions are applied to the `.pem` file using the command:
   `chmod 400 path/to/file.pem`

2. Install git and docker on your ec2 instance by running the following commands:
   - `sudo apt-get update`
   - `sudo apt-get install docker.io`
   - `sudo usermod -aG docker ubuntu`




# How to
🚨 When you add anything to `server.py` make sure to update the dependencies in `requirement.txt` and `Dockerfile` in order to build the image successfully.
## Build the image

Run this command: `docker image build -t dev-server-image .`

## Run the image

Run this command: `docker run -d --env-file .env -p 80:80 dev-server-image`
This should spin up the FastAPI server on `localhost:80`

The `.env` should contain the following keys:

- PINECONE_API_KEY
- PINECONE_ENV
- PINECONE_INDEX
- OPENAI_API_KEY



# EC2 Instance Setup

Platform: Ubuntu
Instance type: t2.micro

1. ssh into the EC2 instance with a `.pem` key file
   1. `chmod 400 travo-dev.pem`
   2. `ssh -i "travo-dev.pem" ubuntu@ec2-54-219-130-238.us-west-1.compute.amazonaws.com`
2. `sudo apt-get update`
3. `sudo apt-get install docker.io`
4. `sudo usermod -aG docker ubuntu` so that you don't need to run `sudo docker...` for every Docker command 
5. Clone the repo to get all the files for building the Docker image `git clone https://jhnyc:<ACCESS_TOKEN>@github.com/jhnyc/travo.git`
6. Build & run the docker image
7. Call API endpoint at `http://ec2-54-219-130-238.us-west-1.compute.amazonaws.com`