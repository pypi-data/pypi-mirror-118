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
Copyright 2014-2021 Anthony Larcher

"""

import numpy
import shutil
import torch

from datetime import datetime
from .sequence_sets import SeqSet
from .sequence_sets import SeqSetSampler
from .sequence_sets import SeqSetRandomSampler
from .sequence_models import SeqToSeq

from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from sklearn.metrics import confusion_matrix

__license__ = "LGPL"
__author__ = "Anthony Larcher & Martin Lebourdais & Theo Mariotte"
__copyright__ = "Copyright 2015-2021 Anthony Larcher"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'


def save_checkpoint(state, is_best, filename='checkpoint.pth.tar', best_filename='model_best.pth.tar'):
    """
    :param state:
    :param is_best:
    :param filename:
    :param best_filename:
    :return:
    """
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, best_filename)


def prepare_loaders(dataset_yaml, logger=None, rng_=None, seed=1234):
    """
    Prepare Pytoch DataLoader for training and evaluation of seq2seq model

    :param dataset_yaml:
    :param logger:
    :param rng_:
    :param seed:
    :return:
    """
    if rng_ is None:
        rng = numpy.random.default_rng(seed)
    else:
        rng = rng_
    dataset = dataset_yaml

    # training loader with custom data sampler
    task = dataset["task"]
    sampler_typ = dataset["sampler_type"]
    file_list = dataset["train"]["file_list"]
    eval_file_list = dataset["eval"]["file_list"]
    seg_set = dataset["train"]["seg_set"]
    eval_seg_set = dataset["eval"]["seg_set"]
    batch_size = dataset["sampler"]["batch_size"]
    batch_num = dataset["sampler"]["batch_number"]
    ola_ratio = dataset["sampler"]["overlap_ratio"]
    art_ola_ratio = dataset["sampler"]["artificial_overlap_ratio"]
    spkT_ratio = dataset["sampler"]["speaker_turn_ratio"]
    speech_ratio = dataset["sampler"]["speech_ratio"]
    num_workers = dataset["num_workers"]

    if sampler_typ == "balanced":
        print(f"Overlap proportion = {ola_ratio}, speech proportion = {speech_ratio}, artoverlap proportion = {art_ola_ratio}")
        sampler = SeqSetSampler(list_file=file_list,
                                seg_set=seg_set,
                                speech_ratio=speech_ratio,
                                spk_turn_ratio=spkT_ratio,
                                overlap_ratio=ola_ratio,
                                artificial_overlap_ratio = art_ola_ratio,
                                batch_size=batch_size,
                                batch_number=batch_num,
                                task=task,
                                rng = rng)
    elif sampler_typ == "random":
        sampler = SeqSetRandomSampler(batch_size=batch_size,
                                      batch_num=batch_num,
                                      list_file=file_list,
                                      seg_set=seg_set,
                                      rng = rng)

    else:
        raise NotImplementedError()

    training_set = SeqSet(dataset_params=dataset, mode="train", logger=logger, rng = rng)

    training_loader = DataLoader(training_set,
                                 sampler = sampler,
                                 batch_size=batch_size,
                                 num_workers=num_workers)

    evaluation_set = SeqSet(dataset_params=dataset,mode="eval", logger=logger, rng=rng)
    eval_sampler = SeqSetRandomSampler(batch_size=batch_size,
                                       batch_num=batch_num,
                                       list_file=eval_file_list,
                                       seg_set=eval_seg_set,
                                       rng = rng)

    eval_loader = DataLoader(evaluation_set,
                             sampler=eval_sampler,
                             batch_size=batch_size,
                             num_workers=num_workers)

    return training_loader, eval_loader


def seqtoseq_train(training_loader,
                   validation_loader,
                   model,
                   task,
                   training_yaml,
                   logger,
                   rng_=None,
                   seed=1234):
    """
    Training loop for seqtoseq model used for VAD, overlap and speaker
    turn detection tasks

    :param training_loader: Pytorch DataLoader for training set
    :param validation_loader: Pytorch DataLoader for validation set
    :param model: model to be trained
    :param task: training task (e.g. 'vad')
    :param training_yaml: YAML file containing training parameters
    :param logger: TrainLogger object to follow training and track process
    """
    if rng_ is None:
        rng = numpy.random.default_rng(seed)
    else:
        rng = rng_
    # read learning parameters
    train_params = training_yaml

    if "model_name" in train_params.keys():
        model_name=train_params["model_name"]
    else:
        model_name=None

    epochs = train_params["number_of_epochs"]
    opt = train_params["optimizer"]
    lr = train_params["learning_rate"]
    momentum = train_params["momentum"]
    patience = train_params["patience"]
    seed = train_params["seed"]
    xent_weights = train_params["xent_weights"]
    now = datetime.now()
    time = now.strftime("%m-%d_%H-%M")
    checkpoint_model_name = train_params["checkpoint_name"]
    best_model_name = train_params["best_name"]
    multi_gpu = train_params["multi_gpu"]
    num_thread = train_params["num_thread"]
    log_interval = train_params["log_interval"]

    if "scheduler" in train_params:
        scheduler_name = train_params["scheduler"].get("type",'None')
    else:
        scheduler_name = 'None'
    tensorboard_logs = train_params.get("tensorboard_logs",None)

    if tensorboard_logs is not None:
        tensorboard_logs += time+'/'
    # current device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # in case of multi_gpu training
    if torch.cuda.device_count() > 1 and multi_gpu:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = torch.nn.DataParallel(model)
    else:
        print("Train on a single GPU")

    # push model to GPU
    model.to(device)

    """
    Set the training options
    """
    if opt == 'sgd':
        _optimizer = torch.optim.SGD
        _options = {'lr': lr, 'momentum': momentum}
    elif opt == 'adam':
        _optimizer = torch.optim.Adam
        _options = {'lr': lr}
    elif opt == 'rmsprop':
        _optimizer = torch.optim.RMSprop
        _options = {'lr': lr}

    params = [
        {
            'params': [
                param for name, param in model.named_parameters() if 'bn' not in name
            ]
        },
        {
            'params': [
                param for name, param in model.named_parameters() if 'bn' in name
            ],
            'weight_decay': 0
        },
    ]

    optimizer = _optimizer([{'params': model.parameters()},], **_options)
    if scheduler_name == "Plateau":
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', verbose=True,patience = train_params["scheduler"]["patience"])
    if scheduler_name == "Cycle":
        scheduler = torch.optim.lr_scheduler.CyclicLR(optimizer,mode='triangular2',base_lr=train_params["scheduler"]["base_lr"],max_lr=train_params["scheduler"]["max_lr"],step_size_up=train_params["scheduler"]["step"])
    if scheduler_name == "None":
        scheduler = None
    best_fmeas = 0.0
    best_fmeas_epoch = 1
    curr_patience = patience

    # for tensorboard training monitoring
    writer = SummaryWriter(log_dir=tensorboard_logs)
    for epoch in range(1, epochs + 1):

        # Process one epoch and return the current model
        model, optimizer, scheduler = train_epoch(model,
                                                  training_loader,
                                                  optimizer,
                                                  scheduler=scheduler,
                                                  log_interval=log_interval,
                                                  epoch=epoch,
                                                  device=device,
                                                  xent_weights=xent_weights,
                                                  writer=writer,
                                                  logger=logger)

        # validation
        val_loss, accuracy, fmeas = eval_epoch(validation_loader,
                                               model,
                                               device,
                                               epoch,
                                               xent_weights=xent_weights,
                                               writer=writer,
                                               logger=logger)

        # Decrease learning rate according to the scheduler policy
        # scheduler.step(val_loss)
        logger.message(stream=f"Learning rate is {optimizer.param_groups[0]['lr']}")

        # remember best accuracy and save checkpoint
        is_best = fmeas > best_fmeas
        best_fmeas = max(fmeas,best_fmeas)

        if type(model) is SeqToSeq:
            save_checkpoint({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'accuracy': best_fmeas,
                'scheduler': scheduler
            }, is_best, filename=checkpoint_model_name+".pt", best_filename=best_model_name + '.pt')
        else:
            save_checkpoint({
                'epoch': epoch,
                'model_state_dict': model.module.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'accuracy': best_fmeas,
                'scheduler': scheduler
            }, is_best, filename=checkpoint_model_name +".pt", best_filename=best_model_name + '.pt')

        if is_best:
            best_fmeas_epoch = epoch
            curr_patience = patience
        else:
            curr_patience -= 1

    logger.message(stream=f"Best accuracy {best_fmeas * 100.} obtained at epoch {best_fmeas_epoch}")


def train_epoch(model,
                training_loader,
                optimizer,
                device,
                epoch,
                log_interval,
                scheduler=None,
                xent_weights=[0.5,0.5],
                writer=None,
                logger=None):
    """
    Model training along one epoch

    :param model: model to be trained
    :param training_loader: train set loader
    :param optimizer: current optimizer to update system weights
    :param device: current device (GPUs,...)
    :param epoch: index of the current epoch (for logging)
    :param log_interval: number of batch to process between two logging outputs
    :param xent_weights: weights of the cross entropy loss
    :param writer: logging on tensorboard
    :param logger: logging in a log file
    """
    model.to(device)
    model.train()
    # criterion = torch.nn.CrossEntropyLoss(reduction='mean', weight=torch.FloatTensor(xent_weights).to(device))
    criterion = torch.nn.CrossEntropyLoss(reduction='mean')

    recall = 0.0
    precision = 0.0
    accuracy = 0.0
    mean_speech_ratio = 0.0
    macrotp = 0.0
    macrofp = 0.0
    macrotn = 0.0
    macrofn = 0.0
    loss_acc = 0.0
    count = 0
    sm = torch.nn.Softmax(dim=1)
    for batch_idx, (data, target) in enumerate(training_loader):

        # target = target.squeeze()
        output = model(data.to(device))

        # Output shape = (Batch,time,nclass)
        # Target shape = (Batch,time)
        reshaped_output = torch.flatten(output,start_dim=0,end_dim=1)
        reshaped_target = torch.flatten(target)

        loss = criterion(reshaped_output,reshaped_target.to(device)) # Want (batch , class, time) and (batch,time) or (seq,class) (seq)
        loss_acc += loss
        count+=1
        if scheduler is not None:
            if isinstance(scheduler,torch.optim.lr_scheduler.CyclicLR):
                scheduler.step()
            else:
                scheduler.step(loss)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        output = sm(reshaped_output)
        tn, fp, fn, tp = confusion_matrix(reshaped_target.cpu(),torch.argmax(output,1).cpu()).ravel()
        macrotp += tp
        macrotn += tn
        macrofp += fp
        macrofn += fn

        if writer:
            writer.add_scalar('Loss/Train',loss.item(),epoch*len(training_loader)+batch_idx)
            writer.add_scalar('lr',optimizer.param_groups[0]['lr'],epoch*len(training_loader)+batch_idx)

        if batch_idx % log_interval == 0:
            precision, recall, f_measure, accuracy = matrix2metrics(macrotp, macrotn, macrofp, macrofn)
            averaged_loss = loss_acc/count
            loss_acc = 0.0
            count = 0
            macrotp = 0.0
            macrofp = 0.0
            macrotn = 0.0
            macrofn = 0.0
            batch_size = target.shape[0]
            if precision != 0 or recall != 0:
                logger.addStep(
                            mode="train",
                            epoch=epoch,
                            batch_idx=batch_idx,
                            batch_num=len(training_loader),
                            loss=averaged_loss,
                            metrics={"acc": accuracy,
                                     "precision": precision,
                                     "recall": recall,
                                     "fmeas": f_measure})
            else:
                f_measure = 0
                logger.addStep(
                            mode="train",
                            epoch=epoch,
                            batch_idx=batch_idx,
                            batch_num=len(training_loader),
                            loss=averaged_loss,
                            metrics={"acc": accuracy,
                                     "precision": precision,
                                     "recall": recall})

            if writer:
                writer.add_scalar('Acc/Train', accuracy, (epoch-1)*len(training_loader)+batch_idx)
                writer.add_scalar('F-meas/Train', f_measure, (epoch-1)*len(training_loader)+batch_idx)

    return model, optimizer, scheduler


def eval_epoch(validation_loader,
               model,
               device,
               epoch,
               xent_weights=[0.5, 0.5],
               writer=None,
               logger=None):
    """

    :param validation_loader:
    :param model:
    :param device:
    :param epoch:
    :param xent_weights:
    :param writer:
    :param logger:
    :return:
    """
    model.to(device)
    model.eval()
    criterion = torch.nn.CrossEntropyLoss(reduction='mean')

    recall = 0.0
    precision = 0.0
    accuracy = 0.0
    loss = 0.0
    macrotp = 0.0
    macrotn = 0.0
    macrofp = 0.0
    macrofn = 0.0
    sm = torch.nn.Softmax(dim=1)
    length = len(validation_loader)
    with torch.no_grad():

        for batch_idx, (data,target) in enumerate(validation_loader):
            output = model(data.to(device))

            reshaped_output = torch.flatten(output,start_dim=0,end_dim=1)
            reshaped_target = torch.flatten(target)

            loss += criterion(reshaped_output,reshaped_target.to(device)) # Want (batch , class, time) and (batch,time)

            output = sm(reshaped_output)

            try:
                tn, fp, fn, tp = confusion_matrix(reshaped_target.cpu(),torch.argmax(output,1).cpu()).ravel()
            except:
                tn = 0
                fp = 0
                fn = 0
                tp = 0
            macrotp += tp
            macrotn += tn
            macrofp += fp
            macrofn += fn

        # Metric calculation from confusion matrix
        precision, recall, f_measure, accuracy = matrix2metrics(macrotp, macrotn, macrofp, macrofn)
        if precision != 0 or recall != 0:
            # logger
            logger.addStep(
                        mode="eval",
                        epoch=epoch,
                        loss=loss/length,
                        metrics={"acc" : accuracy,
                                 "precision" : precision,
                                 "recall" : recall,
                                 "fmeas" : f_measure})
        else:
            f_measure=0
            logger.addStep(
                        mode="eval",
                        epoch=epoch,
                        loss=loss/length,
                        metrics={"acc" : accuracy,
                                 "precision" : precision,
                                 "recall" : recall})

        # tensor board
        if writer:
            writer.add_scalar('Loss/Eval', loss/length, epoch)
            writer.add_scalar('Acc/Eval', accuracy, epoch)
            if f_measure:
                writer.add_scalar('F-meas/Eval', f_measure, epoch)

    return loss/length, accuracy, f_measure


def matrix2metrics(tp, tn, fp, fn):
    """

    :param tp:
    :param tn:
    :param fp:
    :param fn:
    :return:
    """
    eps = 1e-7
    prec = tp/(tp+fp+eps)
    rec = tp/(tp+fn+eps)
    acc = (tp+tn)/(tp+tn+fp+fn+eps)
    fmes = (2*tp)/(2*tp+fp+fn+eps)
    return prec, rec, fmes, acc

