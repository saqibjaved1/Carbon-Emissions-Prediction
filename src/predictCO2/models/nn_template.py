"""
Author: Saqib Javed
Date: 01/7/2020
"""

class NN_Template(object):
    def __init__(self, config):
        self.model = None
        self.config = config

    def build_model(self):
        """
        Method to create the model
        """
        raise NotImplementedError

    def save(self):
        """
        Saves the model checkpoint to the path specified by the argument
        """
        if self.model is None:
            raise Exception("Build the model first!")

        print("Saving model...")
        self.model.save_weights(self.config["model"]["checkpoint_path"])
        print("Model saved!")

    def load(self):
        """
        Loads the model checkpoint from the path specified by the argument
        """
        if self.model is None:
            raise Exception("Build the model first.")

        print("Loading model checkpoint {} ...\n".format(self.config["model"]["restore_model"]))
        self.model.load_weights(self.config["model"]["restore_model"])
        print("Model loaded!")
