import pytest
from twitch_plays.join_irc import Irc

def test_blacklist_word():
  irc = Irc()
  irc.blacklist_word('blacklistMe(bad)')
  expected = ['bad']
  actual = irc.blacklist
  assert actual == expected


def test_blacklist_word_incorrect_format():
  irc = Irc()
  actual = irc.blacklist_word('blacklistme(bad)')
  expected = None
  assert actual == expected

def test_user_message():
  irc = Irc()
  actual = irc.user_message(':ctgibbs!ctgibbs@ctgibbs.tmi.twitch.tv PRIVMSG #seattcpy401d18 :up')
  expected = True
  assert actual == expected

def test_user_message_noPRIVMSG():
  irc = Irc()
  actual = irc.user_message(':ctgibbs!ctgibbs@ctgibbs.tmi.twitch.tv #seattcpy401d18 :up')
  expected = False
  assert actual == expected

def test_parse_message_from_user():
  irc = Irc()
  actual = irc.parse_message(':ctgibbs!ctgibbs@ctgibbs.tmi.twitch.tv PRIVMSG #seattcpy401d18 :up')
  expected = 'up'
  assert actual == expected

def test_parse_message_empty():
  irc = Irc()
  actual = irc.parse_message('')
  expected = ''
  assert actual == expected

def test_parse_message_from_server():
  irc = Irc()
  actual = irc.parse_message(':tmi the rest of the message')
  expected = ''
  assert actual == expected


def test_parse_message_from_server():
  irc = Irc()
  actual = irc.parse_message('PRIVMSG the rest of the message')
  expected = ''
  assert actual == expected


def test_parse_message_random():
  irc = Irc()
  actual = irc.parse_message('random message')
  expected = ''
  assert actual == expected


def test_getUser():
  irc = Irc()
  actual = irc.getUser(':ctgibbs!ctgibbs@ctgibbs.tmi.twitch.tv #seattcpy401d18 :up')
  expected = 'ctgibbs'
  assert actual == expected


def test_getUser_random():
  irc = Irc()
  actual = irc.getUser('random message')
  expected = ''
  assert actual == expected

def test_loading_complete():
  irc = Irc()
  actual = irc.loadingComplete('End of /NAMES list is in the string')
  expected = False
  assert expected == actual


def test_loading_complete_random_message():
  irc = Irc()
  actual = irc.loadingComplete('randomness of messages')
  expected = True
  assert expected == actual