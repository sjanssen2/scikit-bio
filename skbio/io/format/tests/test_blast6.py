# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from six import assertRaisesRegex

import unittest

import pandas as pd
import numpy as np

from skbio.util import get_data_path, assert_data_frame_almost_equal
from skbio.io.format.blast6 import _blast6_to_data_frame
from skbio.io import BLAST6FormatError


class TestBlast6Reader(unittest.TestCase):
    def test_default_valid_single_line(self):
        fp = get_data_path('blast6_default_single_line')
        df = _blast6_to_data_frame(fp, default_columns=True)
        exp = pd.DataFrame([['query1', 'subject2', 75.0, 8.0, 2.0, 0.0, 1.0,
                             8.0, 2.0, 9.0, 0.06, 11.5]],
                           columns=['qseqid', 'sseqid', 'pident', 'length',
                                    'mismatch', 'gapopen', 'qstart', 'qend',
                                    'sstart', 'send', 'evalue', 'bitscore'])
        assert_data_frame_almost_equal(df, exp)

    def test_default_valid_multi_line(self):
        fp = get_data_path('blast6_default_multi_line')
        df = _blast6_to_data_frame(fp, default_columns=True)
        exp = pd.DataFrame([['query1', 'subject2', 100.00, 8.0, 0.0, 0.0, 1.0,
                             8.0, 3.0, 10.0, 9e-05, 16.9],
                            ['query1', 'subject2', 75.00, 8.0, 2.0, 0.0, 1.0,
                             8.0, 2.0, 9.0, 0.060, 11.5],
                            ['query2', 'subject1', 71.43, 7.0, 2.0, 0.0, 1.0,
                            7.0, 1.0, 7.0, 0.044, 11.9]],
                           columns=['qseqid', 'sseqid', 'pident', 'length',
                                    'mismatch', 'gapopen', 'qstart', 'qend',
                                    'sstart', 'send', 'evalue', 'bitscore'])
        assert_data_frame_almost_equal(df, exp)

    def test_custom_valid_single_line(self):
        fp = get_data_path('blast6_custom_single_line')
        df = _blast6_to_data_frame(fp, columns=['qacc', 'qseq', 'btop',
                                                'sframe', 'ppos',
                                                'positive', 'gaps'])
        exp = pd.DataFrame([['query1', 'PAAWWWWW', 8.0, 1.0, 100.00, 8.0,
                             0.0]], columns=['qacc', 'qseq', 'btop', 'sframe',
                                             'ppos', 'positive', 'gaps'])
        assert_data_frame_almost_equal(df, exp)

    def test_custom_valid_multi_line(self):
        fp = get_data_path('blast6_custom_multi_line')
        df = _blast6_to_data_frame(fp, columns=['sacc', 'score', 'gapopen',
                                                'qcovs', 'sblastnames',
                                                'sallacc', 'qaccver'])
        exp = pd.DataFrame([['subject2', 32.0, 0.0, 100.0, np.nan, 'subject2',
                             'query1'], ['subject2', 18.0, 0.0, 100.0, np.nan,
                                         'subject2', 'query1'],
                            ['subject1', 19.0, 0.0, 70.0, np.nan, 'subject1',
                             'query2']], columns=['sacc', 'score', 'gapopen',
                                                  'qcovs', 'sblastnames',
                                                  'sallacc', 'qaccver'])
        exp['sblastnames'] = exp['sblastnames'].astype(object)
        assert_data_frame_almost_equal(df, exp)

    def test_valid_nan_handling(self):
        fp = get_data_path('blast6_custom_mixed_nans')
        df = _blast6_to_data_frame(fp, columns=['qacc', 'qseq', 'btop',
                                                'sframe', 'ppos', 'positive',
                                                'gaps'])
        exp = pd.DataFrame([[np.nan, 'PAAWWWWW', 8.0, 1.0, 100.00, np.nan,
                             0.0], ['query1', np.nan, 8.0, 1.0, np.nan, 8.0,
                                    0.0]], columns=['qacc', 'qseq', 'btop',
                                                    'sframe', 'ppos',
                                                    'positive', 'gaps'])
        assert_data_frame_almost_equal(df, exp)

    def test_valid_minimal(self):
        fp = get_data_path('blast6_custom_minimal')
        df = _blast6_to_data_frame(fp, columns=['sacc'])
        exp = pd.DataFrame([['subject2']], columns=['sacc'])
        assert_data_frame_almost_equal(df, exp)

    def test_custom_and_default_passed_error(self):
        fp = get_data_path('blast6_default_single_line')
        with assertRaisesRegex(self, ValueError,
                               "`columns` and `default_columns`"):
            _blast6_to_data_frame(fp, columns=['qseqid'], default_columns=True)

    def test_no_columns_passed_error(self):
        fp = get_data_path('blast6_default_single_line')
        with assertRaisesRegex(self, ValueError,
                               "Either `columns` or `default_columns`"):
            _blast6_to_data_frame(fp)

    def test_wrong_amount_of_columns_error(self):
        fp = get_data_path('blast6_invalid_number_of_columns')
        with assertRaisesRegex(self, BLAST6FormatError,
                               "The specified number of columns"):
            _blast6_to_data_frame(fp, default_columns=True)

    def test_wrong_column_name_error(self):
        fp = get_data_path('blast6_default_single_line')
        with assertRaisesRegex(self, ValueError,
                               "The valid column names are"):
            _blast6_to_data_frame(fp, columns=['qseqid', 'sseqid', 'pident',
                                               'length', 'mismatch', 'gapopen',
                                               'qstart', 'qend', 'sstart',
                                               'send', 'abcd', 'bitscore'])

if __name__ == '__main__':
    unittest.main()
