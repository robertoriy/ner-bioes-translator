import pandas as pd

from app.dependencies.dependencies import get_bioes_translator, get_config_handler
from app.utils.df_parser import DataFrameParser

class DataFrameProcessor:

    @classmethod
    def get_translations(cls, sentence_data, languages):
        config = get_config_handler().get_config()
        translator = get_bioes_translator()

        translations = {lang: {} for lang in languages}

        for sentence_name, data in sentence_data.items():
            original_sentence_bioes = DataFrameParser.parse_df_sentence_bioes(data)

            for language in languages:
                translated_sentence = translator.translate(original_sentence_bioes, language, config)

                updated_translated_sentence = DataFrameParser.remove_unnecessary_tags(translated_sentence)

                processed_sentence_bioes = DataFrameParser.parse_tags_from_string(updated_translated_sentence)

                translations[language][sentence_name] = processed_sentence_bioes

                plain_text = ''
                for word, tag in processed_sentence_bioes:
                    plain_text = plain_text + ' ' + word
                plain_text = plain_text.strip()
                print(f"Текущий перевод с удалением разметки - {plain_text}")

        return translations

    @classmethod
    def update_df(cls, df, unique_sentences, translations):
        original_lang_code = get_config_handler().get_config().prompt_data.get_original_language()

        filtered_df = df[df['Sentence'].isin(unique_sentences)].copy()
        new_word_name = f'Word_original_{original_lang_code}'
        new_tag_name = f'BIOES-Tag_original_{original_lang_code}'
        filtered_df = filtered_df.rename(columns={
            'Word': new_word_name,
            'BIOES-Tag': new_tag_name
        })
        return cls.add_translations_ordered(filtered_df, translations, original_lang_code)

    @classmethod
    def add_translations_ordered(cls, df, translations, og_lang):
        # Создаем список для хранения всех строк
        all_rows = []

        # Получаем уникальные предложения в порядке их появления
        sentences = df['Sentence'].unique()

        for sent in sentences:
            # Получаем все строки для текущего предложения из оригинального df
            original_rows = df[df['Sentence'] == sent].to_dict('records')

            # Определяем максимальное количество строк среди всех языков
            max_len = len(original_rows)
            for lang in translations.keys():
                if sent in translations[lang]:
                    max_len = max(max_len, len(translations[lang][sent]))

            # Создаем строки для текущего предложения
            for i in range(max_len):
                row = {'Sentence': sent}

                # Заполняем оригинальные данные (если есть)
                if i < len(original_rows):
                    row.update({
                        f'Word_original_{og_lang}': original_rows[i][f'Word_original_{og_lang}'],
                        f'BIOES-Tag_original_{og_lang}': original_rows[i][f'BIOES-Tag_original_{og_lang}']
                    })
                else:
                    row.update({
                        f'Word_original_{og_lang}': None,
                        f'BIOES-Tag_original_{og_lang}': None
                    })

                # Заполняем переводы для каждого языка
                for lang in translations.keys():
                    if sent in translations[lang] and i < len(translations[lang][sent]):
                        row[f'Word_{lang}'] = translations[lang][sent][i][0]
                        row[f'BIOES-Tag_{lang}'] = translations[lang][sent][i][1]
                    else:
                        row[f'Word_{lang}'] = None
                        row[f'BIOES-Tag_{lang}'] = None

                all_rows.append(row)

        # Создаем новый DataFrame
        new_df = pd.DataFrame(all_rows)
        return new_df

