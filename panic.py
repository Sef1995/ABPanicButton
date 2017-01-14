#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
import urllib2
import sched
import time

import threading
from threading import Thread

GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.IN)

def panicListener():
    try:
        while True:
            if GPIO.input(5):
                try:
                    response = urllib2.urlopen('http://abpanic.nl/rpc.php?handle=panic', timeout = 30).read()
                except urllib2.URLError, e:
                    print("There was an error: %r" % e)

                print("Panic")
                print(response)

        sleep(0.00001)
    finally:
        GPIO.cleanup()


def ping():
    starttime=time.time()
    while True:
        try:
            response = urllib2.urlopen('http://abpanic.nl/rpc.php?handle=ping', timeout = 30).read()
        except urllib2.URLError, e:
            print("There was an error: %r" % e)

        print("Ping")
        print(response)
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


if __name__ == '__main__':
    Thread(target = panicListener).start()
    Thread(target = ping).start()
