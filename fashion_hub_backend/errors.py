"""
This file contains exceptions classes for invalid API requests.
"""


class ErrorBase(Exception):  # noqa: N818
    def __init__(self, detail: str = "unspecificed error"):
        """
        detail: Details on the error, can be returned by the API.
        """
        self.detail = detail

    def model_dump(self):
        return {"detail": self.detail}


class APIBadRequest(ErrorBase):
    """
    Error type for an generic invalid request.
    """

    def __init__(self, detail: str):
        super().__init__(detail)


class APINotFound(ErrorBase):
    """
    Error type for an invalid reference to an object.
    """

    def __init__(self, key: int | str | dict, detail: str | None = None):
        """
        keys: The missing key (if keys is int or str) or a dictionary of several
              joint identifiers (e.g., keys={"diagram_id": 1, "name": "Node1"}).
        """
        self.key = key
        if not detail:
            detail = f"not found: {key}"
        super().__init__(detail)

    def model_dump(self):
        return {
            **super().model_dump(),
            "key": self.key,
        }


class DataBaseNotFound(ErrorBase):
    """
    Internal error for database connection issues.
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        if not detail:
            detail = f"Database does not exist: {db_name}"
        super().__init__(detail)

    def model_dump(self):
        return {
            **super().model_dump(),
            "dbName": self.db_name,
        }
