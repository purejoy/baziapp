# -*- coding:utf-8 -*-
from django import forms
from widgets import SelectPicker, DateTimePicker

class BaziForm(forms.Form):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE,'男'), (GENDER_FEMALE, '女')]
    gender = forms.ChoiceField(
        label="性别",
        choices=GENDER_CHOICES,
        widget=SelectPicker(attrs={"id":"selectpicker1",},
                            icon_attrs={"class":"icon-parents",
                                        "0":"icon-user",
                                        "1":"icon-woman"},
                            options={"size":8,},))
    date = forms.DateField(
        label="出生日期",
        widget=DateTimePicker(attrs={"readonly":"",},
                              div_attrs={"class": "input-group date",
                                         "id":"datetimepicker1",},
                              options={"format": "YYYY-MM-DD",
                                       "locale": "zh-cn",
                                       "viewMode": "years",
                                       "showClose": True,
		                       "showTodayButton": True,
		                       "showClear": True,
                                       "ignoreReadonly": True,
                                       "minDate": "1800-01-01",
                                       "maxDate": "2100-01-01",
                                       "widgetPositioning": {'horizontal': 'left', 'vertical': 'bottom'},}))
    time = forms.TimeField(
        label="出生时间",
        widget=DateTimePicker(attrs={"readonly":"",},
                              div_attrs={"class": "input-group date",
                                         "id":"datetimepicker2",},
                              options={"format": "HH:mm",
                                       "ignoreReadonly": True,
                                       "showClose": True,
                                       "showClear": True},
                              icon_attrs={'class': 'glyphicon glyphicon-time',}))

    
'''
class ToDoForm(forms.Form):
    todo = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    date = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "orientation": "bottom left"}))
    reminder = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}))
'''

