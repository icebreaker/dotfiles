#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: rewrite this in Bash script

import os
import subprocess
import sys

class Powerline:
    separator = '⮀'
    separator_thin="⮁"
    ESC = '\e'
    LSQ = '\['
    RSQ = '\]'
    clear_fg = LSQ + ESC + '[38;0m' + RSQ
    clear_bg = LSQ + ESC + '[48;0m' + RSQ
    reset = LSQ + ESC + '[0m' + RSQ

    def __init__(self):
        self.segments = []

    def append(self, content, fg, bg, separator=None, separator_fg=None):
        if separator == None:
            separator = self.separator

        if separator_fg == None:
            separator_fg = bg

        segment = {
            'content': str(content),
            'fg': str(fg),
            'bg': str(bg),
            'separator': str(separator),
            'separator_fg': str(separator_fg)
        }

        self.segments.append(segment)

    def color(self, prefix, code):
        return self.LSQ + self.ESC + '[' + prefix + ';5;' + code + 'm' + self.RSQ

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def draw(self):
        i=0
        line=''

        while i < len(self.segments)-1:
            s = self.segments[i]
            ns = self.segments[i+1]
            line += self.fgcolor(s['fg']) + self.bgcolor(s['bg']) + s['content']
            line += self.fgcolor(s['separator_fg']) + self.bgcolor(ns['bg']) + s['separator']
            i += 1

        s = self.segments[i]
        line += self.fgcolor(s['fg']) + self.bgcolor(s['bg']) + s['content']
        line += self.reset + self.fgcolor(s['separator_fg']) + s['separator'] + self.reset

        return line

def add_git_segment(p):
    try:
        p1 = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p1.communicate()[0].strip()
        if len(output) > 0:
            lines = output.splitlines()
            branch = lines[0].split(' ')[-1].strip()
            fg = 22
            bg = 148
            if len(lines) > 3 and lines[-1] != 'nothing to commit, working tree clean':
                fg = 15
                bg = 124
            p.append(' ' + branch + ' ', fg, bg)
    except subprocess.CalledProcessError:
        pass

def add_cwd_segment(p):
    home = os.getenv('HOME')
    cwd = os.getenv('PWD')

    if cwd.find(home) == 0:
        cwd = cwd.replace(home, '~', 1)

    if cwd[0] == '/':
        cwd = cwd[1:]

    names = cwd.split('/')
    for n in names[:-2]:
        p.append(' ' + n + ' ', 247, 236, Powerline.separator_thin, 247)

    if len(names) > 1:
        p.append(' ' + names[-2] + ' ', 247, 236)

    p.append(' ' + names[-1] + ' ', 231, 240)

def add_root_indicator(p, error):
    bg = 236
    fg = 247
    if int(error) != 0:
        fg = 15
        bg = 161
    p.append(' \$ ', fg, bg)

if __name__ == '__main__':
    p = Powerline()
    add_cwd_segment(p)
    add_git_segment(p)
    add_root_indicator(p, sys.argv[1] if len(sys.argv) > 1 else 0)
    print p.draw()
