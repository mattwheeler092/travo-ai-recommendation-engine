# Travo.ai Recommendation Engine

Travo.ai is an incredible travel planning app designed to make your trip planning experience seamless and personalized. By simply providing text prompts describing your desired activities, Travo.ai generates customized travel itineraries just for you!

With access to a vast database of over 120,000 activities from 130 cities worldwide, sourced directly from TripAdviser ([more details](https://github.com/mattwheeler092/tripadvisor-scraper)), Travo.ai ensures that you have access to the best recommendations for your travel adventures. You can visit our website ([here](https://eclectic-brioche-a372fe.netlify.app/)) for more information.

This GitHub repository encompasses all the code required to generate these personalized recommendations, as well as the deployment process of our recommendation API on AWS. Topics covered include:

- [Project Description](#project-description)
- [Recommender Architecture](#recommender-architecture)
- [Dev Installation](#dev-installation)
- [Deployment to AWS](#deployment-to-aws)


![](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/images/travo-ai-demo.gif)

## Project Description

## Recommender Architecture

## Dev Installation

If you want to use this code for your own use, in the repository root directory run the following commands to create and activate the python virtual environment to continue development:

   - `make setup`
   - `source env/bin/activate`

**NOTE:** If you need to include new packages for your recommendation engine, make sure to include them in the `requirements.txt` file

## Deployment to AWS

The following steps are intended to show how the recommendation API can be deployed onto an AWS EC2 instance. Once these steps are complete, you will be able to access the recommendation engine via the Python `requests` library, as detailed [here](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/tutorial.ipynb).

1. Create an AWS EC2 instance, with Amazon Linux POS, and save the corresponding `.pem` file. Ensure "read-only" permissions are applied to the `.pem` file by running the command: 
   - `chmod 400 path/to/file.pem`

2. Update the `EC2_INSTANCE_IP` and `PRIVATE_KEY_PATH` parameters in the `config.ini` file ([here](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/config.ini)) with the EC2 instance public IP-address and `.pem` filepath respectively.

3. SSH into you EC2 instance using your `.pem` file and EC2 Public IP-address using the command: 
   - `ssh -i path/to/file.pem ec2-user@$EC2_INSTANCE_IP`

4. Install git on your ec2 instance by running the following commands:
   - `sudo yum update -y`
   - `sudo yum install git`

5. Install docker on your ec2 instance by running the following commands:
   - `sudo yum install docker -y`
   - `sudo service docker start`
   - `sudo usermod -a -G docker ec2-user`

6. Disconnect and then re-SSH into your EC2 instance. Run `docker info` to validate docker has been installed.

7. Install docker-compose on your ec2 instance by running the following commands:
   - `sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
   - `sudo chmod +x /usr/local/bin/docker-compose`
   - Run `docker-compose --version` to validate installation

8. Navigate to the root of the repository, run the command: 
   - `make start-server`

Once these steps are commpleted, the recommendation API will be accessible via the endpoint: `http://EC2_PUBLIC_IP/recommendation/`. See the tutorial [notebook](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/tutorial.ipynb) for more details.

**NOTE:** When you are done with the recommendation API, run the command `make stop-server` to shut down the recommendation API server. Also make sure to shut down the EC2 instance to avoid excess billing!!

