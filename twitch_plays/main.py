import socket

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

def getMessage(line):
    global message
    try:
        message = (line.split(":",2))[2]
    except:
        message = ""
    return message

def Console(line):
    if "" in line:
        return False
    else:
        return True




joinchat()

while True:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                print(msgg)
                continue
            else:
                print(line)
                user = getUser(line)
                message = getMessage(line)
                print(user + " : " + message)



# while True:
#     try:
#         readbuffer = irc.recv(1024).decode()
#     except:
#         readbuffer = ""
#     for line in readbuffer.split("\r\n"):
#         if line == "":
#             continue
#         else:
#             getUser(line)
#             print(line)
