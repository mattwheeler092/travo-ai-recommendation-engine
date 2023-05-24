
import numpy as np

from .event import Event
from .event_queue import EventQueue

from typing import List, Dict, Any
from sklearn.cluster import KMeans

from .utils import (
    get_review_rating_scores,
    get_similarity_scores,
    generate_coord_check_func,
    denormalise_data,
    optimise_order,
    format_event
)

class Itinerary:
    """ A class for generating travel itineraries based on a list 
        of events and a provided user prompt embedding.

    Attributes:
        events (numpy.ndarray): An array of Event objects representing 
            the events in the itinerary.
        metadata (Dict[int, Dict[str, Any]]): A dictionary containing 
            metadata for each event,indexed by their ID.
        queues (List[EventQueue]): A list of EventQueue objects representing 
            the queues for each day in the itinerary.

    Methods:
        __init__(self, events: List[Event], embedding: List[float]) -> None:
            Initializes a new Itinerary object.
        generate_itinerary(self, num_days: int) -> Dict[str, List[Dict[str, Any]]]:
            Generates a travel itinerary for the specified number of days.
        generate_event_queues(self, num_days: int) -> None:
            Generates the event queues for the itinerary.
    """


    def __init__(
            self, events: List[Event], embedding: List[float]) -> None:
        """ Initializes a new Itinerary object. Processes events by 
            computing similarity + review / rating scores as well as 
            check that the event coordinates are valid.
        Args:
            events (List[Event]): A list of Event objects 
                representing the events in the itinerary.
            embedding (List[float]): A list of floats representing 
                the embedding for the events.
        """
        self.events = []
        self.metadata = {
            event["id"]: event["metadata"] for event in events
        }
        similarity_scores = get_similarity_scores(events, embedding)
        review_rating_scores = get_review_rating_scores(events)
        valid_coord = generate_coord_check_func(events)

        seen_ids = set()
        for idx in range(len(events)):
            event = Event(
                events[idx], similarity_scores[idx], review_rating_scores[idx]
            )
            tripadvisor_id = event.tripadvisor_id
            if valid_coord(event.coord) and tripadvisor_id not in seen_ids:
                self.events.append(event)
                seen_ids.add(tripadvisor_id)

        self.events = np.array(self.events)


    def generate_itinerary(
            self, num_days: int) -> Dict[str, List[Dict[str, Any]]]:
        """ Generates a travel itinerary for the specified 
            number of days.
        Args:
            num_days (int): The number of days for the itinerary.
        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary 
                representing the itinerary.
        """
        self.generate_event_queues(num_days)

        itinerary = {}
        for idx, queue in enumerate(self.queues):
            itinerary[f"day-{idx + 1}"] = [
                format_event(self.metadata[event.id]) for event in queue
            ]
        return itinerary


    def generate_event_queues(self, num_days: int) -> None:
        """ Generates the event queues for the itinerary.
        Args:
            num_days (int): The number of days for the itinerary.
        """
        model = KMeans(num_days)

        weights = denormalise_data([event.score for event in self.events])
        coords = [event.coord for event in self.events]

        assignments = model.fit_predict(coords, sample_weight=weights)
        centroids = model.cluster_centers_

        self.queues = []
        for idx in range(num_days):
            self.queues.append(
                EventQueue(self.events[assignments == idx], centroids[idx])
            )
        self.queues = optimise_order(self.queues)

