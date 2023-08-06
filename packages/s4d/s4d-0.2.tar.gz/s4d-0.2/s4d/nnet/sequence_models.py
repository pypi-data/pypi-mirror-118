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
Copyright 2014-2021 Anthony Larcher & Martin Lebourdais & Theo Mariotte

"""

import numpy
import torch
import torchaudio

from .sequence_sets import SeqSetSingle
from .utils import multi_label_combination
from .utils import filter_vad
from .utils import filter_speaker_turn
from .utils import filter_overlap
from collections import OrderedDict
from torch.utils.data import DataLoader

__license__ = "LGPL"
__author__ = "Theo Mariotte & Anthony Larcher"
__copyright__ = "Copyright 2015-2021 Anthony Larcher"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'


class Deltas(torch.nn.Module):
    """
    Class to add deltas and delta deltas
    """
    def __init__(self,
                 e=False,
                 d=False,
                 de=True,
                 dd=False,
                 dde=True):
        """
        :param e : energy
        :param d : first delta
        :param de : delta energy
        :param dd : delta delta
        :param dde : delta delta energy
        """
        super(Deltas,self).__init__()
        self.e = e
        self.d = d
        self.dd = dd
        #if self.d or self.dd:
        self.delta = torchaudio.transforms.ComputeDeltas()

    def forward(self,coefs):
        coefs = coefs.squeeze(dim=1)
        out=coefs
        #Caculation
        if self.d:
            delt = self.delta(coefs)
        if self.dd:
            delt2 = self.delta(delt)

        #concat
        if not self.e:
            coefs = coefs[:,1:,:]
            out=coefs
        if self.d:
            out = torch.cat((out,delt),dim=1)
        if self.dd:
            out = torch.cat((out,delt2),dim=1)
        return out


class BLSTM(torch.nn.Module):
    """
    Bi LSTM model used for voice activity detection, speaker turn detection, overlap detection and resegmentation
    """
    def __init__(self,
                 input_size,
                 blstm_sizes,
                 num_layers):
        """

        :param input_size:
        :param blstm_sizes:
        """
        super(BLSTM, self).__init__()
        self.input_size = input_size
        self.blstm_sizes = blstm_sizes
        self.output_size = blstm_sizes * 2

        self.blstm_layers = torch.nn.LSTM(input_size,
                                          blstm_sizes,
                                          bidirectional=True,
                                          batch_first=True,
                                          num_layers=num_layers)

    def forward(self, inputs):
        """

        :param inputs:
        :return:
        """
        output, h = self.blstm_layers(inputs)
        return output

    def output_size(self):
        """

        :return:
        """
        return self.output_size


def _init_weights(m):
    """

    :return:
    """
    if type(m) == torch.nn.Linear:
        torch.nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.01)


class SeqToSeq(torch.nn.Module):
    """
    Sequence-To-Sequence model for speech segmentation tasks (VAD, speaker turn detection, overlapped speech detection)
    This model is composed of three main blocks :
        - features extraction : extract audio features from raw audio waveform
        - recurrent layers : reccurent neural network implemented using LSTM (bi-directionnal)
        - MLP : linear layers to project BLSTM outputs to classification domain
    """
    def __init__(self,model_archi):
        """

        :param model_archi: architecture of the model as dictionnary (can be extracted from YAML file)
        """
        super(SeqToSeq, self).__init__()

        cfg = model_archi

        # Get Feature size
        self.feature_size = cfg["feature_size"]
        self.samplerate = cfg["samplerate"]
        self.channel_number = cfg["channel_number"]

        # pre-processing layers
        pre_processing_layers = []
        for k in cfg["pre_processing"].keys():

            if k.startswith("mfcc"):
                n_fft = cfg["pre_processing"][k]["n_fft"]
                win_length = cfg["pre_processing"][k].get("win_length",480)
                hop_length = cfg["pre_processing"][k]["win_shift"]
                n_mels = cfg["pre_processing"][k]["n_mels"]
                n_mfcc = cfg["pre_processing"][k]["n_mfcc"]
                delta = cfg["pre_processing"][k]["delta"]
                delta2 = cfg["pre_processing"][k]["delta-delta"]
                self.center = cfg["pre_processing"][k].get("center",False)
                pad = cfg["pre_processing"][k].get("pad",win_length//2)
                pre_processing_layers.append((k, torchaudio.transforms.MFCC(sample_rate=self.samplerate,
                                                                            n_mfcc=n_mfcc,
                                                                            melkwargs={'n_fft': n_fft,
                                                                                       'n_mels': n_mels,
                                                                                       'hop_length': hop_length,
                                                                                       'win_length':win_length,
                                                                                       'center':self.center,
                                                                                       'pad':pad})))
                pre_processing_layers.append((k+"_delta",Deltas(e=False,
                                                                d=delta,
                                                                dd=delta2)))
                input_size = self.feature_size

            if k.startswith("mel"):
                n_fft = cfg["pre_processing"][k]["n_fft"]
                hop_length = cfg["pre_processing"][k]["win_shift"]
                n_mels = cfg["pre_processing"][k]["n_mels"]
                n_mfcc = cfg["pre_processing"][k]["n_mfcc"]
                pre_processing_layers.append((k, torchaudio.transforms.MelSpectrogram(
                        sample_rate=self.samplerate,
                        n_fft = n_fft,
                        n_mels = n_mels,
                        hop_length = hop_length)))

                input_size = self.feature_size

        self.pre_processing = torch.nn.Sequential(OrderedDict(pre_processing_layers))

        # sequence to sequence network
        sequence_to_sequence_layers = []
        for k in cfg["sequence_to_sequence"].keys():
            if k.startswith("blstm"):
                sequence_to_sequence_layers.append((k, BLSTM(input_size=input_size,
                                                             blstm_sizes=cfg["sequence_to_sequence"][k]["output_size"],
                                                             num_layers=cfg["sequence_to_sequence"][k]["num_layers"])))
                input_size = cfg["sequence_to_sequence"][k]["output_size"] * 2

        self.sequence_to_sequence = torch.nn.Sequential(OrderedDict(sequence_to_sequence_layers))

        # post processing network
        if cfg["activation"] is not None:
            activation = cfg["activation"]
        else:
            activation='tanh'

        if activation == 'tanh':
            post_processing_activation = torch.nn.Tanh()
        elif activation == 'relu':
            post_processing_activation = torch.nn.ReLU()
        elif activation == 'sigmoid':
            post_processing_activation = torch.nn.Sigmoid()
        else:
            post_processing_activation = torch.nn.Tanh()

        post_processing_layers = []
        for k in cfg["post_processing"].keys():

            if k.startswith("lin"):
                post_processing_layers.append((k, torch.nn.Linear(input_size,
                                                            cfg["post_processing"][k]["output"])))
                input_size = cfg["post_processing"][k]["output"]

            elif k.startswith("activation"):
                post_processing_layers.append((k, post_processing_activation))

            elif k.startswith('batch_norm'):
                post_processing_layers.append((k, torch.nn.BatchNorm1d(input_size)))

            elif k.startswith('dropout'):
                post_processing_layers.append((k, torch.nn.Dropout(p=cfg["post_processing"][k])))

        self.post_processing = torch.nn.Sequential(OrderedDict(post_processing_layers))
        self.post_processing.apply(_init_weights)
        self.output_size = input_size

    def forward(self, inputs):
        """

        :param inputs: raw audio signal
        :return:
        """
        if self.center:
            x = self.pre_processing(inputs[:, :, :-1])
        else:
            x = self.pre_processing(inputs[:, :, :])
        # remove energy
        if len(x.shape) == 4:
            x = torch.squeeze(x[:, :, :])
        x = self.sequence_to_sequence(x.permute(0, 2, 1))
        x = self.post_processing(x)
        return x

    def get_output_size(self):
        """

        :return:
        """
        return self.output_size

    def predict(self,
                wav_filename,
                uem_filename,
                device,
                shift,
                output_rate,
                th_in,
                th_out,
                seg_duration=2.0,
                show=None,
                audio_fr=16000,
                out_fr=100,
                batch_size=64,
                task="vad",
                mode="mean"
                ):
        """
            A MODIFIER POU NE PRENDRE QUE LE NOM DU FICHIER WAV ET CRÉER LE DATA LOADER À L'INTERIEUR

        :param seg_duration:
        :param show:
        :param mode:
        :param wav_filename:
        :param batch_size:
        :param uem_filename:
        :param out_fr:
        :param audio_fr:
        :param task:
        :param th_out:
        :param th_in:
        :param output_rate:
        :param shift:
        :param model:
        :param validation_loader:
        :param device:
        :param only_lab_generation: only generating lab file for each wav file without evaluation
        :return: the raw ouput of the network (probability for each class) the vector of labels
        """
        if show is None:
            show = wav_filename

        data_set = SeqSetSingle(show=show,          # Pourquoi????
                                wav_fn=wav_filename,
                                label_set=None,     # Pourquoi???
                                audio_framerate=audio_fr,
                                output_framerate=out_fr,
                                duration=seg_duration,
                                task="vad",
                                uem=uem_filename,   # initalement UEM
                                shift=shift)

        data_loader = DataLoader(data_set,
                                 batch_size=batch_size,
                                 shuffle=False,
                                 drop_last=False,
                                 pin_memory=True,
                                 num_workers=5
                                 )

        output_data = []
        output_idx = []

        sm = torch.nn.Softmax(dim=2)
        with torch.no_grad():
            # TODO : to speed up
            for batch_idx, (win_idx, data) in enumerate(data_loader):
                output = sm(self.forward(data.to(device))).cpu().numpy()
                for ii in range(output.shape[0]):
                    output_data.append(output[ii])
                    output_idx.append(int(win_idx[ii]))

        final_output, _ = multi_label_combination(output_idx,
                                                  None,
                                                  output_data,
                                                  shift,
                                                  output_rate,
                                                  mode=mode)

        if task == "vad":
            prediction = filter_vad(final_output, th_in, th_out)

        elif task == "speaker_turn":
            prediction = filter_speaker_turn(final_output, th_in, output_rate, min_durationi_spkt)
        elif task == "overlap":
            prediction = filter_overlap(final_output, th_in, th_out)
        else:
            raise NotImplementedError()

        return prediction.astype("int"), final_output

