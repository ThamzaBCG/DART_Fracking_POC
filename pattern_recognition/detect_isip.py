
import pandas as pd
import numpy as np

from src.config import config

import src.constants.datasets as ds
import src.constants.query_parameters as q
import src.constants.general as g
import src.constants.completion_columns as cc

from pattern_recognition.isip import flagging_isip


def main(df):

    df = flagging_isip(df)


if __name__ == '__main__':
    main()