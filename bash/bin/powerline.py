#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

class Powerline:
    ESC   = '\e'
    LSQ   = '\['
    RSQ   = '\]'
    RESET = LSQ + ESC + '[0m' + RSQ
    BG0   = '236'
    BG1   = '237'
    FG    = '250'
    RED   = '124'
    PINK  = '126'
    GREEN = '23'

    def __init__(self):
        self.segments = []

    def append(self, text, fg = None, bg = None):
        segment = {
            'text': str(text),
            'fg': fg,
            'bg': bg
        }

        self.segments.append(segment)

    def color(self, prefix, code):
        return self.LSQ + self.ESC + '[' + prefix + ';5;' + code + 'm' + self.RSQ

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def draw(self):
        line = ''

        fg = self.FG
        bg = self.BG0

        if len(self.segments) % 2:
            bg = self.BG1

        for s in self.segments:
            line += self.fgcolor(s['fg'] or fg) + self.bgcolor(s['bg'] or bg) + s['text']

            if bg == self.BG0:
                bg = self.BG1
            else:
                bg = self.BG0

        line += self.RESET

        return line

    def add_git_segment(self):
        try:
            p1 = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output = p1.communicate()[0].strip()
            if len(output) == 0:
                return

            lines = output.splitlines()
            branch = lines[0].split(' ')[-1].strip()

            bg = self.GREEN

            if len(lines) > 3 and lines[-1] != 'nothing to commit, working tree clean':
                bg = self.RED

            self.append(' ' + branch + ' ', None, bg)
        except subprocess.CalledProcessError:
            pass

    def add_cwd_segment(self):
        home = os.getenv('HOME')
        cwd = os.getenv('PWD')

        if cwd.find(home) == 0:
            cwd = cwd.replace(home, '~', 1)

        if cwd[0] == '/':
            cwd = cwd[1:]

        if len(cwd) == 0:
            return

        names = cwd.split('/')

        for name in names:
            self.append(' ' + name + ' ')

    def add_root_indicator_segment(self, error):
        bg = None

        if int(error) != 0:
            bg = self.PINK

        self.append(' \$ ', None, bg)

if __name__ == '__main__':
    p = Powerline()
    p.add_cwd_segment()
    p.add_git_segment()
    p.add_root_indicator_segment(sys.argv[1] if len(sys.argv) > 1 else 0)
    print(p.draw())
