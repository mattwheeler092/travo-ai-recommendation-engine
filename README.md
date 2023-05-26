# Travo.ai Recommendation Engine

Travo.ai is an incredible travel planning app designed to make your trip planning experience seamless and personalized. By simply providing text prompts describing your desired activities, Travo.ai generates customized travel itineraries just for you!

With access to a vast database of over 120,000 activities from 130 cities worldwide, sourced directly from TripAdviser ([more details](https://github.com/mattwheeler092/tripadvisor-scraper)), Travo.ai ensures that you have access to the best recommendations for your travel adventures. You can visit our  [website](https://eclectic-brioche-a372fe.netlify.app/) to try it out for yourself!

This GitHub repository encompasses all the code required to generate these personalized recommendations, as well as the deployment process of our recommendation API on AWS. Topics covered include:

- [Project Description](#project-description)
- [Recommender Architecture](#recommender-architecture)
- [Deployment to AWS](#deployment-to-aws)
- [Dev Installation](#dev-installation)


![](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/images/travo-ai-demo.gif)

## Project Description

Travo.ai is a personalized trip planning app that generates customized itineraries based on user-provided descriptions of their desired activities. At the core of this application is a robust recommendation engine that matches user preferences with a database of TripAdvisor activities to generate relevant trip suggestions.

To build the recommendation engine, we leveraged the OpenAI embedding API to obtain vector representations of user text prompts and predefined preferences. Using these vectors, we queried a Pinecone database containing activities [scraped from TripAdvisor](https://github.com/mattwheeler092/tripadvisor-scraper). The query results were then ranked based on both similarity to the user's embedded vector and popularity. Finally, a clustering algorithm was applied to group the activities into different days of the trip.

This innovative approach successfully delivers recommendations closely aligned with the user's input, ensuring a tailored travel experience. The **Recommender Architecture** section runs through the specifics of how we generated each recommendation.


## Recommender Architecture

![](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/images/recommender-architecture-diagram.png)

## Deployment to AWS

Follow these steps to deploy the recommendation API onto an AWS EC2 instance. Once completed, you will be able to access the recommendation engine using the Python requests library as explained [here](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/tutorial.ipynb).

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

After completing these steps, the AWS EC2 instance is ready to host the recommendation API. You do not need to repeat these steps. The repository's Makefile provides convenient commands for starting and stopping the recommendation API server on your instance. The available commands are:

   - `make start-server`: Pulls the latest repo changes from Github and starts the FastAPI app
   - `make stop-server`: Shuts down the FastAPI app (remember to also such down the EC2 instance!)

**NOTE:** The first time you run `make start-server`, the repository will be cloned onto the EC2 instance; re-running the commands will pull any changes to the repo. Once the FastAPI app is running, you can access the recommendation API at the endpoint: http://EC2_PUBLIC_IP/recommendation/. For more details, refer to the tutorial [notebook](https://github.com/mattwheeler092/travo-ai-recommendation-engine/blob/main/tutorial.ipynb)


## Dev Installation

If you want to use this code for your own use, follow these steps in the repository root directory to create and activate the Python virtual environment for further development:

1. Run the following command to set up the virtual environment. You only need to run this once:
   - `make setup`

2. Activate the virtual environment by running the command:
   - `source env/bin/activate`

**NOTE:** If you need to include new packages for your recommendation engine, make sure to include them in the `requirements.txt` file
