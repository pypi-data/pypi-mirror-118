#
# Copyright 2019 Mycroft AI Inc.
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

import unittest
from lingua_nostra import load_language
from lingua_nostra.lang.parse_common import tokenize, Token
from lingua_nostra.parse import roman_to_int, is_roman_numeral,\
    extract_roman_numeral_spans, normalize_roman_numerals


class TestParseCommon(unittest.TestCase):
    def setUp(cls) -> None:
        load_language("en")

    def test_tokenize(self):
        self.assertEqual(tokenize('One small step for man'),
                         [Token('One', 0), Token('small', 1), Token('step', 2),
                          Token('for', 3), Token('man', 4)])

        self.assertEqual(tokenize('15%'),
                         [Token('15', 0), Token('%', 1)])

        self.assertEqual(tokenize('I am #1'),
                         [Token('I', 0), Token('am', 1), Token('#', 2),
                          Token('1', 3)])

        self.assertEqual(tokenize('hashtag #1world'),
                         [Token('hashtag', 0), Token('#1world', 1)])

    def test_roman(self):
        # valid numerals
        self.assertEqual(roman_to_int("III"), 3)
        self.assertEqual(roman_to_int("IV"), 4)
        self.assertEqual(roman_to_int("V"), 5)
        self.assertEqual(is_roman_numeral("IV"), True)

        # invalid numerals
        self.assertEqual(roman_to_int("v"), None)
        self.assertEqual(is_roman_numeral("ii"), False)
        self.assertEqual(is_roman_numeral("the IV century"), False)

        # test spans
        self.assertEqual(extract_roman_numeral_spans("the IV century"),
                         [(4, (4, 6))])
        self.assertEqual(extract_roman_numeral_spans("the XIV century"),
                         [(14, (4, 7))])

        # test normalization
        self.assertEqual(normalize_roman_numerals("the XV century"),
                         "the 15 century")

        # test ordinals
        self.assertEqual(normalize_roman_numerals("the XXI century",
                                                  ordinals=True),
                         "the 21st century")
        self.assertEqual(normalize_roman_numerals("the XII century",
                                                  ordinals=True),
                         "the 12nd century")
        self.assertEqual(normalize_roman_numerals("the XXIII century",
                                                  ordinals=True),
                         "the 23rd century")
        self.assertEqual(normalize_roman_numerals("the XXIV century",
                                                  ordinals=True),
                         "the 24th century")

        # test space
        self.assertEqual(is_roman_numeral("I V"), False)
        self.assertEqual(normalize_roman_numerals("the X V century"),
                         "the 10 5 century")
        self.assertEqual(extract_roman_numeral_spans("the X V century"),
                         [(10, (4, 5)),
                          (5, (6, 7))])

