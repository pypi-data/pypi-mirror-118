import json
import requests

class API:
    """
    -----------------------------------------------------
    Automation of API fetching and converting to JSON
    -----------------------------------------------------
    
    version: 0.0.2
    
    Recommended Method of Usage:
        `json_object = API(api_url)()` 
        
    This usually returns dicts (might return list depending on the api)
    
    author: Al Razi (https://github.com/abartoha)
    """
    def __init__(self, url:str, space_safety:bool = True, space_substitute:str = "+") -> None:
        """
        ------------------------------------------
        Main Task:
        ------------------------------------------
        Just a request instance 'GET'-ting the api 
        data

        the initial instance of this class will return 
        the __repr__ which is actually a st-
        ring (string of a byte for now!)

        if you "call" that instance like a function, 
        it will return the main json object.

        ------------------------------------------
        space_safety && space_substitute:
        ------------------------------------------
        Checking for whitespaces because you can't 
        trust others to do it! URLs can't have whitespaces 
        in them! It's against nature's law!! 

        By default the thing will be turned on but
        if someone wants to reduce the constant time 
        constraint in his 'algorithm', s/he can and 
        should check the bool off, i guess
        or just change the sustitute character!

        """
        self.url = url
        if (space_safety): #necessary evil
            self.url = url.replace(" ", space_substitute)
        fetch = requests.get(self.url)
        self.request_object = fetch #for debugging purposes i left it here
        self.object_json = json.loads(fetch.content)
        pass
    def __repr__(self) -> str:
        """
        Returns a string verion of the object
        """
        return str(self.request_object.content)
    def __call__(self):
        """
        ------------------------------------------
        Returns the API json in json form (usually dict)
        ------------------------------------------

        because APIs these days can return arrays(lists), 
        objects(dicts), and any combination of these.

        Left this thing to do the same thing as the
        load method, A little strange but not awkward! It might 
        teach noobs how to use more pythonic approaches!
        """
        return self.object_json
    def load(self):
        """
        Added this one unnecessarily

        ------------------------------------------
        Returns the API json in json form (usually dict)
        ------------------------------------------

        because APIs these days can include arrays, 
        dicts, and any combination of these. I think 
        I might need to do more stuff in the near future.
        """
        return self.object_json
