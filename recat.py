#!/usr/bin/env python2.7
import os
import fileinput
import time
import datetime
import curses

from tempfile import mkstemp
from shutil import move
from os import remove, close

import sys
import signal

from termcolor import colored, cprint

def file_contain_str(file_path, pattern):
    file = open(file_path)
    for line in file:
        if (line.find(pattern) != -1):
            return True
    
    return False    
    
def lines_in_file(file_path, pattern):
    file = open(file_path)
    lines = []
    for line in file:
        if (line.find(pattern) != -1):
            lines.append(line)
    
    return lines

def find(target_str, excluded_path):

    files_to_search = []

    for path, subdirs, files in os.walk(current_path):
        for name in files:
            file = os.path.join(path, name)
            if (file.find(excluded_path) == -1):
                files_to_search.append(file)
            
    files_found = []

    for file in files_to_search:
        if (file_contain_str(file, target_str)):
            files_found.append({'path': file, 'lines': lines_in_file(file, target_str)})

    return files_found
    '''
    if (len(files_found)):
        for file in files_found:
            cprint('File: ' + file['path'].replace(current_path + '/', ''), 'grey', 'on_white')
            for line in file['lines']:
                cprint(line.replace('\n', ''), 'green')                
    else:
        cprint('No file found.', 'grey', 'on_white')
    '''

def signal_handler(signal, frame):
    curses.endwin()
    sys.exit(0)
    
def current_datetime():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st

def main(arg2, arg3):
    signal.signal(signal.SIGINT, signal_handler)        

    stdscr = curses.initscr()
    while (True):
        line_index = 0
        data = find(arg2, arg3)

        stdscr.addstr(line_index, 0, 'Current time: ' + current_datetime(), curses.A_REVERSE)
        line_index += 1

        for file in data:            
            stdscr.addstr(line_index, 0, 'File: ' + file['path'].replace(current_path + '/', '') + ': ' + str(len(file['lines'])))
            line_index += 1
            '''
            for line in file['lines']:
                stdscr.addstr(line_index, 0, line)
                line_index += 1
            '''
        
        stdscr.refresh()
        time.sleep(1)                


current_path = os.getcwd()

if __name__=='__main__':
    try:
        sys.exit(main(sys.argv[1], sys.argv[2]))
    except Exception as e:
        print e
        curses.endwin()
        sys.exit(0)
