import pyaudio
from time import sleep
import threading


def _thread_call_sound():
    while again:
        global stream
        myRates = [4185, 4700, 5275, 5590, 6270, 7040, 7900]
        for v_rate in myRates:
            stream = pyaudio.PyAudio().open(format=pyaudio.paInt8, channels=1, rate=v_rate, output=True)
            for beep_num in range(0, 2):
                for n in range(0, 100, 1):
                    stream.write("\x00\x30\x5a\x76\x7f\x76\x5a\x30\x00\xd0\xa6\x8a\x80\x8a\xa6\xd0")
        stream.close()
        pyaudio.PyAudio().terminate()


def play_incoming_call_sound():
    global again
    again = True
    thread_incoming_call_sound = threading.Thread(target=_thread_call_sound)
    thread_incoming_call_sound.start()


def stop_incoming_call_sound():
    global again
    again = False


# def start_ring(py_audio, buffer):
#     print("Vou falar")
#     ring_output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=2092, channels=2,
#                                        frames_per_buffer=buffer)
#     while True:
#         for n in range(600):
#             ring_output_stream.write("\x00\x30\x5a\x76\x7f\x76\x5a\x30\x00\xd0\xa6\x8a\x80\x8a\xa6\xd0")
#         sleep(3)