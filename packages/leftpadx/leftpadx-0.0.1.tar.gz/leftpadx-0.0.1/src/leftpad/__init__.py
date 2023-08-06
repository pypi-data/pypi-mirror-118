import urllib.request as urllib
from urllib.parse import urlencode
import json

def leftpad(string, length, character):
    """A function that pads a string to the left with a character. The character must be just one character and the length is the length of the padded string, not the padding."""
    return json.loads(urllib.urlopen("https://api.left-pad.io/?" + urlencode({'str' : string, 'len' : length, 'ch' : character}, True)).read().decode('utf-8'))['str']
if __name__ == "__main__":
    print(leftpad("epic", 100, "@"))