NAME
====

 **BOT** - pure python3 irc bot - https://pypi.org/project/botlib

SYNOPSIS
========

bot \<cmd\> \|options\] \[key=value\] \[key==value\]

CONFIGURATION
=============

| bot cfg server=\<server\> channel=<channel> nick=\<nick\>

| bot cfg users=True
| bot met \<userhost\>

| bot pwd \<nickservnick\> \<nickservpass\>
| bot cfg password=\<outputfrompwd\>

| bot rss \<url\>

| \* default channel/server is #bot on localhost

DESCRIPTION
===========

**BOT** is a IRC bot that can run as a  background
daemon for 24/7 a day presence in a IRC channel. You can use it to
display RSS feeds, act as a UDP to IRC gateway, program your own
commands for it and have it log objects on disk to search them. 

the bot package provides a library you can use to program objects 
under python3, an Object class, that mimics a dict while using 
attribute access and provides a save/load to/from json files on disk. objects
can be searched with database functions and uses read-only files to
improve persistence and a type in filename for reconstruction.

basic usage is this::

>>> from bot.obj import Object
>> o = Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from bot.obj import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> oo = Object()
>>> load(oo, p)
>>> oo.key
>>> 'value'

great for giving objects peristence by having their state stored in files.

the library depends on 3 variables defined in the runtime:

>>> def getmain(name):
>>>     return getattr(sys.modules["__main__"], name, None)
>>>
>>> clt = getmain("clt")
>>> k = getmain("k")
>>> tbl = getmain("tbl")

great for not having to store state in the library.

FILES
=====

| bin/bot
| man/man1/bot.1.gz

COPYRIGHT
=========

**BOT** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

| Bart Thate <bthate67@gmail.com>
