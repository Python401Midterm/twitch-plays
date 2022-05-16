import socket
import re
from dotenv import load_dotenv
from game_controls import controls
from join_irc import Irc
import threading

SERVER = 'irc.twitch.tv'
PORT = 6667
PASS = 'oauth:8jztt62rrdnfh8yjn9d0gi1k4qn5gr'
BOT = 'twitchbot'
CHANNEL = 'seattcpy401d18'
OWNER = 'seattcpy401d18bot'
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(( "PASS " + PASS + "\n" +
          "NICK " + BOT + "\n " +
          "JOIN #" + CHANNEL + "\n"
          ).encode())


def joinchat():
    Loading = True
    while Loading:
        readbuffer_join = irc.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        for line in readbuffer_join.split("\n")[0:-1]:
            print(line)
            Loading = loadingComplete(line)


def loadingComplete(line):
    if "End of /NAMES list" in line:
        print('Bot has joined' + CHANNEL + "'s Channel")
        sendMessage(irc, "Chat Room Joined")

        return False
    else:
        return True

def sendMessage(irc, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    irc.send((messageTemp + "\n").encode())

def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user

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

def user_message(twitch_response):
  '''
  returns True if the twitch_response from twitch contains "PRIVMSG" and False otherwise. "PRIVMSG" in the twitch_response means that it is from a user and not the server.
  '''
  if "PRIVMSG" in twitch_response:
    return True
  else:
    return False


joinchat()



def receiving_loop():
    global response
    while True:
        try:
            received = irc.recv(1024).decode()
        except:
            received = ""

        for line in received.split("\r\n"):
            if "PING" in line and not user_message(line):
                response = "PONG.tmi.twitch.tv\r\n".encode()
                irc.send(response)
            else:
                response = parse_message(line)



load_dotenv()

if __name__ == "__main__":
    One = threading.Thread(target = Irc())
    One.start()
    Two = threading.Thread(target = controls)
    Two.start()