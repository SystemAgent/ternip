#!/usr/bin/env python

import unittest
from ternip import timex
from ternip.rule_engine.normalisation_functions import *

class date_functions_Test(unittest.TestCase):
    
    def test_normalise_two_year_date_full(self):
        self.assertEquals('1989', normalise_two_digit_year('1989'))
    
    def test_normalise_two_year_date_full_just_year(self):
        self.assertEquals('1989', normalise_two_digit_year('19890101'))
    
    def test_normalise_two_year_date_apostrophe(self):
        self.assertEquals('1992', normalise_two_digit_year("'92"))
    
    def test_normalise_two_year_date_apostrophe_future(self):
        self.assertEquals('2018', normalise_two_digit_year("'18"))
    
    def test_normalise_two_year_date_two_year(self):
        self.assertEquals('1992', normalise_two_digit_year("92"))
    
    def test_normalise_two_year_date_two_year_future(self):
        self.assertEquals('2018', normalise_two_digit_year("18"))
    
    def test_normalise_two_year_date_first_millenium(self):
        self.assertEquals('0906', normalise_two_digit_year('906'))
    
    def test_easter_date_string(self):
        self.assertEquals('20100404', easter_date('2010'))
    
    def test_easter_date_int(self):
        self.assertEquals('20100404', easter_date(2010))
    
    def test_date_to_week(self):
        self.assertEquals('2010W31', date_to_week(2010, 8, 3))
    
    def test_date_to_dow_normal(self):
        self.assertEquals(2, date_to_dow(2010, 8, 3))
    
    def test_date_to_dow_wraparound(self):
        self.assertEquals(0, date_to_dow(2010, 8, 1))
    
    def test_nth_dow_to_date_normal(self):
        self.assertEquals(3, nth_dow_to_date(8, 2, 1, 2010))
    
    def test_nth_dow_to_date_special_case(self):
        self.assertEquals(8, nth_dow_to_date(8, 7, 2, 2010))
    
    def test_nth_dow_to_date_special_case2(self):
        self.assertEquals(12, nth_dow_to_date(7, 1, 2, 2010))

class string_conversions_Test(unittest.TestCase):
    
    def test_month_to_num_abbr(self):
        self.assertEquals(4, month_to_num('apr'))
    
    def test_month_to_num_full(self):
        self.assertEquals(4, month_to_num('April'))
    
    def test_month_to_num_mixed(self):
        self.assertEquals(6, month_to_num('JUNE'))
    
    def test_month_to_num_invalid(self):
        self.assertEquals(0, month_to_num('Frentober'))
    
    def test_day_to_num_full(self):
        self.assertEquals(0, day_to_num('sunday'))
    
    def test_month_to_num_mixed(self):
        self.assertEquals(5, day_to_num('FRIDAY'))
    
    def test_month_to_num_mixed(self):
        self.assertEquals(7, day_to_num('frankfurter'))
    
    def test_decade_num(self):
        self.assertEquals(9, decade_nums('nine'))
    
    def test_decade_num_mixed(self):
        self.assertEquals(8, decade_nums('EiGH'))
    
    def test_decade_num_bad(self):
        self.assertEquals(1, decade_nums('twenty-seven'))
    
    def test_season(self):
        self.assertEquals('SP', season('spring'))
    
    def test_season_mixed(self):
        self.assertEquals('WI', season('WINTER'))
    
    def test_season_bad(self):
        self.assertEquals('hunting', season('hunting'))
    
    def test_units_to_gran(self):
        self.assertEquals('D', units_to_gran('day'))
    
    def test_units_to_gran_mixed(self):
        self.assertEquals('C', units_to_gran('CENTURY'))
    
    def test_units_to_gran_bad(self):
        self.assertEquals('bad', units_to_gran('bad'))
    
    def test_fixed_holiday_date(self):
        self.assertEquals('1225', fixed_holiday_date('christmas'))
    
    def test_fixed_holiday_date_mixed(self):
        self.assertEquals('0423', fixed_holiday_date('<Saint~NNP><George~NNP>'))
    
    def test_fixed_holiday_date_bad(self):
        self.assertEquals('', fixed_holiday_date('bad'))
    
    def test_nth_dow_holiday_date(self):
        self.assertEquals((1, 1, 3), nth_dow_holiday_date('king'))
    
    def test_nth_dow_holiday_date_mixed(self):
        self.assertEquals((11, 4, 4), nth_dow_holiday_date('ThanksGiving'))
    
    def test_nth_dow_holiday_date_bad(self):
        self.assertEquals((0,0,0), nth_dow_holiday_date('bad'))

class words_to_num_Test(unittest.TestCase):
    
    def test_ordinal_number(self):
        self.assertEquals(6, ordinal_to_num('6th'))
    
    def test_ordinal_word(self):
        self.assertEquals(18, ordinal_to_num('eighteenth'))
    
    def test_ordinal_bad(self):
        self.assertEquals(1, ordinal_to_num('beefburger'))
    
    def test_words_to_num_simple(self):
        self.assertEquals(8, words_to_num("eight"))
    
    def test_words_to_num_none(self):
        self.assertEquals(0, words_to_num(None))
    
    def test_words_to_num_a(self):
        self.assertEquals(100, words_to_num('a hundred'))
    
    def test_words_to_num_the(self):
        self.assertEquals(6, words_to_num('the six'))
    
    def test_words_to_num_and(self):
        self.assertEquals(326, words_to_num('three hundred and twenty six'))
    
    def test_words_to_num_and(self):
        self.assertEquals(7320, words_to_num('seven thousand, three hundred and twenty'))
    
    def test_words_to_num_mixed(self):
        self.assertEquals(1806, words_to_num('18 hundred and six'))
    
    def test_words_to_num_mixed(self):
        self.assertEquals(324, words_to_num('324'))
    
    def test_words_to_num_mixed(self):
        self.assertEquals(0, words_to_num('six hundred and bread'))
    
    def test_words_to_num_ordinal(self):
        self.assertEquals(92, words_to_num('ninety second'))
    
    def test_words_to_num_bad_ordinal(self):
        self.assertEquals(0, words_to_num('first two'))

class relative_date_functions_Test(unittest.TestCase):
    
    def test_compute_offset_base_yesterday(self):
        self.assertEquals('20100803', compute_offset_base('20100804', 'Yesterday', 1))
        self.assertEquals('20100803', compute_offset_base('20100804', 'yesterday', -1))
    
    def test_compute_offset_base_tomorrow(self):
        self.assertEquals('20100805', compute_offset_base('20100804', 'tomORROW', -1))
        self.assertEquals('20100805', compute_offset_base('20100804', 'tomorrow', 1))
    
    def test_compute_offset_base_no_match(self):
        self.assertEquals('20100804', compute_offset_base('20100804', None, -1))
    
    def test_compute_offset_base_bad_day(self):
        self.assertEquals('20100804', compute_offset_base('20100804', 'nosuchday', -1))
    
    def test_compute_offset_base_last_day(self):
        self.assertEquals('20100730', compute_offset_base('20100804', 'Friday', -1))
        self.assertEquals('20100729', compute_offset_base('20100804', 'thursday', -1))
    
    def test_compute_offset_base_next_day(self):
        self.assertEquals('20100806', compute_offset_base('20100804', 'Friday', 1))
        self.assertEquals('20100810', compute_offset_base('20100804', 'tuesday', 1))
    
    def test_compute_offset_base_today(self):
        self.assertEquals('20100804', compute_offset_base('20100804', 'Wednesday', 1))
        self.assertEquals('20100804', compute_offset_base('20100804', 'Wednesday', -1))
    
    def test_offset_minute(self):
        self.assertEquals('20100804T1628', offset_from_date('20100804T163604', -8, 'TM'))
        self.assertEquals('20100804T1642', offset_from_date('20100804T1636', 6, 'TM'))
        self.assertEquals('20100804T1504', offset_from_date('20100804T1459', 5, 'TM'))
        self.assertEquals('20100804T1559', offset_from_date('20100804T1709', -70, 'TM'))
    
    def test_offset_hour(self):
        self.assertEquals('20100804T10', offset_from_date('20100804T1836', -8, 'TH'))
        self.assertEquals('20100804T1036', offset_from_date('20100804T1836', -8, 'TH', True))
        self.assertEquals('20100804T22', offset_from_date('20100804T1636', 6, 'TH'))
        self.assertEquals('20100805T06', offset_from_date('20100804T1859', 12, 'TH'))
        self.assertEquals('20100802T22', offset_from_date('20100804T0409', -30, 'TH'))
    
    def test_offset_day(self):
        self.assertEquals('20100401', offset_from_date('20100403T1443', -2))
        self.assertEquals('20100401T1443', offset_from_date('20100403T1443', -2, exact=True))
        self.assertEquals('20100401T14', offset_from_date('20100403T14', -2, exact=True))
        self.assertEquals('20100406', offset_from_date('20100403T1443', 3))
        self.assertEquals('20100403', offset_from_date('20100321T1443', 13))
        self.assertEquals('20080229', offset_from_date('20090301', -366, exact=True))
    
    def test_offset_week(self):
        self.assertEquals('2010W31', offset_from_date('20100820', -2, 'W'))
        self.assertEquals('20100806', offset_from_date('20100820', -2, 'W', True))
        self.assertEquals('2010W01', offset_from_date('20091225', 2, 'W'))
    
    def test_offset_fortnight(self):
        self.assertEquals('2010W29', offset_from_date('20100820', -2, 'F'))
        self.assertEquals('20100731', offset_from_date('20100828', -2, 'F', True))
        self.assertEquals('2010W03', offset_from_date('20091225', 2, 'F'))
    
    def test_offset_month(self):
        self.assertEquals('201006', offset_from_date('20100820', -2, 'M'))
        self.assertEquals('20100628', offset_from_date('20100828', -2, 'M', True))
        self.assertEquals('201004', offset_from_date('200810', 18, 'M'))
        self.assertEquals('20100228', offset_from_date('20100331', -1, 'M', True))
        self.assertEquals('200912', offset_from_date('20100110', -1, 'M'))
        self.assertEquals('20080229', offset_from_date('20100331', -25, 'M', True))
    
    def test_offset_year(self):
        self.assertEquals('1999', offset_from_date('20080812', -9, 'Y'))
        self.assertEquals('20090812', offset_from_date('20080812T1236', 1, 'Y', True))
        self.assertEquals('202008', offset_from_date('200808',12, 'Y', True))
        self.assertEquals('20080229', offset_from_date('20120229', -4, 'Y', True))
        self.assertEquals('20100228', offset_from_date('20120229', -2, 'Y', True))
    
    def test_offset_decade(self):
        self.assertEquals('199', offset_from_date('200908', -1, 'E'))
        self.assertEquals('19990812', offset_from_date('19890812T1236', 1, 'E', True))
    
    def test_offset_century(self):
        self.assertEquals('19', offset_from_date('200908', -1, 'C'))
        self.assertEquals('20990812', offset_from_date('19990812T1236', 1, 'C', True))
    
    def test_offset_generic(self):
        self.assertEquals('PAST_REF', offset_from_date('20100804T1432', -1, 'X'))
        self.assertEquals('FUTURE_REF', offset_from_date('20100804T1432', 1, 'X'))
        self.assertEquals('20100804T1432', offset_from_date('20100804T1432', 0, 'X'))