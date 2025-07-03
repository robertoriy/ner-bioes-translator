from app.handlers.back_translation_evaluation_handler import back_translation_evaluations
from app.handlers.config_handler import config_handler
from app.handlers.df_handler import df_handler, result_df_handler
from app.handlers.expert_evaluation_handler import expert_evaluations
from app.services.back_translation_service import back_translator
from app.services.bioes_translation_service import bioes_translator


def get_config_handler():
    return config_handler

def get_df_handler():
    return df_handler

def get_result_df_handler():
    return result_df_handler

def get_expert_evaluations():
    return expert_evaluations


def get_bioes_translator():
    return bioes_translator

def get_back_translator():
    return back_translator