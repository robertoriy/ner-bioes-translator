class DataFrameParser:
    def __init__(self):
        pass

    @classmethod
    def parse_df_sentence_bioes(cls, sentence_df):
        bioes = list(zip(sentence_df['Word'], sentence_df['BIOES-Tag']))
        text_bioes = ''

        for word, tag in bioes:
            text_bioes = text_bioes + ' ' + word + ' (' + tag + ')'

        text_bioes = text_bioes.strip()
        return text_bioes

    @classmethod
    def parse_tags_from_string(cls, sentence_bioes):
        tokens = sentence_bioes.split()
        result = []

        for i in range(0, len(tokens), 2):
            if i + 1 >= len(tokens):
                break

            word = tokens[i]
            tag = tokens[i + 1].strip("(),!.?-")

            result.append((word, tag))

        return result

# df_parser = DataFrameParser()