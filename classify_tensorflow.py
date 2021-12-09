#!/usr/bin/env python3
# Tensorflow classification that uses .h5 and .json

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import string
import random
import numpy
import argparse
import tensorflow as tf
import tensorflow.keras as keras
import pandas as pd

# import tensorflow as tf

def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:, 0]
    return ''.join([characters[x] for x in y])


def predict_with_model(model, image, captcha_symbols):

    prediction = model.predict(image)
    prediction = decode(captcha_symbols, prediction).replace('s', '')
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


    symbols_captcha = "%{}[]\>()#:+-0123456789ABCDeFghjkMnPQRSTUVWXYZs"
    symbols_length_model = "ns"

    print("Classifying captchas with symbol set {" + symbols_captcha + "}")

    model_1_and_2_name = "model_1_2"
    model_3_name = "model_3"
    model_4_name = "model_4"
    model_5_name = "model_5"
    model_6_name = "model_6"

    with tf.device('/cpu:0'):
        with open(args.output + '.csv', 'w') as output_file:
            json_file = open(args.model_name+'.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model = keras.models.model_from_json(loaded_model_json)
            model.load_weights(args.model_name+'.h5')
            model.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])

            json_file = open(model_1_and_2_name + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model_1_and_2 = keras.models.model_from_json(loaded_model_json)
            model_1_and_2.load_weights(model_1_and_2_name + '.h5')
            model_1_and_2.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])

            json_file = open(model_3_name + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model_3 = keras.models.model_from_json(loaded_model_json)
            model_3.load_weights(model_3_name + '.h5')
            model_3.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])

            json_file = open(model_4_name + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model_4 = keras.models.model_from_json(loaded_model_json)
            model_4.load_weights(model_4_name + '.h5')
            model_4.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])


            json_file = open(model_5_name + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model_5 = keras.models.model_from_json(loaded_model_json)
            model_5.load_weights(model_5_name + '.h5')
            model_5.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])


            json_file = open(model_6_name + '.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model_6 = keras.models.model_from_json(loaded_model_json)
            model_6.load_weights(model_6_name + '.h5')
            model_6.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])


            for x in os.listdir(args.captcha_dir):
                # load image and preprocess it
                raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
                rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
                rgb_data = cv2.medianBlur(rgb_data, 5)
                image = numpy.array(rgb_data) / 255.0
                (c, h, w) = image.shape
                image = image.reshape([-1, c, h, w])
                prediction = model.predict(image)
                prediction = decode(symbols_length_model, prediction).replace('s', '')

                pred_length = 0
                for i in range(len(prediction)):
                    if prediction[i] == 'n': pred_length += 1

                if pred_length == 1 or pred_length == 2:
                    prediction = predict_with_model(model_1_and_2, image, symbols_captcha)
                    output_file.write(x + "," + str(prediction) + "\n")
                    print('Classified ' + x)

                elif pred_length == 3:
                    prediction = predict_with_model(model_3, image, symbols_captcha)
                    output_file.write(x + "," + str(prediction) + "\n")
                    print('Classified ' + x)

                elif pred_length == 4:
                    prediction = predict_with_model(model_4, image, symbols_captcha)
                    output_file.write(x + "," + str(prediction) + "\n")
                    print('Classified ' + x)

                elif pred_length == 5:
                    prediction = predict_with_model(model_5, image, symbols_captcha)
                    output_file.write(x + "," + str(prediction) + "\n")
                    print('Classified ' + x)

                elif pred_length == 6:
                    prediction = predict_with_model(model_6, image, symbols_captcha)
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


