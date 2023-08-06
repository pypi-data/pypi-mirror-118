#!/usr/bin/env python

import os
import math
from yatts import style

class FramedTitle:

    def __init__(self, titles, frame_type = 'hash', frame_color = 'white',
            text_color = 'white', text_align = 'center', bg_color = None,
            margin = 0, padding = 1):

        self.titles = titles
        self.frame_type = frame_type
        self.frame_color = frame_color
        self.text_color = text_color
        self.text_align = text_align
        self.bg_color = bg_color

        self.set_margin(margin)
        self.set_padding(padding)

        self.FRAMES = {
            'stroke':           ['│', '─', '┌', '┐', '└', '┘'],
            'double_stroke':    ['║', '═', '╔', '╗', '╚', '╝'],
            'simple':           ['|', '-', '+', '+', '+', '+'],
            'hash':             ['#', '#', '#', '#', '#', '#']
        }

        self.rows, self.cols = self.get_term_size()

    def create_horizontal(self, dir):
        top = ' ' * self.margin_left
        top += self.get_frame_char(2 if dir == 'top' else 4)
        top += self.get_frame_char(1) * (self.cols-2-self.margin_left-self.margin_right)
        top += self.get_frame_char(3 if dir == 'top' else 5)
        top += ' ' * self.margin_right

        return style(top, self.frame_color)

    def create_newline(self, text = ''):
        gap_left = 0
        gap_right = 0

        if self.text_align == 'left' or self.text_align == 'right':
            margin = self.margin_left + self.margin_right
            padding = self.padding_left + self.padding_right

            if self.text_align == 'left':
                gap_left = ''
                gap_right = ' ' * (self.cols-2-len(text)-margin-padding)

            if self.text_align == 'right':
                gap_left = ' ' * (self.cols-2-len(text)-margin-padding)
                gap_right = ''

        if self.text_align == 'center':
            gap_size = (self.cols-2-len(text))/2

            gap_left = ' ' * (math.ceil(gap_size)-self.margin_left-self.padding_left)
            gap_right = ' ' * (math.floor(gap_size)-self.margin_right-self.padding_right)

        line = ' ' * self.margin_left
        line += style(self.get_frame_char(0), self.frame_color)
        line += style(' ' * self.padding_left, bgcolor=self.bg_color)
        line += style(gap_left + text + gap_right, self.text_color, self.bg_color)
        line += style(' ' * self.padding_right, bgcolor=self.bg_color)
        line += style(self.get_frame_char(0), self.frame_color)
        line += ' ' * self.margin_right

        return line

    def show(self):
        for _ in range(self.margin_top):
            print('')

        print(self.create_horizontal('top'))
        for _ in range(self.padding_top):
            print(self.create_newline())

        if type(self.titles) is str:
            print(self.create_newline(self.titles))
        elif type(self.titles) is list:
            for title in self.titles:
                print(self.create_newline(title))

        for _ in range(self.padding_bottom):
            print(self.create_newline(''))
        print(self.create_horizontal('bottom'))

        for _ in range(self.margin_bottom):
            print('')

    def get_frame_char(self, n):
        return self.FRAMES[self.frame_type][n]

    def set_margin(self, a, b = None, c = None, d = None):
        if b is None:
            self.margin_top = a
            self.margin_right = a
            self.margin_bottom = a
            self.margin_left = a
        elif c is None and d is None:
            self.margin_top = a
            self.margin_right = b
            self.margin_bottom = a
            self.margin_left = b
        elif c is not None and d is not None:
            self.margin_top = a
            self.margin_right = b
            self.margin_bottom = c
            self.margin_left = d
        else:
            self.margin_top = 0
            self.margin_right = 0
            self.margin_bottom = 0
            self.margin_left = 0

    def set_padding(self, a, b=None, c=None, d=None):
        if b is None:
            self.padding_top = a
            self.padding_right = a
            self.padding_bottom = a
            self.padding_left = a
        elif c is None and d is None:
            self.padding_top = a
            self.padding_right = b
            self.padding_bottom = a
            self.padding_left = b
        elif c is not None and d is not None:
            self.padding_top = a
            self.padding_right = b
            self.padding_bottom = c
            self.padding_left = d
        else:
            self.padding_top = 0
            self.padding_right = 0
            self.padding_bottom = 0
            self.padding_left = 0

    def get_term_size(self):
        r, c = os.popen('stty size', 'r').read().split()
        return int(r), int(c)
