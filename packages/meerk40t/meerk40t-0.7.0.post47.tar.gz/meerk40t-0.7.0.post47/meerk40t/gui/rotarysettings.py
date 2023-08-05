#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.3 on Mon Dec 30 01:30:50 2019
#

import wx

from .icons import icons8_roll_50
from .mwindow import MWindow

_ = wx.GetTranslation


class RotarySettings(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(222, 347, *args, **kwds)

        self.checkbox_rotary = wx.CheckBox(self, wx.ID_ANY, _("Rotary"))
        self.text_rotary_scaley = wx.TextCtrl(self, wx.ID_ANY, "1.0")
        self.text_rotary_scalex = wx.TextCtrl(self, wx.ID_ANY, "1.0")
        self.checkbox_rotary_loop = wx.CheckBox(self, wx.ID_ANY, _("Field Loop"))
        self.text_rotary_rotation = wx.TextCtrl(self, wx.ID_ANY, "360.0")
        self.checkbox_rotary_roller = wx.CheckBox(self, wx.ID_ANY, _("Uses Roller"))
        self.text_rotary_roller_circumference = wx.TextCtrl(self, wx.ID_ANY, "50.0")
        self.text_rotary_object_circumference = wx.TextCtrl(self, wx.ID_ANY, "50.0")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.on_check_rotary, self.checkbox_rotary)
        self.Bind(wx.EVT_TEXT, self.on_text_rotary_scale_y, self.text_rotary_scaley)
        self.Bind(wx.EVT_TEXT, self.on_text_rotary_scale_x, self.text_rotary_scalex)
        self.Bind(wx.EVT_CHECKBOX, self.on_check_rotary_loop, self.checkbox_rotary_loop)
        self.Bind(wx.EVT_TEXT, self.on_text_rotation, self.text_rotary_rotation)
        self.Bind(
            wx.EVT_CHECKBOX, self.on_check_rotary_roller, self.checkbox_rotary_roller
        )
        self.Bind(
            wx.EVT_TEXT,
            self.on_text_rotary_roller_circumference,
            self.text_rotary_roller_circumference,
        )
        self.Bind(
            wx.EVT_TEXT,
            self.on_text_rotary_object_circumference,
            self.text_rotary_object_circumference,
        )

    def window_open(self):
        self.context.setting(bool, "rotary", False)
        self.context.setting(float, "scale_x", 1.0)
        self.context.setting(float, "scale_y", 1.0)
        self.text_rotary_scalex.SetValue(str(self.context.scale_x))
        self.text_rotary_scaley.SetValue(str(self.context.scale_y))
        self.checkbox_rotary.SetValue(self.context.rotary)
        self.on_check_rotary(None)

    def window_close(self):
        pass

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_roll_50.GetBitmap())
        self.SetIcon(_icon)
        # begin wxGlade: RotarySettings.__set_properties
        self.SetTitle(_("RotarySettings"))
        self.checkbox_rotary.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.checkbox_rotary.SetToolTip(_("Use Rotary Settings"))
        self.text_rotary_scaley.SetMinSize((80, 23))
        self.text_rotary_scaley.SetToolTip(_("Rotary Scale Factor X"))
        self.text_rotary_scaley.Enable(False)
        self.text_rotary_scalex.SetMinSize((80, 23))
        self.text_rotary_scalex.SetToolTip(_("Rotary Scale Factor Y"))
        self.text_rotary_scalex.Enable(False)
        self.checkbox_rotary_loop.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "Segoe UI",
            )
        )
        self.checkbox_rotary_loop.SetToolTip(_("Use Rotary Settings"))
        self.text_rotary_rotation.SetMinSize((80, 23))
        self.text_rotary_rotation.SetToolTip(_("Steps required for a full rotation"))
        self.text_rotary_rotation.Enable(False)
        self.text_rotary_roller_circumference.SetMinSize((80, 23))
        self.text_rotary_roller_circumference.SetToolTip(_("Circumference of roller"))
        self.text_rotary_roller_circumference.Enable(False)
        self.text_rotary_object_circumference.SetMinSize((80, 23))
        self.text_rotary_object_circumference.SetToolTip(
            _("Circumference of object in rotary")
        )
        self.text_rotary_object_circumference.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RotarySettings.__do_layout
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_circumference = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Object Circumference")), wx.HORIZONTAL
        )
        sizer_20 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Roller Circumference")), wx.HORIZONTAL
        )
        sizer_steps = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Rotation Steps")), wx.HORIZONTAL
        )
        sizer_x = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Scale X")), wx.HORIZONTAL
        )
        sizer_y = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Scale Y")), wx.HORIZONTAL
        )
        sizer_main.Add(self.checkbox_rotary, 0, 0, 0)
        sizer_y.Add(self.text_rotary_scaley, 0, 0, 0)
        sizer_main.Add(sizer_y, 0, wx.EXPAND, 0)
        sizer_x.Add(self.text_rotary_scalex, 0, 0, 0)
        sizer_main.Add(sizer_x, 0, wx.EXPAND, 0)
        sizer_main.Add((20, 20), 0, 0, 0)
        sizer_main.Add(self.checkbox_rotary_loop, 0, 0, 0)
        sizer_steps.Add(self.text_rotary_rotation, 0, 0, 0)
        label_steps = wx.StaticText(self, wx.ID_ANY, _("steps"))
        sizer_steps.Add(label_steps, 0, 0, 0)
        sizer_main.Add(sizer_steps, 0, wx.EXPAND, 0)
        sizer_20.Add(self.checkbox_rotary_roller, 0, 0, 0)
        sizer_20.Add(self.text_rotary_roller_circumference, 0, 0, 0)
        label_mm = wx.StaticText(self, wx.ID_ANY, _("mm"))
        sizer_20.Add(label_mm, 0, 0, 0)
        sizer_main.Add(sizer_20, 0, wx.EXPAND, 0)
        sizer_circumference.Add(self.text_rotary_object_circumference, 0, 0, 0)
        label_mm2 = wx.StaticText(self, wx.ID_ANY, _("mm"))
        sizer_circumference.Add(label_mm2, 0, 0, 0)
        sizer_main.Add(sizer_circumference, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_main)
        self.Layout()
        # end wxGlade

    def on_check_rotary(self, event=None):  # wxGlade: RotarySettings.<event_handler>
        self.context.rotary = self.checkbox_rotary.GetValue()
        self.text_rotary_scalex.Enable(self.checkbox_rotary.GetValue())
        self.text_rotary_scaley.Enable(self.checkbox_rotary.GetValue())

    def on_text_rotary_scale_y(
        self, event=None
    ):  # wxGlade: RotarySettings.<event_handler>
        if self.context is not None:
            try:
                self.context.scale_y = float(self.text_rotary_scaley.GetValue())
            except ValueError:
                pass

    def on_text_rotary_scale_x(
        self, event=None
    ):  # wxGlade: RotarySettings.<event_handler>
        if self.context is not None:
            try:
                self.context.scale_x = float(self.text_rotary_scalex.GetValue())
            except ValueError:
                pass

    def on_check_rotary_loop(self, event):  # wxGlade: RotarySettings.<event_handler>
        print("Event handler 'on_check_rotary_loop' not implemented!")
        event.Skip()

    def on_text_rotation(self, event):  # wxGlade: RotarySettings.<event_handler>
        print("Event handler 'on_text_rotation' not implemented!")
        event.Skip()

    def on_check_rotary_roller(self, event):  # wxGlade: RotarySettings.<event_handler>
        print("Event handler 'on_check_rotary_roller' not implemented!")
        event.Skip()

    def on_text_rotary_roller_circumference(
        self, event
    ):  # wxGlade: RotarySettings.<event_handler>
        print("Event handler 'on_text_rotary_roller_circumference' not implemented!")
        event.Skip()

    def on_text_rotary_object_circumference(
        self, event
    ):  # wxGlade: RotarySettings.<event_handler>
        print("Event handler 'on_text_rotary_object_circumference' not implemented!")
        event.Skip()


# end of class RotarySettings
