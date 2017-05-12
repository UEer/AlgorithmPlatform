from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import sys

#sys.path.append('/home/tensorflow/master/models-master/im2txt')
#print(sys.path)

os.environ["CUDA_VISIBLE_DEVICES"] = ""

import tensorflow as tf

from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary


class Im2txt:
    def __init__(self, checkpoint_path="/home/tensorflow/im2txt/model/train", vocab_file="/home/tensorflow/im2txt/data/mscoco/word_counts.txt"):

        tf.logging.set_verbosity(tf.logging.INFO)
        self.g = tf.Graph()
        with self.g.as_default():
            model = inference_wrapper.InferenceWrapper()
            restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
                                                       checkpoint_path)
        self.g.finalize()
        self.vocab = vocabulary.Vocabulary(vocab_file)
        self.sess = tf.Session(graph=self.g)
        restore_fn(self.sess)
        self.generator = caption_generator.CaptionGenerator(model, self.vocab)

    def main(self, filename):
        with tf.gfile.GFile(filename, "r") as f:
            image = f.read()
        captions = self.generator.beam_search(self.sess, image)
        for i, caption in enumerate(captions):
            # Ignore begin and end words.
            sentence = [self.vocab.id_to_word(w) for w in caption.sentence[1:-1]]
            sentence = " ".join(sentence)
            yield (sentence, math.exp(caption.logprob))
