# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 11:03:42 2019

@author: MAGESHWARAN
"""
import os
import json
import configparser
import numpy as np


def evaluateModel(gt_result, model_result):
    """
        Evaluates the model based on ground truth values

    Input:
        gt_result : dict object containing ground truth result

        model_result: dict object containing model generated output

    Output:
        Returns nothing, Prints the evaluation metrics in the console

    """

    gt_images = list(gt_result.keys())

    tp = tn = fp = fn = 0

    for img in gt_images:

        gt_association = gt_result[img]
        model_association = model_result[img]
        gt_list = []
        model_list = []

        if gt_association:
            for i in range(len(gt_association)):
                gt_list.append(gt_association[i][0])

            for j in range(len(model_association)):
                model_list.append(model_association[j][0])

            gt_copy = gt_list.copy()
            model_copy = model_list.copy()

            for association in gt_list:
                if association in model_list:
                    if img != "NA":
                        tp += 1
                    else:
                        tn += 1
                    gt_copy.remove(association)
                    model_copy.remove(association)

                else:
                    fn += 1

            for found in model_copy:
                if found not in gt_copy:
                    fp += 1

        elif not model_association:
            tn += 1

        else:
            fp += len(model_association)

    precision = tp / (tp + fp)

    recall = tp / (tp + fn)

    f1_score = 2* ((precision * recall) / (precision + recall))

    print("Precision: ", precision)
    print("recall: ", recall)
    print("F1 Score:", f1_score)

    confusion_matrix = np.array(([tp, fp], [fn, tn]))

    print("Confusion Matrix:", confusion_matrix)


if __name__ == "__main__":

    base_dir = os.getcwd()

    # reading config file
    config = configparser.ConfigParser()
    config.read("evaluationConfig.inf")

    section = config.sections()

    # storing section names into a list
    filepath = config.options(section[0])

    gtResult = config.get(section[0], filepath[0])
    modelResult = config.get(section[0], filepath[1])

    with open(modelResult, "r") as f:
        read_model_result = json.load(f)

    with open(gtResult, "r") as f:
        read_gt_result = json.load(f)

    evaluateModel(read_gt_result, read_model_result)
