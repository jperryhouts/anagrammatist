#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#

'''
This file is part of Anagrammatist.

Anagrammatist is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Anagrammatist is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import gettext, os, sys, wx
try:
    # wxPython >= 4.0
    from wx.adv import AboutDialogInfo as wxAboutDialogInfo
    from wx.adv import AboutBox as wxAboutBox
except ImportError:
    # wxPython < 4.0
    from wx import AboutDialogInfo as wxAboutDialogInfo
    from wx import AboutBox as wxAboutBox
import numpy as np

class Dictionary:
    def __init__(self, DICT='resources/english.dic'):
        self.dict_path = os.path.realpath(DICT)
        self.dict = [w.strip() for w in open(DICT).readlines()]
        self.dict_cca = np.array([self.to_cca(word) for word in self.dict])

    def get_dict_path(self):
        return self.dict_path

    def index(self, c):
        ''' Map Z->N and W->M, etc. '''
        if c == ord('Z'): c = ord('N')
        elif c == ord('W'): c = ord('M')
        return c - ord('A')

    def to_cca(self, word):
        ''' Returns 26-index array of letter counts in string
        (character count array = cca)'''
        W = [self.index(c) for c in bytearray(word.upper(), 'utf-8')]
        return np.array([W.count(i) for i in range(26)])

    def find_lexigrams(self, full, used):
        ''' Returns possible lexigrams from leftover letters. If the anagram
        cannot be spelled with the input letters, will return useful error
        message instead. '''
        letter_bank = self.to_cca(full) - self.to_cca(used)
        res = []
        if min(letter_bank) < 0:
            for c in np.where(letter_bank<0)[0]:
                pluralizer = '\'s' if letter_bank[c] < -1 else ''
                res.append('Short {} letter {}{}'.format(-letter_bank[c], \
                        chr(c+ord('A')),pluralizer))
        else:
            w = np.where(np.min(letter_bank-self.dict_cca, axis=1) >= 0)
            res = [self.dict[i] for i in w[0]]
        return '\n'.join(res)
# end of class Dictionary

class AnagrammatistFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds['style'] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.script_root = os.path.dirname(os.path.realpath(sys.argv[0]))
        # Menu Bar
        self.main_menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.open_menu_item = wx.MenuItem(self.file_menu, wx.ID_ANY, \
                _('Load Dictionary\tCtrl+O'), 'Load Dictionary', wx.ITEM_NORMAL)
        try:
            self.file_menu.Append(self.open_menu_item)
        except TypeError:
            self.file_menu.AppendItem(self.open_menu_item)
        self.quit_menu_item = wx.MenuItem(self.file_menu, wx.ID_ANY, \
                _('Quit\tCtrl+Q'), 'Exit Anagrammatist', wx.ITEM_NORMAL)
        try:
            self.file_menu.Append(self.quit_menu_item)
        except TypeError:
            self.file_menu.AppendItem(self.quit_menu_item)
        self.main_menubar.Append(self.file_menu, _('File'))
        self.help_menu = wx.Menu()
        self.about_menu_item = wx.MenuItem(self.help_menu, wx.ID_ANY, \
                _('About'), 'About Anagrammatist', wx.ITEM_NORMAL)
        try:
            self.help_menu.Append(self.about_menu_item)
        except TypeError:
            self.help_menu.AppendItem(self.about_menu_item)
        self.main_menubar.Append(self.help_menu, _('Help'))
        self.SetMenuBar(self.main_menubar)
        # Menu Bar end
        self.main_statusbar = self.CreateStatusBar(1, 0)
        self.input_label = wx.StaticText(self, wx.ID_ANY, \
                _('    Input: '), style=wx.ALIGN_RIGHT)
        self.input_txt = wx.TextCtrl(self, wx.ID_ANY, '')
        self.anagram_label = wx.StaticText(self, wx.ID_ANY, \
                _('    Anagram: '), style=wx.ALIGN_RIGHT)
        self.anagram_txt = wx.TextCtrl(self, wx.ID_ANY, '')
        self.lexigrams_txt = wx.TextCtrl(self, wx.ID_ANY, _(''), \
                style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.inputs_changed, self.input_txt)
        self.Bind(wx.EVT_TEXT, self.inputs_changed, self.anagram_txt)
        self.Bind(wx.EVT_MENU, self.open_dict, self.open_menu_item)
        self.Bind(wx.EVT_MENU, self.show_about, self.about_menu_item)
        self.Bind(wx.EVT_MENU, self.on_exit, self.quit_menu_item)
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        quitId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_exit, id=quitId)
        openId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.open_dict, id=openId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Q'), quitId), \
                (wx.ACCEL_CTRL, ord('O'), openId)])
        self.SetAcceleratorTable(accel_tbl)

    def __set_properties(self):
        self.SetTitle(_('Anagrammatist'))
        try:
            _icon = wx.Icon()
        except TypeError:
            _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(os.path.join(self.script_root, \
                'resources/icon.png'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((600, 450))
        self.main_statusbar.SetStatusWidths([-1])
        # statusbar fields
        main_statusbar_fields = ['']
        for i in range(len(main_statusbar_fields)):
            self.main_statusbar.SetStatusText(main_statusbar_fields[i], i)

    def __do_layout(self):
        grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(1, 4, 0, 0)
        grid_sizer_2.Add(self.input_label, 0, \
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.input_txt, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.anagram_label, 0, \
                wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.anagram_txt, 0, wx.EXPAND, 0)
        grid_sizer_2.AddGrowableCol(1)
        grid_sizer_2.AddGrowableCol(3)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.lexigrams_txt, 0, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(0)
        self.Layout()

    def do_update(self):
        orig = self.input_txt.GetValue()
        anagram = self.anagram_txt.GetValue()
        lexigrams = self.dictionary.find_lexigrams(orig, anagram)
        self.lexigrams_txt.SetValue(lexigrams)

    def inputs_changed(self, event):
        self.do_update()
        event.Skip()

    def load_dictionary(self, dict_path):
        self.main_statusbar.SetStatusText('Loading Dictionary...', 0)
        self.dictionary = Dictionary(dict_path)
        self.main_statusbar.SetStatusText('', 0)
        self.do_update()

    def open_dict(self, event):
        curpath = self.dictionary.get_dict_path()
        fdlg = wx.FileDialog(self, 'Dictionary file path', \
                os.path.dirname(curpath), os.path.basename(curpath), \
                'Dictionary files(*.dic)|*.*', wx.FD_OPEN)
        if fdlg.ShowModal() == wx.ID_OK:
            self.load_dictionary(fdlg.GetPath())
        event.Skip()

    def show_about(self, event):
        license = _('''
    Anagrammatist Anagram Generator
    Copyright (C) 2014 Jonathan Perry-Houts

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
        ''')
        info = wxAboutDialogInfo()
        info.SetIcon(wx.Icon(os.path.join(self.script_root, \
                'resources/icon.png'), wx.BITMAP_TYPE_PNG))
        info.SetName('Anagrammatist')
        info.SetVersion('0.98b')
        info.SetDescription('Anagram Generator')
        info.SetCopyright('(C) 2014-2018 Jonathan Perry-Houts')
        info.SetWebSite('https://github.com/jperryhouts/anagrammatist')
        info.SetLicence(license)
        info.AddDeveloper('Jonathan Perry-Houts')
        info.AddDocWriter('Jonathan Perry-Houts')
        wxAboutBox(info)
        event.Skip()

    def on_exit(self, event):
        self.Destroy()
        event.Skip()
# end of class AnagrammatistFrame

class AnagrammatistGUI(wx.App):
    def OnInit(self):
        self.main_frame = AnagrammatistFrame(None, wx.ID_ANY, '')
        self.SetTopWindow(self.main_frame)
        self.main_frame.Show()
        return 1

    def load_dictionary(self, path):
        self.main_frame.load_dictionary(path)
# end of class AnagrammatistGUI

if __name__ == '__main__':
    gettext.install('app')

    app = AnagrammatistGUI(0)
    script_root = os.path.dirname(os.path.realpath(sys.argv[0]))
    app.load_dictionary(os.path.join(script_root, 'resources/english.dic'))
    app.MainLoop()
