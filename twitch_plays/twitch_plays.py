from dotenv import load_dotenv

def user_message(twitch_response):
  '''
  returns True if the twitch_response from twitch contains "PRIVMSG" and False otherwise. "PRIVMSG" in the twitch_response means that it is from a user and not the server. 
  '''
  if "PRIVMSG" in twitch_response:
    return True
  else:
    return False

load_dotenv()