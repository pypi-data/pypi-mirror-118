# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import nwae.math.Cluster as clst
from nwae.utils.Log import Log
from inspect import currentframe, getframeinfo
from nwae.lang.model.WordFreqDocMatrix import WordFreqDocMatrix


#
# NOTE: This Class is NOT Thread Safe
#
class TxtCluster:

    #
    # Initialize with a list of text, assumed to be already word separated by space.
    #
    def __init__(
            self,
            # A list of text sentences in list type, already in lowercase and cleaned of None or ''.
            # Preprocessing assumed to be done and no text processing will be done here.
            sentences_list,
    ):
        self.sentences_list = sentences_list
        Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Sentences list (before filter):\n\r' + str(self.sentences_list)
        )
        return

    #
    # The main clustering function
    #
    def cluster_text(
            self,
            word_freq_doc_matrix,
            keywords_list,
            ncenters,
            iterations = 50,
            words_per_topic = 20,
    ):
        #
        # From the sentence matrix, we can calculate the IDF
        #
        # Do a redundant multiplication so that a copy is created, instead of pass by reference
        sentence_matrix = np.transpose(word_freq_doc_matrix)

        retval_cluster = clst.Cluster.cluster(
            matx          = sentence_matrix,
            feature_names = keywords_list,
            ncenters      = ncenters,
            iterations    = iterations
        )
        # Relative to sentence_matrix, shape is (n_documents,)
        # It will return a tuple of a single object (numpy ndarray)
        # e.g. ( array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1], dtype=int32), )
        doc_labels = retval_cluster.np_cluster_labels[0]
        # Relative to keywords_list, shape is (n_clusters, n_words_in_keywords_list)
        doc_centers = retval_cluster.np_cluster_centers

        Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Doc labels, shape ' + str(doc_labels.shape) + ': ' + str(doc_labels)
        )
        Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Doc centers, shape ' + str(doc_centers.shape) + ': ' + str(doc_centers)
        )

        """
        Extract top words from each cluster center
        """
        df = pd.DataFrame(doc_centers)
        df.columns = keywords_list
        print(df)

        np_keyword = np.array(keywords_list)
        n_print_how_many = min(20, len(keywords_list))
        words_values = []
        words_per_topic = min(words_per_topic, len(keywords_list))
        for center in doc_centers:
            # To sort descending, we need to flip, as argsort() by default sorts ascending
            center_idx_sort = np.flip(np.argsort(center))
            center_idx_sort_keywords = np_keyword[center_idx_sort]
            center_idx_sort_values   = center[center_idx_sort]
            wv = dict(zip(center_idx_sort_keywords[0:words_per_topic].tolist(), center_idx_sort_values[0:words_per_topic].tolist()))
            words_values.append(wv)
            Log.info(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': For center ' + str(center[0:n_print_how_many])
                + '\n\rsorted to\n\r' + str(center_idx_sort[0:n_print_how_many])
                + '\n\rtop keywords-values\n\r' + str(wv)
            )

        return words_values, doc_labels, doc_centers


if __name__ == '__main__':
    Log.DEBUG_PRINT_ALL_TO_SCREEN = True
    Log.LOGLEVEL = Log.LOG_LEVEL_DEBUG_1
    from bot.nlu.lang.preprocess.TextPrepscr import TextPreprepscr

    corpora = 'japchat'
    if corpora == 'test':
        from bot.nlu.lang.corpora.TestCorpora import TestCorpora
        sample_fpath = 'sample.txt'
        tc = TestCorpora()
        sentences_list = tc.test_corpora_general(
            data_from_internet = False,
            write_to_file_path = sample_fpath,
            sample_fpath       = sample_fpath
        )
    elif corpora == 'japchat':
        from bot.nlu.lang.corpora.LivePersonChat import LivePersonChat
        lpc = LivePersonChat(filepath='/usr/local/git/helix-global-llc/bot.nlu/data/sample.chat.jap.csv')
        data = lpc.get_chat_lines(speaker_category=LivePersonChat.SPEAKER_CATEGORY_CLIENT)
        sentences_list = list(data[LivePersonChat.COL_CONTENT])
        # Don't process too much for demo
        sentences_list = sentences_list[0:min(500,len(sentences_list))]
    else:
        raise Exception('??')

    tpp = TextPreprepscr()
    sent_processed = tpp.preprocess_list(
        sentences_list = sentences_list,
    )
    print('Processed sentences: ' + str(sent_processed))

    docmodel = WordFreqDocMatrix()
    wordfreq_doc_matrix, keywords_list = docmodel.get_word_doc_matrix(
        sentences_list = sent_processed,
        # It seems sigmoid-freq-normalized outperforms log-freq-normalized, and for sure the original weak freq
        freq_measure   = WordFreqDocMatrix.BY_SIGMOID_FREQ_NORM,
        remove_quartile_keywords = 0,
    )
    cl = TxtCluster(sentences_list = sent_processed)
    words_values, cluster_labels, cluster_centers = cl.cluster_text(
        word_freq_doc_matrix = wordfreq_doc_matrix,
        keywords_list = keywords_list,
        ncenters = 10,
    )

    for label_idx in range(np.max(cluster_labels)+1):
        print('Cluster #' + str(label_idx))
        print('\tWord-Value Center: ' + str(words_values[label_idx]))
        for j in range(len(sentences_list)):
            if cluster_labels[j] == label_idx:
                # s = sent_processed[j].copy()
                # s.sort()
                # print('\t' + str(s))
                print('\t\t' + str(sentences_list[j]))

    exit(0)
