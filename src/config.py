import os

# Relevant importances of each ranking feature
SIMILARITY_IMPORTANCE = 1       # Similarity to user text prompt
REVIEW_RATING_IMPORTANCE = 0.5  # Event popularity (num review / avg rating)
DISTANCE_IMPORTANCE = 0.2       # How close event is to other other events

MAX_DURARTION = 250     # Max duration of recommended events in a day (mins)
MAX_EVENTS = 5          # Max number of recommended events in a day

MAX_REVIEW_COUNT = 500  # Max cap review count (prevents skew from outliers)
AVG_RATING = 4          # Rating at which event is considered "good"

# Pinecone information / API key
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
PINECONE_TOP_K = 1000

# OpenAI model information / API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"

# Fields to return in recommender API response
RESPONSE_FIELDS = {
    'title': 'name',
    'location': 'address',
    'city': 'city',
    'link': 'website',
    'description': "description",
    'activity_length': "activity_duration",
    'image_url': 'image_url',
    'type': "type"}

# Templates for title of itinerary
TITLE_TEMPLATES = [
    "Discovering [DESTINATION] in [NUM_OF_DAYS] days",
    "[NUM_OF_DAYS]-day adventure in [DESTINATION]",
    "Exploring [DESTINATION] in [NUM_OF_DAYS] days",
    "[NUM_OF_DAYS]-day getaway to [DESTINATION]",
    "Experiencing the culture of [DESTINATION] in [NUM_OF_DAYS] days",
    "[NUM_OF_DAYS]-day journey to [DESTINATION]",
    "[DESTINATION] in [NUM_OF_DAYS] days: A traveler's guide",
    "[NUM_OF_DAYS]-day escape to [DESTINATION]",
    "[DESTINATION] in [NUM_OF_DAYS] days: A cultural immersion",
    "[NUM_OF_DAYS]-day trip to [DESTINATION]: Discovering the hidden gems"
]