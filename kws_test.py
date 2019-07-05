
import os
from pocketsphinx import pocketsphinx
from sphinxbase import sphinxbase
import pyaudio
from xml_parser import get_config_xml
import pyttsx3


class kws_detect(object):
    def __init__(self, config_xml='config.xml'):
        (dns, words) = get_config_xml(config_xml)
        self.dns = dns
        self.words = words
        self.key_file = 'keylist'

    def run(self):
        if len(self.words) == 0:
            print('There is no words-list to be detected.\nPlease fill in config.xml.')
            return
        # write keyword list to file
        if os.path.exists(self.key_file):
            os.remove(self.key_file)
        with open(self.key_file, 'w') as f:
            for word in self.words:
                f.write("{} /1e10/\n".format(word))
            f.close()
        
        self.start_keyphrase_detection(self.callback_function, self.words)

    def start_keyphrase_detection(self, keyphrase_function, key_phrase):
        modeldir = "models"

        config = pocketsphinx.Decoder.default_config()
        config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us-ptm'))
        config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
        config.set_string('-kws', 'keylist')
        # config.set_string('-keyphrase', key_phrase)
        config.set_string('-logfn', './log')
        config.set_float('-kws_threshold', 1e10)

        # Start a pyaudio instance
        p = pyaudio.PyAudio()

        # Create an input stream with pyaudio
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        # Start the stream
        stream.start_stream()

        # Process audio chunk by chunk. On keyword detected perform action and restart search
        decoder = pocketsphinx.Decoder(config)
        decoder.start_utt()

        print('start listening...')

        while True:
            buf = stream.read(1024)
            if buf:
                decoder.process_raw(buf, True, True)
            else:
                break
            hyp = decoder.hyp()
            if  hyp is not None:
                keyphrase_function(hyp.hypstr)
                # Stop and reinitialize the decoder
                decoder.end_utt()
                decoder.start_utt()

    def callback_function(self, kword):
        result = "\"{}\" detected!".format(kword)
        print(result)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
        
        engine.say(result)
        engine.runAndWait()

        """
        voices[0]: male
        voices[-1]: female
        engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        engine.setProperty('volume', 0.9)  # Volume 0-1
        """


