import os
import re
from shutil import ExecError
import sys
import socket
import pyautogui
from dotenv import load_dotenv

load_dotenv()

class Irc:  

    def __init__(self):
        self.connect_attempt = 0
        self.server = 'irc.twitch.tv'
        self.port = 6667
        self.botname = os.getenv("BOTNAME")
        self.channel = os.getenv("CHANNEL")
        self.botowner = os.getenv("BOTOWNER")
        self.bot_owner_oauth = os.getenv("BOTOWNERAUTH")
        self.irc = socket.socket()
        # self.connect_server()
        self.response = ""
        self.blacklist = []


    def connect_server(self):

        irc = self.irc

        irc.settimeout(15)
        
        try:
            irc.connect((self.server, self.port))
            irc.send(( "PASS " + self.bot_owner_oauth + "\n" +
            "NICK " + self.botname + "\n " +
            "JOIN #" + self.channel + "\n"
            ).encode())
            irc.send("CAP REQ :twitch.tv/commands\n".encode())
            self.joinchat()

        except(Exception):
            raise Exception
            print("Error Connecting to IRC Server")
            if self.connect_attempt < 2:
                self.connect_attempt += 1
                print(f"REattempting to connect attempt {self.connect_attempt} of 2")
                return self.connect_server()
            else:
                sys.exit()


    def joinchat(self):
        print("Establishing connection...")
        loading = True
        while loading:
            readbuffer_join = self.irc.recv(1024)
            chat = readbuffer_join.decode()
            for line in chat.split("\n"):
                print(line)
                if line == '' or 'CAP' in line:
                    continue
                loading = self.loadingComplete(line)
                print(loading)
        if loading == False:
            self.sendMessage("The bot has joined the chat! contols: a, b, up, down, left, right. To blacklist a word type 'blacklistMe(word).'")
            self.receiving_loop()
            
    def loadingComplete(self, line): 
        if "End of /NAMES list" in line:
            print('Bot has joined' + self.channel + "'s Channel")           
            return False
        else:
            return True

    def sendMessage(self, message):
        messageTemp = "PRIVMSG #" + self.channel + " :" + message
        print(messageTemp)
        self.irc.send((messageTemp + "\n").encode())

    def getUser(self, line):
        # separate = line.split(":", 2)
        # user = separate[1].split("!", 1)[0]
        # return user
        pattern = r":(.*)!" #:(.*)!
        userName = re.search(pattern, line)
        if userName:
            userName = userName.group(1)
        else:
            userName = ""

        return userName

    def parse_message(self, twitch_response):
        '''
        Accepts the twitch response string and parses it to return only what the user typed in.
        '''
        print(twitch_response)
        from_bot = bool(re.search(r"^PRIVMSG", twitch_response))
        from_server = bool(re.search(r"^:tmi", twitch_response))
        if twitch_response == "" or from_bot or from_server:
            message = ""
        else:
            pattern = r".:(.*)$"
            message = re.search(pattern, twitch_response)
            if message:
                message = message.group(1)
            else:
                message = ''

        return message

    def user_message(self, twitch_response):
        '''
         returns True if the twitch_response from twitch contains "PRIVMSG" and False otherwise. "PRIVMSG" in the twitch_response means that it is from a user and not the server.
        '''
        if "PRIVMSG" in twitch_response:
            return True
        else:
            return False

    
    def controls(self, response):
        response = response.lower()
        response = response.strip()
        if response == "up":
            pyautogui.keyDown("up")
            pyautogui.keyUp("up")
        elif response == "down":
            pyautogui.keyDown("down")
            pyautogui.keyUp("down")
        elif response == "left":
            pyautogui.keyDown("left")
            pyautogui.keyUp("left")
        elif response == "right":
            pyautogui.keyDown("right")
            pyautogui.keyUp("right")
        elif response == "a":
            pyautogui.keyDown("s")
            pyautogui.keyUp("s")
            print("press a")
        elif response == "b":
            pyautogui.keyDown("a")
            pyautogui.keyUp("a")
            print("press b")
        elif response == "start":
            pyautogui.keyDown("enter")
            pyautogui.keyUp("enter")


    def receiving_loop(self):
        while True:
            try:
                received = self.irc.recv(1024).decode()
            except:
                received = ""

            for line in received.split("\r\n"):
                if line == "":
                    continue
                if "PING" in line and not self.user_message(line):
                    self.response = "PONG.tmi.twitch.tv\r\n".encode()
                    self.irc.send(self.response)
                else:
                    self.response = self.parse_message(line)
                    from_bot = bool(re.search(r"^PRIVMSG", line))
                    from_server = bool(re.search(r"^:tmi", line))
                    if from_bot or from_server:
                        continue
                    user = self.getUser(line)
                    if self.blacklist:
                        for word in self.blacklist:
                            if word in self.response.lower():
                                self.sendMessage(f"@{user} you've used a blacklisted word. This is a warning. Please don't use any blacklisted words.")
                    if "blacklistMe" in self.response:
                        self.blacklist_word(self.response)
                    self.controls(self.response)

    def blacklist_word(self, message):
        if not 'blacklistMe(' in message:
            return
        pattern = r"blacklistMe\((\w*)\)"
        word = re.search(pattern, message).group(1)
        self.blacklist.append(word.lower())
        print(self.blacklist)

        

