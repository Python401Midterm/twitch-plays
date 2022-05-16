from dotenv import load_dotenv
import re

def user_message(twitch_response):
  '''
  returns True if the twitch_response from twitch contains "PRIVMSG" and False otherwise. "PRIVMSG" in the twitch_response means that it is from a user and not the server. 
  '''
  if "PRIVMSG" in twitch_response:
    return True
  else:
    return False

def parse_message(twitch_response):
  '''
  Accepts the twitch response string and parses it to return only what the user typed in. 
  '''
  if twitch_response == "":
    message = ""
  else:
    pattern = r".:(.*)$"
    message = re.search(pattern, twitch_response).group(1)

  return message

load_dotenv()