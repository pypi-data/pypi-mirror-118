# -*- coding: ISO-8859-1 -*-

import wx

from meerk40t.gui.icons import icons8_administrative_tools_50
from meerk40t.gui.mwindow import MWindow

_ = wx.GetTranslation


class LhystudiosAccelerationChart(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(551, 234, *args, **kwds)
        self.checkbox_vector_accel_enable = wx.CheckBox(self, wx.ID_ANY, _("Enable"))
        self.text_vector_accel_1 = wx.TextCtrl(self, wx.ID_ANY, "25.4")
        self.text_vector_accel_2 = wx.TextCtrl(self, wx.ID_ANY, "60")
        self.text_vector_accel_3 = wx.TextCtrl(self, wx.ID_ANY, "127")
        self.text_vector_accel_4 = wx.TextCtrl(self, wx.ID_ANY, _("infinity"))
        self.checkbox_vraster_accel_enable = wx.CheckBox(self, wx.ID_ANY, _("Enable"))
        self.text_vraster_accel_1 = wx.TextCtrl(self, wx.ID_ANY, "25.4")
        self.text_vraster_accel_2 = wx.TextCtrl(self, wx.ID_ANY, "60")
        self.text_vraster_accel_3 = wx.TextCtrl(self, wx.ID_ANY, "127")
        self.text_vraster_accel_4 = wx.TextCtrl(self, wx.ID_ANY, _("infinity"))
        self.checkbox_raster_accel_enable = wx.CheckBox(self, wx.ID_ANY, _("Enable"))
        self.text_raster_accel_1 = wx.TextCtrl(self, wx.ID_ANY, "25.4")
        self.text_raster_accel_2 = wx.TextCtrl(self, wx.ID_ANY, "127")
        self.text_raster_accel_3 = wx.TextCtrl(self, wx.ID_ANY, "320")
        self.text_raster_accel_4 = wx.TextCtrl(self, wx.ID_ANY, _("infinity"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_CHECKBOX,
            self.on_check_vector_accel_enable,
            self.checkbox_vector_accel_enable,
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vector_accel, self.text_vector_accel_1)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vector_accel, self.text_vector_accel_1
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vector_accel, self.text_vector_accel_2)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vector_accel, self.text_vector_accel_2
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vector_accel, self.text_vector_accel_3)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vector_accel, self.text_vector_accel_3
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vector_accel, self.text_vector_accel_4)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vector_accel, self.text_vector_accel_4
        )
        self.Bind(
            wx.EVT_CHECKBOX,
            self.on_check_vraster_accel_enable,
            self.checkbox_vraster_accel_enable,
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vraster_accel, self.text_vraster_accel_1)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vraster_accel, self.text_vraster_accel_1
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vraster_accel, self.text_vraster_accel_2)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vraster_accel, self.text_vraster_accel_2
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vraster_accel, self.text_vraster_accel_3)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vraster_accel, self.text_vraster_accel_3
        )
        self.Bind(wx.EVT_TEXT, self.on_text_vraster_accel, self.text_vraster_accel_4)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_vraster_accel, self.text_vraster_accel_4
        )
        self.Bind(
            wx.EVT_CHECKBOX,
            self.on_check_raster_accel_enable,
            self.checkbox_raster_accel_enable,
        )
        self.Bind(wx.EVT_TEXT, self.on_text_raster_accel, self.text_raster_accel_1)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_raster_accel, self.text_raster_accel_1
        )
        self.Bind(wx.EVT_TEXT, self.on_text_raster_accel, self.text_raster_accel_2)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_raster_accel, self.text_raster_accel_2
        )
        self.Bind(wx.EVT_TEXT, self.on_text_raster_accel, self.text_raster_accel_3)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_raster_accel, self.text_raster_accel_3
        )
        self.Bind(wx.EVT_TEXT, self.on_text_raster_accel, self.text_raster_accel_4)
        self.Bind(
            wx.EVT_TEXT_ENTER, self.on_text_raster_accel, self.text_raster_accel_4
        )
        # end wxGlade
        self.set_widgets()

    def __set_properties(self):
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_("Acceleration Chart"))
        self.checkbox_vector_accel_enable.SetToolTip(
            _("Enable defined acceleration chart for vectors")
        )
        self.text_vector_accel_1.SetMinSize((55, 23))
        self.text_vector_accel_1.SetToolTip(_("Upper limit for accel level %d") % 1)
        self.text_vector_accel_1.Enable(False)
        self.text_vector_accel_2.SetMinSize((55, 23))
        self.text_vector_accel_2.SetToolTip(_("Upper limit for accel level %d") % 2)
        self.text_vector_accel_2.Enable(False)
        self.text_vector_accel_3.SetMinSize((55, 23))
        self.text_vector_accel_3.SetToolTip(_("Upper limit for accel level %d") % 3)
        self.text_vector_accel_3.Enable(False)
        self.text_vector_accel_4.SetMinSize((55, 23))
        self.text_vector_accel_4.SetToolTip(_("Upper limit for accel level %d") % 4)
        self.text_vector_accel_4.Enable(False)
        self.checkbox_vraster_accel_enable.SetToolTip(
            _("Enable defined acceleration chart for vertical rasters")
        )
        self.text_vraster_accel_1.SetMinSize((55, 23))
        self.text_vraster_accel_1.SetToolTip(_("Upper limit for accel level %d") % 1)
        self.text_vraster_accel_1.Enable(False)
        self.text_vraster_accel_2.SetMinSize((55, 23))
        self.text_vraster_accel_2.SetToolTip(_("Upper limit for accel level %d") % 2)
        self.text_vraster_accel_2.Enable(False)
        self.text_vraster_accel_3.SetMinSize((55, 23))
        self.text_vraster_accel_3.SetToolTip(_("Upper limit for accel level %d") % 3)
        self.text_vraster_accel_3.Enable(False)
        self.text_vraster_accel_4.SetMinSize((55, 23))
        self.text_vraster_accel_4.SetToolTip(_("Upper limit for accel level %d") % 4)
        self.text_vraster_accel_4.Enable(False)
        self.checkbox_raster_accel_enable.SetToolTip(
            _("Enable defined acceleration chart for horizontal rasters")
        )
        self.text_raster_accel_1.SetMinSize((55, 23))
        self.text_raster_accel_1.SetToolTip(_("Upper limit for accel level %d") % 1)
        self.text_raster_accel_1.Enable(False)
        self.text_raster_accel_2.SetMinSize((55, 23))
        self.text_raster_accel_2.SetToolTip(_("Upper limit for accel level %d") % 2)
        self.text_raster_accel_2.Enable(False)
        self.text_raster_accel_3.SetMinSize((55, 23))
        self.text_raster_accel_3.SetToolTip(_("Upper limit for accel level %d") % 3)
        self.text_raster_accel_3.Enable(False)
        self.text_raster_accel_4.SetMinSize((55, 23))
        self.text_raster_accel_4.SetToolTip(_("Upper limit for accel level %d") % 4)
        self.text_raster_accel_4.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: AccelBuild.__do_layout
        sizer_accel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Horizontal Raster")), wx.VERTICAL
        )
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Vertical Raster")), wx.VERTICAL
        )
        sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Vector")), wx.VERTICAL
        )
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8.Add(self.checkbox_vector_accel_enable, 0, 0, 0)
        label_2 = wx.StaticText(self, wx.ID_ANY, "1 <")
        sizer_9.Add(label_2, 1, 0, 0)
        sizer_9.Add(self.text_vector_accel_1, 1, 0, 0)
        label_3 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_9.Add(label_3, 1, 0, 0)
        sizer_8.Add(sizer_9, 1, wx.EXPAND, 0)
        label_4 = wx.StaticText(self, wx.ID_ANY, "2 <")
        sizer_10.Add(label_4, 1, 0, 0)
        sizer_10.Add(self.text_vector_accel_2, 1, 0, 0)
        label_5 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_10.Add(label_5, 1, 0, 0)
        sizer_8.Add(sizer_10, 1, wx.EXPAND, 0)
        label_6 = wx.StaticText(self, wx.ID_ANY, "3 <")
        sizer_11.Add(label_6, 1, 0, 0)
        sizer_11.Add(self.text_vector_accel_3, 1, 0, 0)
        label_7 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_11.Add(label_7, 1, 0, 0)
        sizer_8.Add(sizer_11, 1, wx.EXPAND, 0)
        label_8 = wx.StaticText(self, wx.ID_ANY, "4 <")
        sizer_12.Add(label_8, 1, 0, 0)
        sizer_12.Add(self.text_vector_accel_4, 1, 0, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_12.Add(label_13, 1, 0, 0)
        sizer_8.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_accel.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_16.Add(self.checkbox_vraster_accel_enable, 0, 0, 0)
        label_9 = wx.StaticText(self, wx.ID_ANY, "1 <")
        sizer_17.Add(label_9, 1, 0, 0)
        sizer_17.Add(self.text_vraster_accel_1, 1, 0, 0)
        label_10 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_17.Add(label_10, 1, 0, 0)
        sizer_16.Add(sizer_17, 1, wx.EXPAND, 0)
        label_11 = wx.StaticText(self, wx.ID_ANY, "2 <")
        sizer_20.Add(label_11, 1, 0, 0)
        sizer_20.Add(self.text_vraster_accel_2, 1, 0, 0)
        label_12 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_20.Add(label_12, 1, 0, 0)
        sizer_16.Add(sizer_20, 1, wx.EXPAND, 0)
        label_14 = wx.StaticText(self, wx.ID_ANY, "3 <")
        sizer_21.Add(label_14, 1, 0, 0)
        sizer_21.Add(self.text_vraster_accel_3, 1, 0, 0)
        label_23 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_21.Add(label_23, 1, 0, 0)
        sizer_16.Add(sizer_21, 1, wx.EXPAND, 0)
        label_24 = wx.StaticText(self, wx.ID_ANY, "4 <")
        sizer_22.Add(label_24, 1, 0, 0)
        sizer_22.Add(self.text_vraster_accel_4, 1, 0, 0)
        label_25 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_22.Add(label_25, 1, 0, 0)
        sizer_16.Add(sizer_22, 1, wx.EXPAND, 0)
        sizer_accel.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_13.Add(self.checkbox_raster_accel_enable, 0, 0, 0)
        label_15 = wx.StaticText(self, wx.ID_ANY, "1 <")
        sizer_14.Add(label_15, 1, 0, 0)
        sizer_14.Add(self.text_raster_accel_1, 1, 0, 0)
        label_16 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_14.Add(label_16, 1, 0, 0)
        sizer_13.Add(sizer_14, 1, wx.EXPAND, 0)
        label_17 = wx.StaticText(self, wx.ID_ANY, "2 <")
        sizer_15.Add(label_17, 1, 0, 0)
        sizer_15.Add(self.text_raster_accel_2, 1, 0, 0)
        label_18 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_15.Add(label_18, 1, 0, 0)
        sizer_13.Add(sizer_15, 1, wx.EXPAND, 0)
        label_19 = wx.StaticText(self, wx.ID_ANY, "3 <")
        sizer_18.Add(label_19, 1, 0, 0)
        sizer_18.Add(self.text_raster_accel_3, 1, 0, 0)
        label_20 = wx.StaticText(self, wx.ID_ANY, _("mm/s"))
        sizer_18.Add(label_20, 1, 0, 0)
        sizer_13.Add(sizer_18, 1, wx.EXPAND, 0)
        label_21 = wx.StaticText(self, wx.ID_ANY, "4 <")
        sizer_19.Add(label_21, 1, 0, 0)
        sizer_19.Add(self.text_raster_accel_4, 1, 0, 0)
        label_22 = wx.StaticText(self, wx.ID_ANY, "mm/s")
        sizer_19.Add(label_22, 1, 0, 0)
        sizer_13.Add(sizer_19, 1, wx.EXPAND, 0)
        sizer_accel.Add(sizer_13, 4, wx.EXPAND, 0)
        self.SetSizer(sizer_accel)
        self.Layout()
        # end wxGlade

    def set_widgets(self):
        context = self.context
        context.setting(bool, "raster_accel_table", False)
        context.setting(bool, "vraster_accel_table", False)
        context.setting(bool, "vector_accel_table", False)

        self.checkbox_raster_accel_enable.SetValue(context.vraster_accel_table)
        self.checkbox_raster_accel_enable.SetValue(context.raster_accel_table)
        self.checkbox_vector_accel_enable.SetValue(context.vector_accel_table)

    def window_open(self):
        # self.context.listen("pipe;buffer", self.on_buffer_update)
        self.context.listen("active", self.on_active_change)

    def window_close(self):
        # self.context.unlisten("pipe;buffer", self.on_buffer_update)
        self.context.unlisten("active", self.on_active_change)

    def on_active_change(self, origin, active):
        # self.Close()
        pass

    def on_check_vector_accel_enable(
        self, event=None
    ):  # wxGlade: LhystudiosDriver.<event_handler>

        self.context.vector_accel_table = self.checkbox_vector_accel_enable.GetValue()

    def on_text_vector_accel(self, event):  # wxGlade: LhystudiosDriver.<event_handler>
        pass

    def on_check_raster_accel_enable(
        self, event=None
    ):  # wxGlade: LhystudiosDriver.<event_handler>
        self.context.raster_accel_table = self.checkbox_raster_accel_enable.GetValue()

    def on_text_raster_accel(self, event):  # wxGlade: LhystudiosDriver.<event_handler>
        pass

    def on_check_vraster_accel_enable(
        self, event=None
    ):  # wxGlade: AccelBuild.<event_handler>
        self.context.vraster_accel_table = self.checkbox_vraster_accel_enable.GetValue()

    def on_text_vraster_accel(self, event):  # wxGlade: AccelBuild.<event_handler>
        pass
