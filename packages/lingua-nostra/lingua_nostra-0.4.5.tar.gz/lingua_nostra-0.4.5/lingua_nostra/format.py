# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import datetime
import json
import os
import re
from collections import namedtuple
from os.path import join
from warnings import warn

from quantulum3 import parser as quantity_parser

from lingua_nostra.bracket_expansion import SentenceTreeParser
from lingua_nostra.internal import localized_function, \
    populate_localized_function_dict, get_active_langs, \
    get_full_lang_code, get_default_loc, \
    is_supported_full_lang, UnsupportedLanguageError, NoneLangWarning, \
    InvalidLangWarning, \
    FunctionNotLocalizedError, get_primary_lang_code
from lingua_nostra.time import now_local

_REGISTERED_FUNCTIONS = ("nice_number",
                         "nice_time",
                         "pronounce_number",
                         "pronounce_digits",
                         "nice_response",
                         "nice_duration")

populate_localized_function_dict("format", langs=get_active_langs())


@localized_function(run_own_code_on=[FunctionNotLocalizedError])
def nice_units(utterance=None, lang=''):
    """  Format a unit to a pronouncable string
    Args:
        unit (string): The unit abbreviation that is to be pronounced
            (i.e. "C", "MW", "mW", "°F" etc)
        utterance (string): A text in which the correct meaning of this
            abbreviation becomes clear (i.e. "It's almost 30 C outside")
            If given, the whole context will be parsed and the first unit
            to be found returned
        lang (string): the language to use, use Mycroft default language if
            not provided
    Returns:
        (str): A fully de-abbreviated unit for insertion in a context like
                situation (i.e. "degree Celsius", "percent")
        (object): The parsed value of the quantity, if any (else None)
    """
    lang = get_primary_lang_code(lang)
    pronounced_units = []

    try:
        quants = quantity_parser.parse(utterance, lang)
        if not quants:
            # Quantulum expects a unit to be prefixed with a quantifier
            quants = quantity_parser.parse(f"1 {utterance}", lang)
        for q in quants:
            pronounced_units.append(str(q))
    except NotImplementedError:
        raise FunctionNotLocalizedError

    return pronounced_units


@localized_function(run_own_code_on=[FunctionNotLocalizedError])
def expand_units(text, lang=""):
    """
        Format all units in a text and their amount into pronouncable strings
        Args:
            text (string): A text, ideally containing compact units
                            (i.e. "It's almost 30 C outside")
            lang (string): the language to use, use Mycroft default language if
                not provided
        Returns:
            (str): A text with fully de-abbreviated units
    """
    lang = get_primary_lang_code(lang)
    try:
        return quantity_parser.inline_parse_and_expand(text, lang)
    except NotImplementedError:
        return text


def _translate_word(name, lang=''):
    """ Helper to get word translations

    Args:
        name (str): Word name. Returned as the default value if not translated
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.

    Returns:
        str: translated version of resource name
    """
    from lingua_nostra.internal import resolve_resource_file
    if not lang:
        if lang is None:
            warn(NoneLangWarning)
        lang = get_default_loc()

    lang_code = lang if is_supported_full_lang(lang) else \
        get_full_lang_code(lang)

    filename = resolve_resource_file(join("text", lang_code, name + ".word"))
    if filename:
        # open the file
        try:
            with open(filename, 'r', encoding='utf8') as f:
                for line in f:
                    word = line.strip()
                    if word.startswith("#"):
                        continue  # skip comment lines
                    return word
        except Exception:
            pass
    return name  # use resource name as the word


NUMBER_TUPLE = namedtuple(
    'number',
    ('x, xx, x0, x_in_x0, xxx, x00, x_in_x00, xx00, xx_in_xx00, x000, ' +
     'x_in_x000, x0_in_x000, x_in_0x00'))


class DateTimeFormat:
    def __init__(self, config_path):
        self.lang_config = {}
        self.config_path = config_path

    def cache(self, lang):
        if lang not in self.lang_config:
            try:
                # Attempt to load the language-specific formatting data
                with open(self.config_path + '/' + lang + '/date_time.json',
                          'r', encoding='utf8') as lang_config_file:
                    self.lang_config[lang] = json.loads(
                        lang_config_file.read())
            except FileNotFoundError:
                # Fallback to English formatting
                with open(self.config_path + '/en-us/date_time.json',
                          'r') as lang_config_file:
                    self.lang_config[lang] = json.loads(
                        lang_config_file.read())

            for x in ['decade_format', 'hundreds_format', 'thousand_format',
                      'year_format']:
                i = 1
                while self.lang_config[lang][x].get(str(i)):
                    self.lang_config[lang][x][str(i)]['re'] = (
                        re.compile(self.lang_config[lang][x][str(i)]['match']
                                   ))
                    i = i + 1

    def _number_strings(self, number, lang):
        x = (self.lang_config[lang]['number'].get(str(number % 10)) or
             str(number % 10))
        xx = (self.lang_config[lang]['number'].get(str(number % 100)) or
              str(number % 100))
        x_in_x0 = self.lang_config[lang]['number'].get(
            str(int(number % 100 / 10))) or str(int(number % 100 / 10))
        x0 = (self.lang_config[lang]['number'].get(
            str(int(number % 100 / 10) * 10)) or
              str(int(number % 100 / 10) * 10))
        xxx = (self.lang_config[lang]['number'].get(str(number % 1000)) or
               str(number % 1000))
        x00 = (self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100) * 100)) or
               str(int(number % 1000 / 100) * 100))
        x_in_x00 = self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100))) or str(int(number % 1000 / 100))
        xx00 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 100) * 100)) or str(int(number % 10000 / 100) *
                                                 100)
        xx_in_xx00 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 100))) or str(int(number % 10000 / 100))
        x000 = (self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000) * 1000)) or
                str(int(number % 10000 / 1000) * 1000))
        x_in_x000 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000))) or str(int(number % 10000 / 1000))
        x0_in_x000 = self.lang_config[lang]['number'].get(str(int(
            number % 10000 / 1000) * 10)) or str(
            int(number % 10000 / 1000) * 10)
        x_in_0x00 = self.lang_config[lang]['number'].get(str(int(
            number % 1000 / 100)) or str(int(number % 1000 / 100)))

        return NUMBER_TUPLE(
            x, xx, x0, x_in_x0, xxx, x00, x_in_x00, xx00, xx_in_xx00, x000,
            x_in_x000, x0_in_x000, x_in_0x00)

    def _format_string(self, number, format_section, lang):
        s = self.lang_config[lang][format_section]['default']
        i = 1
        while self.lang_config[lang][format_section].get(str(i)):
            e = self.lang_config[lang][format_section][str(i)]
            if e['re'].match(str(number)):
                return e['format']
            i = i + 1
        return s

    def _decade_format(self, number, number_tuple, lang):
        s = self._format_string(number % 100, 'decade_format', lang)
        return s.format(x=number_tuple.x, xx=number_tuple.xx,
                        x0=number_tuple.x0, x_in_x0=number_tuple.x_in_x0,
                        number=str(number % 100))

    def _number_format_hundreds(self, number, number_tuple, lang,
                                formatted_decade):
        s = self._format_string(number % 1000, 'hundreds_format', lang)
        return s.format(xxx=number_tuple.xxx, x00=number_tuple.x00,
                        x_in_x00=number_tuple.x_in_x00,
                        formatted_decade=formatted_decade,
                        number=str(number % 1000))

    def _number_format_thousand(self, number, number_tuple, lang,
                                formatted_decade, formatted_hundreds):
        s = self._format_string(number % 10000, 'thousand_format', lang)
        return s.format(x_in_x00=number_tuple.x_in_x00,
                        xx00=number_tuple.xx00,
                        xx_in_xx00=number_tuple.xx_in_xx00,
                        x000=number_tuple.x000,
                        x_in_x000=number_tuple.x_in_x000,
                        x0_in_x000=number_tuple.x0_in_x000,
                        x_in_0x00=number_tuple.x_in_0x00,
                        formatted_decade=formatted_decade,
                        formatted_hundreds=formatted_hundreds,
                        number=str(number % 10000))

    def date_format(self, dt, lang, now):
        format_str = 'date_full'
        if now:
            if dt.year == now.year:
                format_str = 'date_full_no_year'
                if dt.month == now.month and dt.day > now.day:
                    format_str = 'date_full_no_year_month'

            tomorrow = now + datetime.timedelta(days=1)
            yesterday = now - datetime.timedelta(days=1)
            if tomorrow.date() == dt.date():
                format_str = 'tomorrow'
            elif now.date() == dt.date():
                format_str = 'today'
            elif yesterday.date() == dt.date():
                format_str = 'yesterday'

        return self.lang_config[lang]['date_format'][format_str].format(
            weekday=self.lang_config[lang]['weekday'][str(dt.weekday())],
            month=self.lang_config[lang]['month'][str(dt.month)],
            day=self.lang_config[lang]['date'][str(dt.day)],
            formatted_year=self.year_format(dt, lang, False))

    def date_time_format(self, dt, lang, now, use_24hour, use_ampm):
        date_str = self.date_format(dt, lang, now)
        time_str = nice_time(dt, lang, use_24hour=use_24hour,
                             use_ampm=use_ampm)
        return self.lang_config[lang]['date_time_format']['date_time'].format(
            formatted_date=date_str, formatted_time=time_str)

    def year_format(self, dt, lang, bc):
        number_tuple = self._number_strings(dt.year, lang)
        formatted_bc = (
            self.lang_config[lang]['year_format']['bc'] if bc else '')
        formatted_decade = self._decade_format(
            dt.year, number_tuple, lang)
        formatted_hundreds = self._number_format_hundreds(
            dt.year, number_tuple, lang, formatted_decade)
        formatted_thousand = self._number_format_thousand(
            dt.year, number_tuple, lang, formatted_decade, formatted_hundreds)

        s = self._format_string(dt.year, 'year_format', lang)

        return re.sub(' +', ' ',
                      s.format(
                          year=str(dt.year),
                          century=str(int(dt.year / 100)),
                          decade=str(dt.year % 100),
                          formatted_hundreds=formatted_hundreds,
                          formatted_decade=formatted_decade,
                          formatted_thousand=formatted_thousand,
                          bc=formatted_bc)).strip()


date_time_format = DateTimeFormat(os.path.join(os.path.dirname(__file__),
                                               'res/text'))


@localized_function(run_own_code_on=[UnsupportedLanguageError])
def nice_number(number, lang='', speech=True, denominators=None):
    """Format a float to human readable functions

    This function formats a float to human understandable functions. Like
    4.5 becomes 4 and a half for speech and 4 1/2 for text
    Args:
        number (int or float): the float to format
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    return str(number)


@localized_function()
def nice_time(dt, lang='', speech=True, use_24hour=False,
              use_ampm=False, variant=None):
    """
    Format a time to a comfortable human format

    For example, generate 'five thirty' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        speech (bool): format for speech (default/True) or display (False)
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
        variant (string): alternative time system to be used, string must
                          match language specific mappings
    Returns:
        (str): The formatted time string
    """


@localized_function()
def pronounce_number(number, lang='', places=2, short_scale=True,
                     scientific=False, ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5' would be 'five'

    Args:
        number: the number to pronounce
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        places (int): number of decimal places to express, default 2
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool) : convert and pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """


@localized_function()
def pronounce_digits(number, lang=None, places=2, all_digits=False):
    """
    Pronounce a number's digits, either colloquially or in full
    In English, the colloquial way is usually to read two digits at a time,
    treating each pair as a single number.
    Examples:
        >>> pronounce_number(127, all_digits=False)
        'one twenty seven'
        >>> pronounce_number(127, all_digits=True)
        'one two seven'
    Args:
        number (int|float)
        all_digits (bool): read every digit, rather than two digits at a time
    """


def nice_date(dt, lang='', now=None):
    """
    Format a datetime to a pronounceable date

    For example, generates 'tuesday, june the fifth, 2018'

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        now (datetime): Current date. If provided, the returned date for speech
            will be shortened accordingly: No year is returned if now is in the
            same year as td, no month is returned if now is in the same month
            as td. If now and td is the same day, 'today' is returned.

    Returns:
        (str): The formatted date string
    """
    full_code = get_full_lang_code(lang)
    date_time_format.cache(full_code)

    return date_time_format.date_format(dt, full_code, now)


def nice_date_time(dt, lang='', now=None, use_24hour=False,
                   use_ampm=False):
    """
        Format a datetime to a pronounceable date and time

        For example, generate 'tuesday, june the fifth, 2018 at five thirty'

        Args:
            dt (datetime): date to format (assumes already in local timezone)
            lang (str, optional): an optional BCP-47 language code, if omitted
                                  the default language will be used.
            now (datetime): Current date. If provided, the returned date for
                speech will be shortened accordingly: No year is returned if
                now is in the same year as td, no month is returned if now is
                in the same month as td. If now and td is the same day, 'today'
                is returned.
            use_24hour (bool): output in 24-hour/military or 12-hour format
            use_ampm (bool): include the am/pm for 12-hour format
        Returns:
            (str): The formatted date time string
    """

    full_code = get_full_lang_code(lang)
    date_time_format.cache(full_code)

    return date_time_format.date_time_format(dt, full_code, now, use_24hour,
                                             use_ampm)


def nice_day(dt, date_format='MDY', include_month=True, lang=""):
    if include_month:
        month = nice_month(dt, date_format, lang)
        if date_format == 'MDY':
            return "{} {}".format(month, dt.strftime("%d"))
        else:
            return "{} {}".format(dt.strftime("%d"), month)
    return dt.strftime("%d")


def nice_weekday(dt, lang=""):
    if lang in date_time_format.lang_config.keys():
        localized_day_names = list(
            date_time_format.lang_config[lang]['weekday'].values())
        weekday = localized_day_names[dt.weekday()]
    else:
        weekday = dt.strftime("%A")
    return weekday.capitalize()


def nice_month(dt, date_format='MDY', lang=""):
    if lang in date_time_format.lang_config.keys():
        localized_month_names = date_time_format.lang_config[lang]['month']
        month = localized_month_names[str(int(dt.strftime("%m")))]
    else:
        month = dt.strftime("%B")
    return month.capitalize()


def nice_year(dt, lang='', bc=False):
    """
        Format a datetime to a pronounceable year

        For example, generate 'nineteen-hundred and eighty-four' for year 1984

        Args:
            dt (datetime): date to format (assumes already in local timezone)
            lang (str, optional): an optional BCP-47 language code, if omitted
                                  the default language will be used.
            bc (bool) pust B.C. after the year (python does not support dates
                B.C. in datetime)
        Returns:
            (str): The formatted year string
    """

    full_code = get_full_lang_code(lang)
    date_time_format.cache(full_code)

    return date_time_format.year_format(dt, full_code, bc)


def get_date_strings(dt=None, date_format='MDY', time_format="full", lang=""):
    lang = get_primary_lang_code(lang)
    dt = dt or now_local()
    timestr = nice_time(dt, lang, speech=False,
                         use_24hour=time_format == "full")
    monthstr = nice_month(dt, date_format, lang)
    weekdaystr = nice_weekday(dt, lang)
    yearstr = dt.strftime("%Y")
    daystr = nice_day(dt, date_format, include_month=False, lang=lang)
    if date_format == 'MDY':
        return {
            "date_string": dt.strftime("%-m/%-d/%Y"),
            "time_string": timestr,
            "month_string": monthstr,
            "day_string": daystr,
            'year_string': yearstr,
            "weekday_string": weekdaystr
        }
    else:
        return {
            "date_string": dt.strftime("%Y/%-d/%-m"),
            "time_string": timestr,
            "month_string": monthstr,
            "day_string": daystr,
            'year_string': yearstr,
            "weekday_string": weekdaystr
        }


@localized_function(run_own_code_on=[FunctionNotLocalizedError])
def nice_duration(duration, lang='', speech=True):
    """ Convert duration in seconds to a nice spoken timespan

    Examples:
       duration = 60  ->  "1:00" or "one minute"
       duration = 163  ->  "2:43" or "two minutes forty three seconds"

    Args:
        duration: time, in seconds
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        speech (bool): format for speech (True) or display (False)

    Returns:
        str: timespan as a string
    """
    if not lang:
        if lang is None:
            warn(NoneLangWarning)
        lang = get_default_loc()
    if not is_supported_full_lang(lang):
        # TODO deprecated; delete when 'lang=None' and 'lang=invalid' are
        # removed
        try:
            lang = get_full_lang_code(lang)
        except UnsupportedLanguageError:
            warn(InvalidLangWarning)
            lang = get_default_loc()

    if isinstance(duration, datetime.timedelta):
        duration = duration.total_seconds()

    # Do traditional rounding: 2.5->3, 3.5->4, plus this
    # helps in a few cases of where calculations generate
    # times like 2:59:59.9 instead of 3:00.
    duration += 0.5

    days = int(duration // 86400)
    hours = int(duration // 3600 % 24)
    minutes = int(duration // 60 % 60)
    seconds = int(duration % 60)

    if speech:
        out = ""
        if days > 0:
            out += pronounce_number(days, lang) + " "
            if days == 1:
                out += _translate_word("day", lang)
            else:
                out += _translate_word("days", lang)
            out += " "
        if hours > 0:
            if out:
                out += " "
            out += pronounce_number(hours, lang) + " "
            if hours == 1:
                out += _translate_word("hour", lang)
            else:
                out += _translate_word("hours", lang)
        if minutes > 0:
            if out:
                out += " "
            out += pronounce_number(minutes, lang) + " "
            if minutes == 1:
                out += _translate_word("minute", lang)
            else:
                out += _translate_word("minutes", lang)
        if seconds > 0:
            if out:
                out += " "
            out += pronounce_number(seconds, lang) + " "
            if seconds == 1:
                out += _translate_word("second", lang)
            else:
                out += _translate_word("seconds", lang)
    else:
        # M:SS, MM:SS, H:MM:SS, Dd H:MM:SS format
        out = ""
        if days > 0:
            out = str(days) + "d "
        if hours > 0 or days > 0:
            out += str(hours) + ":"
        if minutes < 10 and (hours > 0 or days > 0):
            out += "0"
        out += str(minutes) + ":"
        if seconds < 10:
            out += "0"
        out += str(seconds)

    return out


def join_list(items, connector, sep=None, lang=''):
    """ Join a list into a phrase using the given connector word

    Examples:
        join_list([1,2,3], "and") ->  "1, 2 and 3"
        join_list([1,2,3], "and", ";") ->  "1; 2 and 3"

    Args:
        items (array): items to be joined
        connector (str): connecting word (resource name), like "and" or "or"
        sep (str, optional): separator character, default = ","
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        str: the connected list phrase
    """

    if not items:
        return ""
    if len(items) == 1:
        return str(items[0])

    if not sep:
        sep = ", "
    else:
        sep += " "
    return (sep.join(str(item) for item in items[:-1]) +
            " " + _translate_word(connector, lang) +
            " " + items[-1])


def expand_parentheses(sent):
    """
    ['1', '(', '2', '|', '3, ')'] -> [['1', '2'], ['1', '3']]
    For example:
    Will it (rain|pour) (today|tomorrow|)?
    ---->
    Will it rain today?
    Will it rain tomorrow?
    Will it rain?
    Will it pour today?
    Will it pour tomorrow?
    Will it pour?

    Args:
        sent (list<str>): List of tokens in sentence

    Returns:
        list<list<str>>: Multiple possible sentences from original
    """
    return SentenceTreeParser(sent).expand_parentheses()


def expand_options(parentheses_line: str) -> list:
    """
    Convert 'test (a|b)' -> ['test a', 'test b']

    Args:
        parentheses_line: Input line to expand

    Returns:
        List of expanded possibilities
    """
    # 'a(this|that)b' -> [['a', 'this', 'b'], ['a', 'that', 'b']]
    options = expand_parentheses(re.split(r'([(|)])', parentheses_line))
    return [re.sub(r'\s+', ' ', ' '.join(i)).strip() for i in options]


@localized_function()
def nice_response(text, lang=''):
    """
    In some languages, sanitizes certain numeric input for TTS

    Most of the time, this function will be called by any formatters
    which might need it. It's exposed here just in case you've got a clever
    use.

    As of July 2020, this function sanitizes some dates and "x ^ y"-formatted
    exponents in the following primary language codes:
      da de nl sv

    Args:
        text (str): input text to sanitize
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.

    Example:
        assertEqual(nice_response_de("dies ist der 31. mai"),
                         "dies ist der einunddreißigste mai")

        assertEqual(nice_response_de("10 ^ 2"),
                         "10 hoch 2")
    """


@localized_function(run_own_code_on=[FunctionNotLocalizedError])
def nice_bytes(number, lang='', speech=True, binary=True, gnu=False):
    """
    turns a number of bytes into a string using appropriate units
    prefixes - https://en.wikipedia.org/wiki/Binary_prefix
    spoken binary units - https://en.wikipedia.org/wiki/Kibibyte
    implementation - http://stackoverflow.com/a/1094933/2444609
    :param number: number of bytes (int)
    :param lang: lang_code, ignored for now (str)
    :param speech: spoken form (True) or short units (False)
    :param binary: 1 kilobyte = 1024 bytes (True) or 1 kilobyte = 1000 bytes (False)
    :param gnu: say only order of magnitude (bool)  - 100 Kilo (True) or 100 Kilobytes (False)
    :return: nice bytes (str)
    """
    if speech and gnu:
        default_units = ['Bytes', 'Kilo', 'Mega', 'Giga', 'Tera', 'Peta',
                         'Exa', 'Zetta', 'Yotta']
    elif speech and binary:
        default_units = ['Bytes', 'Kibibytes', 'Mebibytes', 'Gibibytes',
                         'Tebibytes', 'Pebibytes', 'Exbibytes', 'Zebibytes',
                         'Yobibytes']
    elif speech:
        default_units = ['Bytes', 'Kilobytes', 'Megabytes', 'Gigabytes',
                         'Terabytes', 'Petabytes', 'Exabytes', 'Zettabytes',
                         'Yottabytes']
    elif gnu:
        default_units = ['B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    elif binary:
        default_units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB',
                         'YiB']
    else:
        default_units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    units = default_units

    if binary:
        n = 1024
    else:
        n = 1000

    for unit in units[:-1]:
        if abs(number) < n:
            if number == 1 and speech and not gnu:
                # strip final "s"
                unit = unit[:-1]
            return "%3.1f %s" % (number, unit)
        number /= n
    return "%.1f %s" % (number, units[-1])
