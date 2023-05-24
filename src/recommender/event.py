import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from typing import List, Dict, Any

from config import (
    SIMILARITY_IMPORTANCE,
    REVIEW_RATING_IMPORTANCE,
    DISTANCE_IMPORTANCE
)

class Event:
    """
    A class representing an event in the itinerary.

    Attributes:
        id (int): An integer representing the ID of the event.
        duration (int): An integer representing the duration 
            of the event in hours.
        coord (List[float]): A list of floats representing 
            the coordinates of the event.
        similarity_score (float): A float representing the 
            similarity score for the event.
        review_rating_score (float): A float representing the 
            review rating score for the event.
        distance_score (float): A float representing the 
            distance score for the event.

    Methods:
        __init__(self, event: dict, similarity: float, review_rating: float) -> None:
            Initializes a new Event object.
        update_distance_score(self, coord: List[float]) -> None:
            Updates the distance score for the event.
        __repr__(self) -> str:
            Returns a string representation of the event.
        score(self) -> float:
            Calculates the overall score for the event.
    """


    def __init__(self, 
            event: Dict[str, Any], similarity: float, review_rating: float):
        """ Initializes a new Event object.
        Args:
            event (dict): A dictionary containing metadata for 
                the event.
            similarity (float): A float representing the similarity 
                score for the event.
            review_rating (float): A float representing the review 
                rating score for the event.
        """
        self.id = event["metadata"]["id"]
        self.tripadvisor_id = str(event["metadata"]["tripadvisor_id"])
        self.duration = event["metadata"]["activity_duration"]
        self.coord = [
            event["metadata"]["latitude"], 
            event["metadata"]["longitude"]
        ]
        self.similarity_score = similarity
        self.review_rating_score = review_rating
        self.distance_score = 0

    
    def compute_distance(self, coord: List[float]) -> None:
        """ Updates the distance score for the event.
        Args:
            coord (List[float]): A list of floats representing 
                the coordinates of the event.
        """
        return math.dist(self.coord, coord)
    

    def __repr__(self) -> str:
        """ Returns a string representation of the event.
        Returns:
            str: A string representation of the event.
        """
        sim = round(self.similarity_score, 3)
        rev = round(self.review_rating_score, 3)
        dist = round(self.distance_score, 3)
        sc = round(self.score, 3)
        event_id = self.id
        return f"Event({sc=}, {sim=}, {rev=}, {dist=}, {event_id=})"
    

    @property
    def score(self) -> float:
        """ Calculates the overall score for the event. 
            Takes into account the event similarity, rating / review, 
            and distance to other events in queue
        Returns:
            float: The overall score for the event.
        """
        return (
            SIMILARITY_IMPORTANCE * self.similarity_score +
            REVIEW_RATING_IMPORTANCE * self.review_rating_score +
            DISTANCE_IMPORTANCE * self.distance_score
        )