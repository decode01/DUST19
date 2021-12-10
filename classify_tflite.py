#!/usr/bin/env python3
#Classification file to run on pi (tflite models)

# KEMAL SEDAT CEYHAN's tflite classification file for the project 2
# used for creating a peer-to-peer security protocol

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import string
import random
import numpy
import argparse
import tflite_runtime.interpreter as tflite
import pandas as pd

def decode(characters, y):
    y = numpy.squeeze(y)
    result = numpy.argmax(numpy.array(y))
    # y = numpy.argmax(numpy.array(y), axis=2)[:,0]

    return ''.join(characters[result]).replace('s', '')


def predict_with_model(model, image, captcha_symbols, captcha_length):
    interpreter = tflite.Interpreter(model_path=model)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()

    prediction = ""
    for i in range(captcha_length):
        char = interpreter.get_tensor(output_details[i]['index'])
        prediction += str(decode(captcha_symbols, char))

    return prediction


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    symbols_captcha = symbols_file.readline().strip()
    symbols_file.close()

    print("Classifying captchas with symbol set {" + symbols_captcha + "}")

    symbols_captcha = "%{}[]\>()#:+-0123456789ABCDeFghjkMnPQRSTUVWXYZs"
    symbols_length_model = "ns"

    model_1_and_2 = "model_1_2.tflite"
    model_3 = "model_3.tflite"
    model_4 = "model_4.tflite"
    model_5 = "model_5.tflite"
    model_6 = "model_6.tflite"
    model_length = args.model_name + '.tflite'

    with open(args.output + '.csv', 'w') as output_file:
        interpreter = tflite.Interpreter(model_path=model_length)
        interpreter.allocate_tensors()

        for x in os.listdir(args.captcha_dir):
            # load image and preprocess it
            raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
            rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
            rgb_data = cv2.medianBlur(rgb_data, 5)
            image = numpy.array(rgb_data) / 255.0
            (c, h, w) = image.shape
            image = image.reshape([-1, c, h, w]).astype('float32')

            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            interpreter.set_tensor(input_details[0]['index'], image)
            interpreter.invoke()

            char0 = interpreter.get_tensor(output_details[0]['index'])
            char1 = interpreter.get_tensor(output_details[1]['index'])
            char2 = interpreter.get_tensor(output_details[2]['index'])
            char3 = interpreter.get_tensor(output_details[3]['index'])
            char4 = interpreter.get_tensor(output_details[4]['index'])
            char5 = interpreter.get_tensor(output_details[5]['index'])

            prediction = str(decode(symbols_length_model, char0)) + str(decode(symbols_length_model, char1)) + \
                         str(decode(symbols_length_model, char2)) + str(decode(symbols_length_model, char3)) + \
                         str(decode(symbols_length_model, char4)) + str(decode(symbols_length_model, char5))

            pred_length = 0
            for i in range(len(prediction)):
                if prediction[i] == 'n': pred_length += 1

            if pred_length == 1 or pred_length == 2:
                prediction = predict_with_model(model_1_and_2, image, symbols_captcha, 2)
                output_file.write(x + "," + str(prediction) + "\n")
                print('Classified ' + x)

            elif pred_length == 3:
                prediction = predict_with_model(model_3, image, symbols_captcha, 3)
                output_file.write(x + "," + str(prediction) + "\n")
                print('Classified ' + x)

            elif pred_length == 4:
                prediction = predict_with_model(model_4, image, symbols_captcha, 4)
                output_file.write(x + "," + str(prediction) + "\n")
                print('Classified ' + x)

            elif pred_length == 5:
                prediction = predict_with_model(model_5, image, symbols_captcha, 5)
                output_file.write(x + "," + str(prediction) + "\n")
                print('Classified ' + x)

            elif pred_length == 6:
                prediction = predict_with_model(model_6, image, symbols_captcha, 6)
                output_file.write(x + "," + str(prediction) + "\n")
                print('Classified ' + x)


    with open(args.output + '.csv', 'r') as output_file:
        rows = output_file.readlines()
        #print(rows)
        sorted_rows = sorted(rows, key=lambda row: row.split(",")[0], reverse=False)
        for r in range(len(sorted_rows)):
            sorted_rows[r] = sorted_rows[r].replace(" ", "")
        with open(args.output + '_ordered.csv', 'w') as ordered_output_file:
            ordered_output_file.write("ceyhank" + '\n')
            for row in sorted_rows:
                ordered_output_file.write(row)


if __name__ == '__main__':
    main()



