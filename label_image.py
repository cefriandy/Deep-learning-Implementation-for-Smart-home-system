from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os, random,subprocess
import sys
import imutils
import time
import serial
import playsound
from gtts import gTTS
import uuid
import numpy as np
import tensorflow as tf
import speech_recognition as sr
import matplotlib.pyplot as plt

arduino = serial.Serial('COM6', 9600)
time.sleep(2)
print("connected to arduino")


def speak(text):
    save_path = 'data voice'
    tts = gTTS(text=text, lang="id")
    filename = os.path.join(save_path, str(uuid.uuid4()) + ".mp3")
    tts.save(filename)
    playsound.playsound(filename)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("say something!")
        song_name1 = "nada1.mp3"
        playsound.playsound(song_name1)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            song_name2 = "nada2.mp3"
            playsound.playsound(song_name2)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
                                input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels=3,
                                           name='png_reader')
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                      name='gif_reader'))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels=3,
                                            name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)

    return result


def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label


def security():
    file_name = "test.jpg"
    model_file = "retrained_graph.pb"
    label_file = "retrained_labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = 'Mul'
    output_layer = "final_result"

    return file_name, model_file, label_file, input_height, input_width, input_mean, input_std, input_layer, output_layer


def facialexpression():
    file_name = "test.jpg"
    model_file = "retrained_graphface.pb"
    label_file = "retrained_labelsface.txt"
    input_height = 224
    input_width = 224
    input_mean = 128
    input_std = 128
    input_layer = "input"
    output_layer = "final_result"

    return file_name, model_file, label_file, input_height, input_width, input_mean, input_std, input_layer, output_layer


def test(self):
    verify = 1

    if verify == 1:
        file_name, model_file, label_file, input_height, input_width, input_mean, input_std, input_layer, output_layer = security()
        parser = argparse.ArgumentParser()
        parser.add_argument("--image", help="image to be processed")
        parser.add_argument("--graph", help="graph/model to be executed")
        parser.add_argument("--labels", help="name of file containing labels")
        parser.add_argument("--input_height", type=int, help="input height")
        parser.add_argument("--input_width", type=int, help="input width")
        parser.add_argument("--input_mean", type=int, help="input mean")
        parser.add_argument("--input_std", type=int, help="input std")
        parser.add_argument("--input_layer", help="name of input layer")
        parser.add_argument("--output_layer", help="name of output layer")
        args = parser.parse_args()

        if args.graph:
            model_file = args.graph
        if args.image:
            file_name = args.image
        if args.labels:
            label_file = args.labels
        if args.input_height:
            input_height = args.input_height
        if args.input_width:
            input_width = args.input_width
        if args.input_mean:
            input_mean = args.input_mean
        if args.input_std:
            input_std = args.input_std
        if args.input_layer:
            input_layer = args.input_layer
        if args.output_layer:
            output_layer = args.output_layer

        graph = load_graph(model_file)
        t = read_tensor_from_image_file(file_name,
                                        input_height=input_height,
                                        input_width=input_width,
                                        input_mean=input_mean,
                                        input_std=input_std)

        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name);
        output_operation = graph.get_operation_by_name(output_name);

        with tf.Session(graph=graph) as sess:
            start = time.time()
            global hasil
            hasil = sess.run(output_operation.outputs[0],
                             {input_operation.outputs[0]: t})
            end = time.time()
        hasil = np.squeeze(hasil)

        global top_h
        top_h = hasil.argsort()[-5:][::-1]
        labels = load_labels(label_file)
    verify += 1

    if verify == 2:
        file_name, model_file, label_file, input_height, input_width, input_mean, input_std, input_layer, output_layer = facialexpression()
        parser = argparse.ArgumentParser()
        parser.add_argument("--image", help="image to be processed")
        parser.add_argument("--graph", help="graph/model to be executed")
        parser.add_argument("--labels", help="name of file containing labels")
        parser.add_argument("--input_height", type=int, help="input height")
        parser.add_argument("--input_width", type=int, help="input width")
        parser.add_argument("--input_mean", type=int, help="input mean")
        parser.add_argument("--input_std", type=int, help="input std")
        parser.add_argument("--input_layer", help="name of input layer")
        parser.add_argument("--output_layer", help="name of output layer")
        args = parser.parse_args()

        if args.graph:
            model_file = args.graph
        if args.image:
            file_name = args.image
        if args.labels:
            label_file = args.labels
        if args.input_height:
            input_height = args.input_height
        if args.input_width:
            input_width = args.input_width
        if args.input_mean:
            input_mean = args.input_mean
        if args.input_std:
            input_std = args.input_std
        if args.input_layer:
            input_layer = args.input_layer
        if args.output_layer:
            output_layer = args.output_layer

        graph = load_graph(model_file)
        t = read_tensor_from_image_file(file_name,
                                        input_height=input_height,
                                        input_width=input_width,
                                        input_mean=input_mean,
                                        input_std=input_std)

        input_name = "import/" + input_layer
        output_name = "import/" + output_layer
        input_operation = graph.get_operation_by_name(input_name);
        output_operation = graph.get_operation_by_name(output_name);

        with tf.Session(graph=graph) as sess:
            start = time.time()
            results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
            end = time.time()
        results = np.squeeze(results)

        top_k = results.argsort()[-5:][::-1]
        labels = load_labels(label_file)

        # print(hasil)
        # print(results)

        i = hasil[0]
        i *= 100
        if i >= 80:
            print('Pemilik Rumah!')
            speak("selamat datang di rumah")
            c = results[0]
            c *= 100
            d = results[1]
            d *= 100
            e = results[2]
            e *= 100
            f = results[3]
            f *= 100
            for a in top_k:
                if a == 0 and c > e and c > d and c > f:
                    print(labels[0], results[0])
                    arduino.write(str.encode('a'))
                    speak("hei, tenang!!")
                    text = get_audio()
                    speak("mau hidupin tv?")
                    if "iya" in text or "ya" in text:
                        speak("Opening TV")
                    elif "tidak" in text or "gak" in text:
                        speak("ok")

                if a == 1 and d > c and d > e and d > f:
                    print(labels[1], results[1])
                    arduino.write(str.encode('h'))
                    speak("kamu terlihat senang")
                    mp = 'C:/Program Files (x86)/Windows Media Player/wmplayer.exe'
                    randomfile = random.choice(os.listdir("C:/Users/ceff/Desktop/mama/happy/"))
                    print('I will play song for you :' + randomfile)
                    file = ('C:/Users/ceff/Desktop/mama/happy/' + randomfile)
                    subprocess.call([mp, file])

                if a == 2 and e > c and e > d and e > f:
                    print(labels[2], results[2])

                if a == 3 and f > c and f > d and f > e:
                    print(labels[3], results[3])
                    speak("kamu sedih, tenang")
                    arduino.write(str.encode('S'))
                    text = get_audio()
                    speak("ingin memutar sesuatu ?")
                    if "music" in text:
                        speak("memutar music")
                        mp = 'C:/Program Files (x86)/Windows Media Player/wmplayer.exe'
                        randomfile = random.choice(os.listdir("C:/Users/ceff/Desktop/mama/sad/"))
                        print('I will play song for you :' + randomfile)
                        file = ('C:/Users/ceff/Desktop/mama/sad/' + randomfile)
                        subprocess.call([mp, file])
                    elif "No" in text or "no" in text:
                        speak("ok")

            plt.scatter(labels, results)
            plt.plot(1, 4, label='data', zorder=3)
            plt.ylim(-1, 2)
            plt.xlabel('Facial expression Label')
            plt.ylabel('Prediction Result')
            l = plt.legend(loc='upper right')
            l.set_zorder(20)
            plt_path = 'data image graph'
            cef = os.path.join(plt_path, str(uuid.uuid4()) + ".png")
            plt.savefig(cef)

        else:
            print('not matches')
            speak("kamu bukan pemilik. coba lagi")

