# -*- coding: utf-8 -*-
#
# This file is part of SIDEKIT.
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is free software: you can redistribute it and/or modify
# it under the terms of the GNU LLesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# SIDEKIT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.

"""
Copyright 2014-2021 Anthony Larcher & Martin Lebourdais & Theo Mariotte

"""

import h5py
import numpy
import pandas
import pickle
import shelve
import time
import torch
import torchaudio
import tqdm

from ..diar import Diar
from sidekit.nnet.augmentation import data_augmentation
from datetime import datetime


__license__ = "LGPL"
__author__ = "Theo Mariotte & Anthony Larcher"
__copyright__ = "Copyright 2015-2021 Anthony Larcher"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'


class SeqSetRandomSampler(torch.utils.data.Sampler):
    """
    Random data sampler used to build batches in PyTprch DataLoader
    This sampler randomly selects training segments in the database that will be used for training.

    """
    def __init__(self, batch_size, batch_num, list_file, seg_set,rng=None, seed=1234):
        """

        :param batch_size: number of segments per batch
        :param batch_num: number of batches per epoch of training
        :param list_file: list of the files to be used for the training
        :param seg_set: segment sets previously generated using data preparation
        :param rng: random number generator (default : None)
        :param seed: seed of the random generator (default : 1234)
        """
        if rng is None:
            self.rng = numpy.random.default_rng(seed)
        else:
            self.rng = rng
        with open(list_file, "r") as ff:
            self.show_list = [l.strip() for l in ff.readlines()]

        idx_iter = list()
        segments = shelve.open(seg_set)
        for show in tqdm.tqdm(
                self.show_list, desc="Sampler initialization,first pass", unit="show"
        ):
            seg_tags = segments.get(show)

            for seg in seg_tags:
                idx_iter.append({'seg':seg,'overlap':None})

        self.index_iterator = numpy.array(idx_iter)
        self.length = batch_num * batch_size
        segments.close()

    def __iter__(self):
        """

        :return:
        """
        self.rng.shuffle(self.index_iterator)
        self.iter = self.index_iterator[: self.length]
        return iter(self.iter)

    def __len__(self) -> int:
        """

        :return:
        """
        return self.length


class SeqSetSampler(torch.utils.data.Sampler):
    """

    """
    def __init__(self,
                 list_file,
                 seg_set,
                 speech_ratio,
                 spk_turn_ratio,
                 overlap_ratio,
                 artificial_overlap_ratio,
                 batch_size=64,
                 batch_number=None,
                 task="overlap",
                 rng=None,
                 seed=1234):
        """
        Fast Sampler from pytorch that respect contraints:
            - Not more than one segment per show in a batch (as much as possible)
            - Ratio of overlap segments, speech segment, speaker turn segment

        :param show_list: list of the shows on the training set
        :param seg_set: path to the shelve file where segments and tags are stored
        :param speech_ratio: ratio of segments annotated as speech only (between 0 and 1)
        :param spk_turn_ratio: ratio of segments annotated as speech turn (between 0 and 1)
        :param overlap: ratio of segments annotated as overlaps (between 0 and 1)
        :param batch_size: size of the batch
        :param batch_number: number of batches to be generated
        :param task: Task the sampler is needed for
        :param rng: random number generator for Numpy
        :param seed: seed for random generator
        """
        # List of Uris
        with open(list_file, "r") as ff:
            self.show_list = [l.strip() for l in ff.readlines()]
        if rng is None:
            self.rng = numpy.random.default_rng(seed)
        else:
            self.rng = rng
        self.speech_ratio = speech_ratio
        self.spkT_ratio = spk_turn_ratio
        self.overlap_ratio = overlap_ratio
        self.artificial_overlap_ratio = artificial_overlap_ratio
        self.batch_size = batch_size

        batch_num_max = 10000
        self.batch_num = batch_num_max if (batch_number is None) else batch_number
        # dictionnary containing global indexes of seglents for each show
        self.seg_per_show = dict()

        # open shelve file containing segments start times for each show + segments tags
        # (i.e. speech/non-speech ; spk turn ; overlap)
        # Index of each segment w.r.t. the whole dataset are also saved here
        segments = shelve.open(seg_set)
        len_ov = []
        len_spkT = []
        len_speech = []
        len_nospeech = []
        self.shows = {
            "overlap": {"list": [], "probs": []},
            "speaker_change": {"list": [], "probs": []},
            "speech": {"list": [], "probs": []},
            "nonspeech": {"list": [], "probs": []},
        }

        for show in tqdm.tqdm(
                self.show_list, desc="Sampler initialization,first pass", unit="show"
        ):

            # Classify each segment (in terms of global index)
            # for speaker_change and overlap you'll need an other list
            idx_speech = list()
            idx_nonspeech = list()
            idx_spkT = list()
            idx_overlap = list()
            lst_speech = []
            lst_nonspeech = []
            lst_spkT = []
            lst_overlap = []

            self.seg_tags = segments.get(show)
            #test
            # print(self.seg_tags)
            # return

            for ii in range(len(self.seg_tags)):
                seg = self.seg_tags[ii]

                # segment labelled as overlap
                if seg["overlap"]:
                    lst_overlap.append(seg)
                # segment labelled as speech turn
                elif seg["speaker_change"]:
                    lst_spkT.append(seg)
                # segment labelled as speech/non-speech
                elif seg["speech"]:
                    lst_speech.append(seg)
                else:
                    lst_nonspeech.append(seg)

            if lst_overlap:
                self.shows["overlap"]["list"].append(show)
            if lst_spkT:
                self.shows["speaker_change"]["list"].append(show)
            if lst_speech:
                self.shows["speech"]["list"].append(show)
            if lst_nonspeech:
                self.shows["nonspeech"]["list"].append(show)

            len_ov.append(len(lst_overlap))
            len_spkT.append(len(lst_spkT))
            len_speech.append(len(lst_speech))
            len_nospeech.append(len(lst_nonspeech))

            # all indexes are stored in a dictionary with each index classified
            self.seg_per_show[show] = {
                "overlap": numpy.array(lst_overlap),
                "speaker_change": numpy.array(lst_spkT),
                "speech": numpy.array(lst_speech),
                "nonspeech": numpy.array(lst_nonspeech),
            }

        # max length of the limiting segment without a possible outlier
        len_max_ov = max(int(numpy.mean(len_ov) + 2 * numpy.std(len_ov)),self.batch_num)

        # check list sizes w.r.t. the batch size
        if len(self.shows["overlap"]["list"]) < self.batch_size:
            self.shows["overlap"]["list"] = self.shows["overlap"]["list"] * numpy.ceil(
                self.batch_size / len(self.shows["overlap"]["list"])
            ).astype("int")

        if len(self.shows["speaker_change"]["list"]) < self.batch_size:
            self.shows["speaker_change"]["list"] = self.shows["speaker_change"]["list"] * numpy.ceil(
                self.batch_size / len(self.shows["speaker_change"]["list"])
            ).astype("int")

        if len(self.shows["speech"]["list"]) < self.batch_size:
            self.shows["speech"]["list"] = self.shows["speech"]["list"] * numpy.ceil(
                self.batch_size / len(self.shows["speech"]["list"])
            ).astype("int")

        if len(self.shows["nonspeech"]["list"]) < self.batch_size:
            self.shows["nonspeech"]["list"] = self.shows["nonspeech"]["list"] * numpy.ceil(
                self.batch_size / len(self.shows["nonspeech"]["list"])
            ).astype("int")

        # probability vectors
        self.shows["overlap"]["probs"] = numpy.ones(len(self.shows["overlap"]["list"]), dtype=int)  # will become a list
        self.shows["speaker_change"]["probs"] = []
        self.shows["speech"]["probs"] = []
        self.shows["nonspeech"]["probs"] = []

        self.batch_num = min(self.batch_num,batch_num_max)
        len_max_speech = max(int(numpy.mean(len_speech) + 2 * numpy.std(len_speech)),self.batch_num)
        len_max_nospeech = max(int(numpy.mean(len_nospeech) + 2 * numpy.std(len_nospeech)),self.batch_num)
        len_max_spkT = max(int(numpy.mean(len_spkT) + 2 * numpy.std(len_spkT)),self.batch_num)

        for show in tqdm.tqdm(
                self.show_list, desc="Sampler initialization, Padding", unit="show"
        ):
            if show in self.shows["overlap"]["list"]:
                # self.shows["overlap"]['probs'].append(len_max_unit)
                if 0 < len(self.seg_per_show[show]["overlap"]) < len_max_ov:

                    tmplist = numpy.repeat(
                        self.seg_per_show[show]["overlap"],
                        numpy.ceil(
                            len_max_ov / len(self.seg_per_show[show]["overlap"])
                        ).astype("int"),
                        axis=0
                    )
                else:
                    tmplist = self.seg_per_show[show]["overlap"]

                self.seg_per_show[show]["overlap"] = {
                    "data": self.rng.permutation(tmplist[:len_max_ov]),
                    "probs": numpy.ones(len_max_ov)
                }

            if show in self.shows["speaker_change"]["list"]:
                # self.shows["overlap"]['probs'].append(len_max_unit)
                if 0 < len(self.seg_per_show[show]["speaker_change"]) < len_max_spkT:

                    tmplist = numpy.repeat(
                        self.seg_per_show[show]["speaker_change"],
                        numpy.ceil(
                            len_max_spkT / len(self.seg_per_show[show]["speaker_change"])
                        ).astype("int"),
                        axis=0
                    )
                else:
                    tmplist = self.seg_per_show[show]["speaker_change"]

                self.seg_per_show[show]["speaker_change"] = {
                    "data": self.rng.permutation(tmplist[:len_max_spkT]),
                    "probs": numpy.ones(len_max_spkT),
                }

            if 0 < len(self.seg_per_show[show]["speech"]) < len_max_speech:
                try:
                    tmplist = numpy.repeat(
                        self.seg_per_show[show]["speech"],
                        numpy.ceil(
                            len_max_speech / len(self.seg_per_show[show]["speech"])
                        ).astype("int"),
                        axis=0
                    )
                except ZeroDivisionError as e:
                    print(show)
                    raise ZeroDivisionError(show)


            else:
                tmplist = self.seg_per_show[show]["speech"]

            self.seg_per_show[show]["speech"] = {
                "data": self.rng.permutation(tmplist[:len_max_speech]),
                "probs": numpy.ones(len_max_speech),
            }

            if 0 < len(self.seg_per_show[show]["nonspeech"]) < len_max_nospeech:

                tmplist = numpy.repeat(
                    self.seg_per_show[show]["nonspeech"],
                    numpy.ceil(
                        len_max_nospeech / len(self.seg_per_show[show]["nonspeech"])
                    ).astype("int"),
                    axis=0
                )

            else:
                tmplist = self.seg_per_show[show]["nonspeech"]

            self.seg_per_show[show]["nonspeech"] = {
                "data": self.rng.permutation(tmplist[:len_max_nospeech]),
                "probs": numpy.ones(len_max_nospeech),
            }

        for show in self.shows["speaker_change"]['list']:
            self.shows["speaker_change"]["probs"].append(
                len(self.seg_per_show[show]["speaker_change"]["data"])
            )

        for show in self.shows["speech"]['list']:
            self.shows["speech"]["probs"].append(
                len(self.seg_per_show[show]["speech"]["data"])
            )

        for show in self.shows["nonspeech"]['list']:
            self.shows["nonspeech"]["probs"].append(
                len(self.seg_per_show[show]["nonspeech"]["data"])
            )

        self.shows["overlap"]["probs"] *= len_max_ov
        self.shows["speaker_change"]["probs"] = numpy.array(self.shows["speaker_change"]["probs"])
        self.shows["speech"]["probs"] = numpy.array(self.shows["speech"]["probs"])
        self.shows["nonspeech"]["probs"] = numpy.array(self.shows["nonspeech"]["probs"])

        self.shows["speaker_change"]["probs"] = self.shows["speaker_change"]["probs"][
            self.shows["speaker_change"]["probs"] > 0
            ]
        self.shows["speech"]["probs"] = self.shows["speech"]["probs"][
            self.shows["speech"]["probs"] > 0
            ]
        self.shows["nonspeech"]["probs"] = self.shows["nonspeech"]["probs"][
            self.shows["nonspeech"]["probs"] > 0
            ]

        self.shows["overlap"]["list"] = numpy.array(self.shows["overlap"]["list"])
        self.shows["speaker_change"]["list"] = numpy.array(self.shows["speaker_change"]["list"])
        self.shows["speech"]["list"] = numpy.array(self.shows["speech"]["list"])
        self.shows["nonspeech"]["list"] = numpy.array(self.shows["nonspeech"]["list"])
        self.length = self.batch_size * self.batch_num
        self.backup_shows = pickle.dumps(self.shows)
        self.backup_seg_per_show = pickle.dumps(self.seg_per_show)
        segments.close()
        self.index_iterator = None

    def __iter__(self):
        """

        :return:
        """
        # count the number of segment of each type
        if self.index_iterator is None:
            N_ola = int(self.overlap_ratio * self.batch_size)
            N_spkT = int(self.spkT_ratio * self.batch_size)
            N_speech = int(self.speech_ratio * self.batch_size)
            N_artificial_ov = int(self.artificial_overlap_ratio * self.batch_size)
            # In case of overlap
            N_nospeech = max(0,self.batch_size - (N_ola + N_speech + N_artificial_ov + N_spkT))

            index_iterator = []

            # RAZ

            t0 = time.time()
            self.seg_per_show = pickle.loads(self.backup_seg_per_show)
            self.shows = pickle.loads(self.backup_shows)

            #self.index_iterator = numpy.zeros((self.length,), dtype=int)

            for batch_idx in range(self.batch_num-1):#Last one fail

                # Overlap segment selection

                probs = self.shows["overlap"]["probs"]
                N = len(self.shows["overlap"]["list"])

                ov_show_idx = self.rng.choice(
                    N, size=N_ola, replace=False, p=probs / numpy.sum(probs)
                ).astype("int")
                self.shows["overlap"]["probs"][ov_show_idx] -= 1

                ov_show = self.shows["overlap"]["list"][ov_show_idx]

                # Speaker turn segments selection
                probs = self.shows["speaker_change"]["probs"]
                N = len(self.shows["speaker_change"]["list"])

                spkT_show_idx = self.rng.choice(
                    N, size=N_spkT, replace=False, p=probs / numpy.sum(probs)
                ).astype("int")
                self.shows["speaker_change"]["probs"][spkT_show_idx] -= 1

                spkT_show = self.shows["speaker_change"]["list"][spkT_show_idx]

                # Speech segment selection
                probs = self.shows["speech"]["probs"]
                N = len(self.shows["speech"]["list"])
                speech_show_idx = self.rng.choice(
                    N, size=N_speech, replace=False, p=probs / numpy.sum(probs)
                ).astype("int")
                self.shows["speech"]["probs"][speech_show_idx] -= 1
                speech_show = self.shows["speech"]["list"][speech_show_idx]

                #Artificial overlap selection

                N = len(self.shows["speech"]["list"])
                art_ov_show_idx = self.rng.choice(
                    N, size=N_artificial_ov, replace=False,
                ).astype("int")

                art_ov_show = self.shows["speech"]["list"][art_ov_show_idx]

                # Non speech segment selection
                probs = self.shows["nonspeech"]["probs"]
                N = len(self.shows["nonspeech"]["list"])

                nospeech_show_idx = self.rng.choice(
                    N, size=N_nospeech, replace=False, p=probs / numpy.sum(probs)
                ).astype("int")
                self.shows["nonspeech"]["probs"][nospeech_show_idx] -= 1
                nospeech_show = self.shows["nonspeech"]["list"][nospeech_show_idx]

                batch_ = []
                ii = 0
                for show in ov_show:
                    probs = self.seg_per_show[show]["overlap"]["probs"]

                    seg_idx = int(
                        self.rng.choice(
                            len(self.seg_per_show[show]["overlap"]["data"]),
                            p=probs / numpy.sum(probs),
                        )
                    )  # only one value so can't use astype

                    self.seg_per_show[show]["overlap"]["probs"][seg_idx] -= 1

                    structure = {
                        'seg':self.seg_per_show[show]["overlap"]["data"][seg_idx],
                        'overlap':None
                    }
                    batch_.append(structure)

                for show in spkT_show:
                    probs = self.seg_per_show[show]["speaker_change"]["probs"]

                    seg_idx = int(
                        self.rng.choice(
                            len(self.seg_per_show[show]["speaker_change"]["data"]),
                            p=probs / numpy.sum(probs),
                        )
                    )  # only one value so can't use astype

                for show in speech_show:
                    probs = self.seg_per_show[show]["speech"]["probs"]
                    seg_idx = int(
                        self.rng.choice(
                            len(self.seg_per_show[show]["speech"]["data"]),
                            p=probs / numpy.sum(probs),
                        )
                    )
                    self.seg_per_show[show]["speech"]["probs"][seg_idx] -= 1
                    structure = {
                        'seg':self.seg_per_show[show]["speech"]["data"][seg_idx],
                        'overlap':None
                    }
                    batch_.append(structure)


                for show in art_ov_show:

                    seg_idx = int(
                        self.rng.choice(
                            len(self.seg_per_show[show]["speech"]["data"]),

                        )
                    )
                    ov_seg_idx = int(
                        self.rng.choice(
                            len(self.seg_per_show[show]["speech"]["data"]),

                        )
                    )
                    structure = {
                        'seg':self.seg_per_show[show]["speech"]["data"][seg_idx],
                        'overlap':self.seg_per_show[show]["speech"]["data"][ov_seg_idx]
                    }
                    batch_.append(structure)

                for show in nospeech_show:
                    probs = self.seg_per_show[show]["nonspeech"]["probs"]
                    seg_idx = int(
                        self.rng.choice(
                            len(self.seg_per_show[show]["nonspeech"]["data"]),
                            p=probs / numpy.sum(probs),
                        )
                    )
                    self.seg_per_show[show]["nonspeech"]["probs"][seg_idx] -= 1
                    structure = {
                        'seg':self.seg_per_show[show]["nonspeech"]["data"][seg_idx],
                        'overlap':None
                    }
                    batch_.append(structure)
                self.rng.shuffle(batch_)

                index_iterator = index_iterator + batch_
            # self.index_iterator = index_iterator
            self.index_iterator = None

        else:
            index_iterator = self.index_iterator

        return iter(index_iterator)

    def __len__(self) -> int:
        return self.length


class SeqSet(torch.utils.data.Dataset):
    """
    DataSet for sequence to sequence model training
    """

    def __init__(self, dataset_params, mode="train", logger=None, rng=None, seed=1234):
        """
        constructor

        :param dataset_params: parameters of the dataset extracted from YAML file (dictionnary)
        :param mode: train or evaluation mode (default="train")
        :param logger: logging object to save dataset parameters
        :param rng: random number generator for Numpy (default None)
        :param seed: random seed to control rng
        """
        torchaudio.set_audio_backend("soundfile")
        if rng is None:
            self.rng = numpy.random.default_rng(seed)
        else:
            self.rng = rng
        self.wav_dir = dataset_params["wav_dir"]
        self.label_set = dataset_params[mode]["label_set"]
        self.seg_set = dataset_params[mode]["seg_set"]
        self.audio_fr = dataset_params["audio_fr"]
        self.output_fr = dataset_params["output_fr"]
        self.task = dataset_params["task"]
        self.hdf5_dataset = self.label_set
        self.babble_noise = dataset_params["babble_noise"]
        self.len_ = dataset_params["sampler"]["batch_number"]*dataset_params["sampler"]["batch_size"]
        self.time_base_start = dict()
        self.logger = logger
        with shelve.open(self.seg_set,'r') as segments:
            for show in segments:
                crnt_set = segments.get(show)
                self.time_base_start[show] = crnt_set[0]["start"] #centisenconds
        # labels augmentation for speaker turn detection
        if not "labelling" in dataset_params.keys():
            self.collar_duration = 0.125
        else:
            self.collar_duration = dataset_params["labelling"]["collar_duration"]

        # lire les fichiers contenant les t_start par show pour construire une liste de segments
        self.duration = numpy.ceil(
            dataset_params[mode]["duration"] * self.audio_fr
        ).astype(
            "int"
        )  # in samples

        # start of each file with respect to UEMS (to guarantee sync between raw labels and segment frontiers)
        self.time_base_start = dict()
        with shelve.open(self.seg_set,'r') as segments:
            for show in segments:
                crnt_set = segments.get(show)
                self.time_base_start[show] = crnt_set[0]["start"] #centisenconds

        if mode == "train":
            self.transformation = dataset_params["train"]["transformation"]
        else:
            self.transformation = dataset_params["eval"]["transformation"]

        self.transform = dict()
        if (self.transformation["pipeline"] != "") and (
                self.transformation["pipeline"] is not None
        ):
            print('Transformation required')
            self.transform_number = 1
            transforms = self.transformation
            self.noise_df = None
            if "AddNoise" in transforms:
                self.transform["add_noise"] = self.transformation["AddNoise"]

                noise_df = pandas.read_csv(self.transform["add_noise"]["noise_db_csv"])
                noise_df = noise_df.loc[noise_df.duration > dataset_params[mode]["duration"]]
                self.noise_df = noise_df.set_index(noise_df.type)

            self.rir_df = None
            if "AddReverb" in transforms:
                self.transform["add_reverb"] = self.transformation["AddReverb"]

                tmp_rir_df = pandas.read_csv(self.transform["add_reverb"]["rir_db_csv"])
                tmp_rir_df = tmp_rir_df.loc[tmp_rir_df["type"] == "simulated_rirs"]
                # load the RIR database
                self.rir_df = tmp_rir_df.set_index(tmp_rir_df.type)

    def __getitem__(self, struct):
        """
        Return a given audio segment and its associated labels at index in the dataset.
        Here, raw audio is returned (e.g. sampled at @16000 Hz or @8000 Hz). Labels are
        sampled at @100Hz since it's the model output frame rate.
        """

        # récupère les frontières des segments
        segarr = struct['seg']
        seg = {
            "start":float(segarr[3]),
            "show":segarr[0],
            "stop":float(segarr[4]),
        }

        idx_start = numpy.round(seg["start"] / 100.0 * self.audio_fr).astype(int)

        # load audio waveform (dim = (channels,length))
        # normalization is applied here
        waveform, speech_fs = torchaudio.load(
            filepath=self.wav_dir + seg["show"] + ".wav",
            frame_offset=idx_start,
            num_frames=self.duration,
            channels_first=True,
            normalize=True
        )
        #waveform = normalize(waveform)
        # is the signal mono or not ?
        is_multichannel = waveform.shape[0] > 1

        # add low energy noise to avoid zero values
        waveform += 1e-6 * torch.randn(waveform.shape[0],waveform.shape[1])

        # data augmentation if needed

        if self.transform and not is_multichannel:
            waveform = data_augmentation(
                waveform,
                speech_fs,
                self.transform,
                self.transform_number,
                noise_df=self.noise_df,
                rir_df=self.rir_df,
                babble_noise = self.babble_noise
            )
            if waveform is None:
                print(seg["show"],seg["start"] / 100.0,seg["stop"] / 100.0)
        # in case of multichannel signal, each channel has to be transformed
        elif self.transform and is_multichannel:
            for ii in range(waveform.shape[0]):
                waveform[ii,:] = data_augmentation(
                    waveform[ii,:],
                    speech_fs,
                    self.transform,
                    self.transform_number,
                    noise_df=self.noise_df,
                    rir_df=self.rir_df,
                    babble_noise = self.babble_noise
                )

        # get labels associated with the current audio training segment
        start = numpy.round(seg["start"] / 100.0 * self.output_fr).astype(int) - self.time_base_start[seg["show"]]
        stop = numpy.round(seg["stop"] / 100.0 * self.output_fr).astype(int) - self.time_base_start[seg["show"]]
        with h5py.File(self.label_set, "r") as data:
            crnt_label = data[seg["show"]]["total"][:, start:stop]
        expected_frames_num = int(self.duration/self.audio_fr * self.output_fr)
        if crnt_label.shape[1]<expected_frames_num:
            crnt_label = numpy.pad(crnt_label,[(0,0),(0,expected_frames_num - crnt_label.shape[1])])
        if crnt_label.shape[1] > expected_frames_num:
            crnt_label = crnt_label[:,:expected_frames_num]

        if self.task == "vad":
            output_label = (crnt_label > 0).astype(numpy.long)

        # may probably be optimized...
        elif self.task == "spk_turn":
            label = numpy.zeros_like(crnt_label)
            label[:,:-1] = (numpy.abs(crnt_label[:,:-1] - crnt_label[:,1:]) > 0).astype(
                numpy.long
            )
            # Apply convolution to replace diracs by a chosen shape (gate or triangle)
            filter_sample = int(self.collar_duration * self.output_fr * 2 + 1)

            conv_filt = numpy.ones((filter_sample,))
            output_label = numpy.convolve(conv_filt, label.squeeze(), mode='same')
            output_label = (numpy.expand_dims(output_label,axis=0)>=1).astype(numpy.long)

        elif self.task == "overlap":

            if struct['overlap'] is not None:

                # Loading artificial overlap
                ov_segarr = struct['overlap']
                ov_seg = {
                    "start":float(ov_segarr[3]),
                    "show":ov_segarr[0],
                    "stop":float(ov_segarr[4]),
                }
                idx_start_ov = numpy.round(ov_seg["start"] / 100.0 * self.audio_fr).astype(int)
                frame_count_ov = self.duration

                waveform_ov, _ = torchaudio.load(
                    filepath=self.wav_dir + ov_seg["show"] + ".wav",
                    frame_offset=idx_start_ov,
                    num_frames=frame_count_ov,
                    channels_first=True,
                )

                start_ov = numpy.round(ov_seg["start"] / 100.0 * self.output_fr).astype(int)
                stop_ov = numpy.round(ov_seg["stop"] / 100.0 * self.output_fr).astype(int)
                with h5py.File(self.label_set, "r") as data:
                    label_ov = data[seg["show"]]["total"][:, start_ov:stop_ov]
                if label_ov.shape[1]<expected_frames_num:
                    label_ov = numpy.pad(label_ov,[(0,0),(0,expected_frames_num - label_ov.shape[1])])
                if label_ov.shape[1] > expected_frames_num:
                    label_ov = label_ov[:,:expected_frames_num]
                speech_power = waveform.norm(p=2)
                noise_power = waveform_ov.norm(p=2)
                snr_db = 10 * self.rng.random()+1
                snr = 10 ** (snr_db / 20)
                scale = snr * noise_power / speech_power

                # Sum with artificial segment
                crnt_label += label_ov
                waveform = (scale * waveform + waveform_ov) / 2

            else:
                pass
            # Binarize the label
            output_label = (crnt_label > 1).astype(numpy.long)
        else:
            raise NotImplementedError()

        if torch.isnan(waveform).any():
            print("Waveform NAN !!!")

        return waveform, torch.from_numpy(output_label).T

    def __len__(self):
        return self.len_


class SeqSetSingle(torch.utils.data.Dataset):
    """
    DataSet for evaluating a modelwhich returns a sliding window over one file
    """
    def __init__(self,
                 show,
                 wav_fn,
                 label_set=None,
                 uem=None,
                 audio_framerate=16000,
                 output_framerate=100,
                 duration=2.0,
                 task="overlap",
                 shift=0.5):
        """
        Ctor

        :param show: name of the show on which to run prediction
        :param wave_fn: name of the wavefile to be loaded
        :param seg_set: segments of the test set
        :param label set: labels of the test set
        :param audio_framerate: samplerate of the audio signal
        :param output_framerate: output sample rate
        :param duration: duration of the test segment
        :param tranformation_pipeline: pipeline of transfomations to be applied
        """
        super(SeqSetSingle, self).__init__()
        self.show = show
        self.audio_fr = audio_framerate
        self.output_fr = output_framerate

        self.segment_list = Diar()
        self.task=task
        self.wav_name = wav_fn
        self.duration = numpy.ceil(duration * self.audio_fr).astype("int")  # in samples
        if label_set is None:
            self.give_label = False
        else:
            self.give_label = True
            self.hdf5_dataset = label_set
        # TODO HANDLE UEM
        waveform, sr = torchaudio.load(
            filepath=self.wav_name,
        )
        self.length = waveform.shape[1]

        # start of each file with respect to UEMS (to guarantee sync between raw labels and segment frontiers)
        self.time_base_start = 0
        if uem is not None:
            self.time_base_start = Diar.read_uem(uem)[0]['start']

        self.shift = numpy.ceil(shift * self.audio_fr ).astype("int")
        start = 0
        # Sliding window
        for val in numpy.arange(start=start,stop = self.length, step = self.shift):
            seg_start = (val/self.audio_fr)
            seg_stop = (seg_start + duration)#second
            self.segment_list.append(
                show=show,  # WARNING : vérifier les unités!!!
                start=seg_start,
                stop=seg_stop,
                cluster="",
            )

    def __getitem__(self, index):
        """
        returns a raw waveform segment at given index with its associated labels
        """

        # récupère les frontières des segments
        seg = self.segment_list[index]
        idx_start = numpy.ceil(seg["start"] * self.audio_fr).astype("int")

        # charge le segment wav de N canaux (torchaudio.load)

        waveform, _ = torchaudio.load(
            filepath=self.wav_name,
            frame_offset=idx_start,
            num_frames=self.duration,
            channels_first=True
        )
        if waveform.shape[1]<self.duration:
            waveform = torch.nn.functional.pad(waveform,(0,self.duration - waveform.shape[1]),"constant",0)

        # add low energy noise to avoid zero values
        waveform += (1e-6 * torch.randn(waveform.shape[0],waveform.shape[1])).long()

        # récupère les labels associés au segment
        if self.give_label:
            start = numpy.round(seg["start"] * self.output_fr).astype(int) - self.time_base_start
            stop = numpy.round(seg["stop"] * self.output_fr).astype(int) - self.time_base_start

            with h5py.File(self.hdf5_dataset, "r") as data:
                crnt_label = data[seg["show"]]["total"][:, start:stop]

            expected_frames_num = int(self.duration/self.audio_fr * self.output_fr)
            if crnt_label.shape[1]<expected_frames_num:
                crnt_label = numpy.pad(crnt_label,[(0,0),(0,expected_frames_num - crnt_label.shape[1])])
            if crnt_label.shape[1] > expected_frames_num:
                crnt_label = crnt_label[:,:expected_frames_num]

            # crnt_label = numpy.ones((stop-start,))
            if self.task == "vad":
                output_label = (crnt_label > 0).astype(numpy.long)

            elif self.task == "spk_turn":
                output_label = (numpy.abs(crnt_label[:-1] - crnt_label[1:]) > 0).astype(
                    numpy.long
                )

            elif self.task == "overlap":
                output_label = (crnt_label > 1).astype(numpy.long)

            else:
                raise NotImplementedError()

            return index,waveform, torch.from_numpy(output_label).T
        else:
            return index, waveform

    def __len__(self):
        """

        :return:
        """
        return len(self.segment_list)
