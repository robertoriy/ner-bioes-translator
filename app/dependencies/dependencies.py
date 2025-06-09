from app.services.config_handler import config_handler
from app.services.df_handler import df_handler
from app.services.evaluation_score_handler import scores
from app.services.translator import translator


def get_config_handler():
    return config_handler

def get_df_handler():
    return df_handler

def get_result_df_handler():
    return df_handler

def get_sentence_scores():
    return scores

def get_translator():
    return translator