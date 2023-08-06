#######################
## test_plotters.py  ##
#######################


# Usage:
# (...) $ cd <top_dir>
# (...) $ python rklearn/tests/test_plotters.py --conf=rklearn/tests/config/config.yaml

#############
## Imports ##
#############

import unittest

import os
import sys
import time
import argparse
import yaml

from rklearn.plotters import plot_learning_curves_cv_scores 
from rktools.loggers import init_logger
from rklearn.perceptron import Perceptron
from rklearn.opendata_loaders import load_iris_binary_data

CONF_FILE = "./config/config.yaml"

class TestPlotters(unittest.TestCase):

    def setUp(self):

        with open(CONF_FILE, 'r') as ymlfile:
            self.config = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.logger = init_logger(name="test_plotters", config=self.config)

        # config params
        self.csv_file = self.config["iris_binary_classifier"]["cvs_file"]
        self.features = self.config["iris_binary_classifier"]["features"]
        self.pos_class = self.config["iris_binary_classifier"]["pos_class"]
        self.neg_class = self.config["iris_binary_classifier"]["neg_class"]

        # hyperparams
        self.lr = self.config["perceptron_hyper"]["lr"]
        self.n_epochs = self.config["perceptron_hyper"]["n_epochs"]

        self.learning_curves_fig = self.config["perceptron_hyper"]["learning_curves_fig"].format(self.n_epochs, self.lr)
        
        # load the Iris data
        self.logger.info("Loading the Iris dataset...")
        start_prep = time.time()
        self.X, self.y = load_iris_binary_data(
            csv_file=self.csv_file,
            features=self.features,
            pos_class=self.pos_class,
            neg_class=self.neg_class,
            logger=self.logger
        )
        assert(self.X is not None)
        assert(self.y is not None)
        self.logger.info("self.X.shape = {}, self.y.shape = {}".format(self.X.shape, self.y.shape))
        end_prep = time.time()
        self.logger.info("Data loaded in {} seconds".format(end_prep - start_prep))

    def test_plot_learning_curves_scores(self):

        self.perceptron = Perceptron(lr=self.lr, n_epochs=self.n_epochs, ascii=True)

        start_lc = time.time()
        plot_learning_curves_cv_scores(self.perceptron,
                                       self.X, self.y,
                                       cv=5,
                                       title="Learning curves for Perceptron - epochs = {} - lr = {}".format(self.n_epochs, self.lr),
                                       logger=self.logger).savefig(self.learning_curves_fig, dpi=300)
 
        end_lc = time.time()
        self.logger.info("Learning curves saved in file  {} seconds".format(self.learning_curves_fig))
        self.logger.info("Learning curves computed in {} seconds".format(end_lc - start_lc))
        self.logger.info("End of test_plot_learning_curves_acc_score()")

    def test_plot_learning_curves_scores_2(self):

        self.perceptron = Perceptron(lr=self.lr, n_epochs=self.n_epochs, ascii=True)
        assert(self.perceptron is not None)

        self.logger.info("Draw only: learning curves + fit times vs data (e.g. scores_vs_fit_times = False)...")

        self.learning_curves_fig = self.learning_curves_fig[0:-4] + "_2.png" 
        
        start_lc = time.time()
        plot_learning_curves_cv_scores(
            self.perceptron,
            self.X, self.y,
            cv=5,
            scores_vs_fit_times=False,
            title="Learning curves for Perceptron - epochs = {} - lr = {}".format(self.n_epochs, self.lr),
            logger=self.logger).savefig(self.learning_curves_fig, dpi=300)
 
        end_lc = time.time()
        self.logger.info("Learning curves saved in file  {} seconds".format(self.learning_curves_fig))
        self.logger.info("Learning curves computed in {} seconds".format(end_lc - start_lc))

    def test_plot_learning_curves_scores_3(self):

        # the perceptron
        self.perceptron = Perceptron(lr=self.lr, n_epochs=self.n_epochs, ascii=True)

        self.logger.info("")
        self.logger.info("##########################################")
        self.logger.info("## test_plot_learning_curves_scores_3() ##")
        self.logger.info("##########################################")
        self.logger.info("")
        self.logger.info("Draw only: learning curves + scores vs fit times (e.g. fit_times_vs_data = False)...")

        self.learning_curves_fig = self.learning_curves_fig[0:-4] + "_3.png" 
        
        start_lc = time.time()
        plot_learning_curves_cv_scores(
            self.perceptron,
            self.X, self.y,
            cv=5,
            fit_times_vs_data=False,
            title="Learning curves for Perceptron - epochs = {} - lr = {}".format(self.n_epochs, self.lr),
            logger=self.logger).savefig(self.learning_curves_fig, dpi=300)
 
        end_lc = time.time()
        self.logger.info("Learning curves saved in file  {} seconds".format(self.learning_curves_fig))
        self.logger.info("Learning curves computed in {} seconds".format(end_lc - start_lc))

if __name__ == '__main__':
    unittest.main()


