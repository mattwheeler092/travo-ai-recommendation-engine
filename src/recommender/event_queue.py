import sys
from pathlib import Path
from typing import Generator, List

sys.path.append(str(Path(__file__).resolve().parent.parent))

from .utils import optimise_order, get_distance_scores
from config import MAX_DURARTION, MAX_EVENTS
from .event import Event


class EventQueue:
    """ A class representing a queue of events for a day's itinerary.

    Attributes:
        coord (List[float]): A list of floats representing the 
            centroid of the queue.
        selected_events (List[Event]): A list of Event objects 
            representing the selected events for the day's itinerary.
        events (List[Event]): A list of Event objects representing 
            the events in the queue.

    Methods:
        __init__(self, events: List[Event], coord: List[float]) -> None:
            Initializes a new EventQueue object.
        select_events(self) -> None:
            Selects events for the day's itinerary.
        __iter__(self) -> Generator[Event, None, None]:
            Returns an iterator over the selected events.
    """


    def __init__(self, events: List[Event], coord: List[float]) -> None:
        """ Initializes a new EventQueue object.
        Args:
            events (List[Event]): A list of Event objects 
                representing the events in the queue.
            coord (List[float]): A list of floats representing 
                the centroid of the queue.
        """
        self.coord = coord
        self.selected_events = []
        self.events = events

        distances = get_distance_scores(events, coord)
        for idx, dist in enumerate(distances):
            self.events[idx].distance_score = dist
        self.events = sorted(
            self.events, key=lambda event: event.score, reverse=True
        )
        self.select_events()


    def select_events(self) -> None:
        """ Selects events for the day's itinerary ensuring 
            that neither the total event duration or number 
            of events exceeds its maximum. """
        total_duration = 0

        while (total_duration < MAX_DURARTION and 
               len(self.selected_events) < MAX_EVENTS):
            
            idx = len(self.selected_events)
            self.selected_events.append(self.events[idx])
            total_duration += self.events[idx].duration

        self.selected_events = optimise_order(self.selected_events)


    def __iter__(self) -> Generator[Event, None, None]:
        """ Returns an iterator over the selected events.
        Yields:
            Event: An Event object representing an event in 
                the day's itinerary.
        """
        for event in self.selected_events:
            yield event
