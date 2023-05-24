import scipy
import math
import sys
import random
import numpy as np

from .event import Event
from typing import List, Dict, Callable
from itertools import permutations
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import (
    MAX_REVIEW_COUNT,
    AVG_RATING,
    TITLE_TEMPLATES,
    RESPONSE_FIELDS
)


def get_review_rating_scores(events: List[Event]) -> np.ndarray:
    """ Calculates review rating scores for a list of events.
    Args:
        events (List[dict]): A list of dictionaries containing 
            metadata for the events.
    Returns:
        np.ndarray: An array of floats representing the review 
            rating scores for the events.
    """
    scores = []
    for event in events:
        scores.append(
            process_rating_score(event['metadata']['rating']) *
            min(event['metadata']['review_count'], MAX_REVIEW_COUNT)
        )
    return np.array(scores) / np.max(np.abs(scores))


def process_rating_score(rating):
    """ """
    if rating <= AVG_RATING:
        return (rating - AVG_RATING) / AVG_RATING
    else:
        return (rating - AVG_RATING) / (5 - AVG_RATING)


def get_similarity_scores(
        events: List[Event], embedding: List[float]) -> np.ndarray:
    """ Calculates similarity scores for a list of events 
        and an embedding.
    Args:
        events (List[dict]): A list of dictionaries containing 
            metadata for the events.
        embedding (List[float]): A list of floats representing 
            the embedding for the events.
    Returns:
        np.ndarray: An array of floats representing the similarity 
            scores for the events.
    """
    scores = []
    for event in events:
        scores.append(np.dot(event["values"], embedding))
    return scale_data(scores)


def get_distance_scores(
        events: List[Event], coord: List[float]) -> np.ndarray:
    """ Calculates distance scores for a list of events 
        and an embedding.
    Args:
        events (List[dict]): A list of dictionaries containing 
            metadata for the events.
        coord (List[float]): A list of floats representing 
            the lat / lng coordinates of the cluster centroid.
    Returns:
        np.ndarray: An array of floats representing the similarity 
            scores for the events.
    """
    distances = [event.compute_distance(coord) for event in events]
    return -1 * scale_data(distances)
    

def scale_data(data: List[float]) -> np.ndarray:
    """ Scale the input data to the range [-1, 1].
    Args:
        data (List[float]): The data to be scaled.
    Returns:
        np.ndarray: The scaled data as a numpy array.
    """
    scaled = (
        (np.array(data) - np.min(data)) / 
        (np.max(data) - np.min(data))
    )
    return 2 * scaled - 1


def denormalise_data(data: List[float]) -> np.ndarray:
    """ Function to convert data that is normally distributed to 
        data that is roughly uniformly distributed.
    Args:
        data (List[float]): A list of floats to denormalize.
    Returns:
        np.ndarray: An array of floats representing the denormalized data.
    """
    return scipy.stats.norm.cdf(
        data, loc=np.mean(data), scale=np.std(data)
    )


def generate_coord_check_func(
        events: List[Event]) -> Callable[[List[float]], bool]:
    """ Generates a function to check if a coordinate is valid. 
        Function returns true if both the lat / lng are within 
        5 std of the mean lat / lng.
    Args:
        events (List[dict]): A list of dictionaries containing 
        metadata for the events.
    Returns:
        Callable[[List[float]], bool]: A function that takes a 
            list of floats representing a coordinate and returns 
            True if the coordinate is valid, False otherwise.
    """
    lat_vals = [event["metadata"]["latitude"] for event in events]
    lat_mean, lat_std = np.mean(lat_vals), np.std(lat_vals)

    lng_vals = [event["metadata"]["longitude"] for event in events]
    lng_mean, lng_std = np.mean(lng_vals), np.std(lng_vals)

    def coord_check(coord):
        lat, lng = coord
        return (
            (lat_mean - 5 * lat_std < lat < lat_mean + 5 * lat_std) and
            (lng_mean - 5 * lng_std < lng < lng_mean + 5 * lng_std) 
        )
    return coord_check


def optimise_order(events: List[Event]) -> List:
    """ Optimizes the order of events for a day's itinerary.
    Args:
        events (List): A list of Event objects representing 
            the events for the day's itinerary.
    Returns:
        List: A list of Event objects representing the optimized 
            order of events for the day's itinerary.
    """
    if len(events) < 3:
        return events
    min_order, min_dist = None, float("inf")

    for event_order in permutations(events):
        dist = compute_order_distance(event_order)
        if dist < min_dist:
            min_dist = dist
            min_order = event_order

    return min_order 


def compute_order_distance(events: List) -> float:
    """ Computes the total distance for a given 
        order of events.
    Args:
        events (List): A list of Event objects representing 
            the events to visit.
    Returns:
        float: The total distance for the given order of events.
    """
    distance = 0
    for idx in range(len(events) - 1):
        distance += math.dist(
            events[idx].coord, events[idx + 1].coord
    )
    return distance


def generate_title(destination: str, num_days: int) -> str:
    """ Generate a random title for a trip to the given 
        destination for the given number of days.
    Args:
        destination (str): The name of the destination.
        num_days (int): The number of days of the trip.
    Returns:
        str: The generated title string.
    """
    title = random.choice(TITLE_TEMPLATES)
    title = title.replace("[DESTINATION]", destination) \
                  .replace("[NUM_OF_DAYS]", str(num_days))
    return title


def format_event(metadata: Dict) -> Dict:
    """ Convert the metadata fields of an event to a 
        new dictionary format.
    Args:
        metadata (Dict): The metadata of an event in the original format.
    Returns:
        Dict: The metadata of the event in the new format.
    """
    return {
        new: metadata[old] for new, old in RESPONSE_FIELDS.items()
    }
