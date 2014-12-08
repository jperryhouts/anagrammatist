#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Sun Nov 23 12:03:07 2014
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

import os, sys, wx
from lexigrams import Dictionary

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class AnagrammatistFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: AnagrammatistFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self.script_root = os.path.dirname(os.path.realpath(sys.argv[0]))
        # Menu Bar
        self.main_menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.quit_menu_item = wx.MenuItem(self.file_menu, wx.ID_ANY, _("Quit\tCtrl+Q"), "Exit Anagrammatist", wx.ITEM_NORMAL)
        self.file_menu.AppendItem(self.quit_menu_item)
        self.main_menubar.Append(self.file_menu, _("File"))
        self.help_menu = wx.Menu()
        self.about_menu_item = wx.MenuItem(self.help_menu, wx.ID_ANY, _("About"), "About Anagrammatist", wx.ITEM_NORMAL)
        self.help_menu.AppendItem(self.about_menu_item)
        self.main_menubar.Append(self.help_menu, _("Help"))
        self.SetMenuBar(self.main_menubar)
        # Menu Bar end
        self.main_statusbar = self.CreateStatusBar(1, 0)
        self.input_label = wx.StaticText(self, wx.ID_ANY, _("    Input: "), style=wx.ALIGN_RIGHT)
        self.input_txt = wx.TextCtrl(self, wx.ID_ANY, "")
        self.anagram_label = wx.StaticText(self, wx.ID_ANY, _("    Anagram: "), style=wx.ALIGN_RIGHT)
        self.anagram_txt = wx.TextCtrl(self, wx.ID_ANY, "")
        self.lexigrams_txt = wx.TextCtrl(self, wx.ID_ANY, _(""), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.UPDATE, self.input_txt)
        self.Bind(wx.EVT_TEXT, self.UPDATE, self.anagram_txt)
        # end wxGlade
        self.Bind(wx.EVT_MENU, self.on_exit, self.quit_menu_item)
        self.Bind(wx.EVT_MENU, self.show_about, self.about_menu_item)
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        randomId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_exit, id=randomId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Q'), randomId)])
        self.SetAcceleratorTable(accel_tbl)

        self.dictionary = Dictionary(os.path.join(self.script_root, 'english.dic'))

    def __set_properties(self):
        # begin wxGlade: AnagrammatistFrame.__set_properties
        self.SetTitle(_("Anagrammatist"))
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(os.path.join(self.script_root, 'A-icon.png'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((600, 450))
        self.main_statusbar.SetStatusWidths([-1])
        # statusbar fields
        main_statusbar_fields = [""]
        for i in range(len(main_statusbar_fields)):
            self.main_statusbar.SetStatusText(main_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: AnagrammatistFrame.__do_layout
        grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_2 = wx.FlexGridSizer(1, 4, 0, 0)
        grid_sizer_2.Add(self.input_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.input_txt, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.anagram_label, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_2.Add(self.anagram_txt, 0, wx.EXPAND, 0)
        grid_sizer_2.AddGrowableCol(1)
        grid_sizer_2.AddGrowableCol(3)
        grid_sizer_1.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.lexigrams_txt, 0, wx.EXPAND, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.AddGrowableRow(1)
        grid_sizer_1.AddGrowableCol(0)
        self.Layout()
        # end wxGlade

    def UPDATE(self, event):  # wxGlade: AnagrammatistFrame.<event_handler>
        orig = self.input_txt.GetValue()
        anagram = self.anagram_txt.GetValue()
        lexigrams = self.dictionary.find_lexigrams(orig, anagram)
        self.lexigrams_txt.SetValue(lexigrams)
        event.Skip()

    def show_about(self, event):
        print('Not implemented.')

    def on_exit(self, event):
        self.Destroy()

# end of class AnagrammatistFrame
class AnagrammatistGUI(wx.App):
    def OnInit(self):
        #wx.InitAllImageHandlers()
        main_frame = AnagrammatistFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(main_frame)
        main_frame.Show()
        return 1

# end of class AnagrammatistGUI

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = AnagrammatistGUI(0)
    app.MainLoop()
