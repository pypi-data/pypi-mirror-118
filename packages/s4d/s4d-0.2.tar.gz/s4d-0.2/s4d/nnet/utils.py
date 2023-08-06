# -*- coding: utf-8 -*-
#
# This file is part of s4d.
#
# s4d is a python package for speaker diarization.
# Home page: http://www-lium.univ-lemans.fr/s4d/
#
# s4d is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# s4d is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with s4d.  If not, see <http://www.gnu.org/licenses/>.

"""
Copyright 2014-2021 Anthony Larcher, Théo Mariotte

"""

import itertools
import numpy


def multi_label_combination(output_idx, output_target, output_data, shift, output_rate, mode="mean"):
    """

    :param output_idx:
    :param output_target:
    :param output_data:
    :param shift:
    :param output_rate:
    :param mode:
    :return:

    Author: Anthony Larcher
    """
    win_shift = int(shift * output_rate)

    # Initialize the size of final_output
    final_output = numpy.zeros((win_shift * (len(output_data) - 1) + output_data[0].shape[0], output_data[0].shape[1]))

    final_target = numpy.zeros(win_shift * (len(output_data) - 1) + output_data[0].shape[0])
    overlaping_label_count = numpy.zeros(final_output.shape)

    win_len = output_data[0].shape[0]
    tmp = numpy.ones(output_data[0].shape)

    # Loop on the overlaping windows
    for idx, tmp_d in zip(output_idx, output_data):
        start_idx = win_shift * idx
        stop_idx = start_idx + win_len

        overlaping_label_count[start_idx: stop_idx, :] += tmp
        final_output[start_idx: stop_idx, :] += tmp_d

    # Divide by the number of overlapping values
    final_output /= overlaping_label_count

    if output_target is not None:
        for idx, tmp_t in zip(output_idx, output_target):
            start_idx = win_shift * idx
            stop_idx = start_idx + win_len
            final_target[start_idx: stop_idx] += tmp_t

        final_target /= overlaping_label_count[:, 0].squeeze()

    return final_output, final_target


def filter_vad(signal, th_in, th_out):
    """

    :param signal:
    :param th_in:
    :param th_out:
    :return:
    """
    speech = False
    prediction = numpy.zeros(signal.shape[0], dtype='bool')
    ii = 0
    while ii < signal.shape[0]:
        if signal[ii, 1] > th_in and not speech:
            speech = True
        elif signal[ii, 1] < th_out and speech:
            speech = False
        prediction[ii] = speech
        ii += 1
    return prediction


def filter_speaker_turn(signal, th, output_rate, min_durationi_spkt):
    """

    :param min_durationi_spkt:
    :param output_rate:
    :param th:
    :param signal:
    :return:
    """
    prediction = numpy.zeros(signal.shape[0], dtype='bool')

    order = max(1, int(round(output_rate * min_durationi_spkt, 0)))
    final_output = signal[:, 1].squeeze()
    idx_max = dsp.argrelmax(final_output, order=order)
    idx_max_th = [ii for ii in idx_max[0] if final_output[ii] > th]
    prediction[idx_max_th] = True

    return prediction


def filter_overlap(signal, th_in, th_out):
    """

    :param signal:
    :param th_in:
    :param th_out:
    :return:
    """
    prediction = numpy.zeros(signal.shape[0], dtype='bool')
    overlap = False
    ii = 0
    while ii < signal.shape[0]:
        if signal[ii, 1] > th_in and not overlap:
            overlap = True
        elif signal[ii, 1] < th_out and overlap:
            overlap = False
        prediction[ii] = overlap
        ii += 1

    return prediction


def create_rttm(output_filename, data, show, min_on=0.5, min_off=1):
    """

    :param output_filename:
    :param data:
    :param show:
    :param min_on:
    :param min_off:
    :return:
    """
    with open(output_filename, 'w') as fh:
        ts = 0.01
        curr_time = 0

        grouped = [(x, len(list(y))) for x, y in itertools.groupby(data)]
        first_clean = []
        for x in grouped:
            if x[0] == 0 and x[1] > min_off / ts:
                first_clean.append(x)
            else:
                first_clean.append((1, x[1]))
        expanded_list = list(itertools.chain.from_iterable([[x] * y for x, y in first_clean]))
        grouped2 = [(x, len(list(y))) for x, y in itertools.groupby(expanded_list)]
        second_clean = []
        for x in grouped2:
            if x[0] == 1 and x[1] > min_on / ts:
                second_clean.append(x)
            else:
                first_clean.append((0, x[1]))
        expanded_list2 = list(itertools.chain.from_iterable([[x] * y for x, y in first_clean]))
        grouped3 = [(x, len(list(y))) for x, y in itertools.groupby(expanded_list)]
        for turn in grouped3:
            if turn[0] == 1:
                start = curr_time
                curr_time += (turn[1] * ts)
                stop = turn[1] * ts
                rttm = f"SPEAKER {show} 1 {start:.2f} {stop:.2f} <NA> <NA> OVER <NA> <NA>"
                fh.write(rttm + '\n')
            else:
                curr_time += (turn[1] * ts)

        fh.close()
