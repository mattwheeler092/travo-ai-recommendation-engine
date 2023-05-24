from fastapi import FastAPI
from utils import rate_limit, RecommendationRequest
from fastapi.middleware.cors import CORSMiddleware
from recommender.recommender import generate_api_response

# Initial server application
app = FastAPI()

# Add middleware to enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello_world():
    """ Root endpoint that returns a greeting message. """
    return {
        "message": "hello world"
    }

@app.post("/recommendation/")
@rate_limit(100)
async def process_data(request_data: RecommendationRequest):
    """ Endpoint for processing recommendation data.
    Parameters:
        request_data: RecommendationRequest - The validated request data 
            containing destination, namespace, num_days, user_query, 
            and user_preferences.
    Returns:
        API response generated based on the request data.
    """
    return generate_api_response(
        request_data.destination,
        request_data.namespace,
        request_data.num_days,
        request_data.user_query,
        request_data.user_preferences
    )
