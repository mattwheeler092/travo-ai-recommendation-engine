from functools import wraps
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


class RecommendationRequest(BaseModel):
    """ Pydantic class representing the structure of the 
        request payload for recommendation endpoint. """
    destination: str
    namespace: str
    num_days: int
    user_query: str
    user_preferences: list[str]


def rate_limit(limit: int):
    """ Decorator to limit the number of requests to the server 
        to avoid exceeding a specified limit.
    Parameters:
        limit (int): The maximum number of requests allowed 
            within the specified timeframe.
    Returns:
        decorator (callable): The actual decorator that will 
            be applied to the target function.
    """
    def decorator(func):
        counter = 0

        @wraps(func)
        async def wrapper(*args, **kwargs):
            """ Wrapper function that checks the request counter 
                and limits the number of requests.
            Parameters:
                args: The positional arguments passed to the target function.
                kwargs: The keyword arguments passed to the target function.
            Returns:
                The result of the target function call.
            """
            nonlocal counter
            if counter >= limit:
                raise HTTPException(
                    status_code=429, detail="Too Many Requests")
            counter += 1
            return await func(*args, **kwargs)

        return wrapper

    return decorator
