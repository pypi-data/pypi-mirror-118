import requests

class Invalid(Exception):
    """Exception raised when the api return nothing.
    """

    def __init__(self, message="Could not get a response. Try again by checking the api key and bid."):
        self.message = message
        super().__init__(self.message)

class EmptyMessage(Exception):
    """Exception raised when the message is empty.
    """

    def __init__(self, message="Message cannot be empty."):
        self.message = message
        super().__init__(self.message)


class Brain():
    def __init__(self,key : str , bid : int):
        super().__init__()
        self.key = key
        self.bid = bid

    def ask(self, message):
        """
        Get response from the api.\n
        Attributes:\n
        message :str -- input of a message
        """
        if len(message) > 0:

            res = requests.get(f"http://api.brainshop.ai/get?bid={self.bid}&key={self.key}&uid=[uid]&msg={message}").json()['cnt']
            if len(res) > 0:
                return res
            else:
                raise Invalid
        else:
            raise EmptyMessage
