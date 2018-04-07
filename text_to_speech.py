# coding=utf-8
from __future__ import print_function
import json
from watson_developer_cloud import TextToSpeechV1
import text_scraper

text_to_speech = TextToSpeechV1(
    username='7d084eb0-c888-4d0d-b0cf-1220faa2114a',
    password='IYlMgOjMZEHk')


# print(json.dumps(text_to_speech.list_voices(), indent=2))

def text_to_speech_string(text_string, filename, voice):
    with open(filename, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                text_string, accept='audio/wav',
                voice=voice).content)


def text_to_speech_list(text_list, filename_base, voice):
    filenames = []
    filename_ext = '.wav'
    for i, text in enumerate(text_list):
        filename = filename_base + '_' + str(i) + filename_ext
        filenames.append(filename)
        print(len(text.encode('utf-8')))
        with open(filename, 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    text, accept='audio/wav', voice=voice).content)
    return filenames


def get_voice_list():
    de_voices = {'Birgit': 'de-DE_BirgitVoice',
                 'Dieter': 'de-DE_DieterVoice'}
    en_voices = {'Kate': 'en-GB_KateVoice',
                 'Allison': 'en-US_AllisonVoice',
                 'Lisa': 'en-US_LisaVoice',
                 'Michael': 'en-US_MichaelVoice'}
    es_voices = {'Laura': 'es-ES_LauraVoice',
                 'Enrique': 'es-ES_EnriqueVoice',
                 'Sofia-LA': 'es-LA_SofiaVoice',
                 'Sofia-US': 'es-US_SofiaVoice'}
    fr_voices = {'Renee': 'fr-FR_ReneeVoice'}
    it_voices = {'Francesca': 'it-IT_FrancescaVoice'}
    ja_voices = {'Emi': 'ja-JP_EmiVoice'}
    pt_voices = {'Isabela': 'pt-BR_IsabelaVoice'}

    voices_by_language = {'English': en_voices, 'German': de_voices,
                          'Spanish': es_voices, 'French': fr_voices,
                          'Italian': it_voices, 'Japanese': ja_voices,
                          'Portugese': pt_voices}
    return voices_by_language


if __name__ == '__main__':
    # pdf_filename = 'Lecture11.pdf'
    pptx_filename = 'graphics.pptx'
    docx_filename = 'Documentation.docx'

    text_string = text_scraper.read_pptx(pptx_filename)
    text_list = text_scraper.read_docx(docx_filename)

    filename_string = 'output_string.wav'
    filename_list = 'output_list'

    voices = get_voice_list()

    print(text_list[0])

    text_to_speech_string(text_string, filename_string,
                          voices['English']['Michael'])
    text_to_speech_list(text_list, filename_list, voices['Japanese']['Emi'])

# print(json.dumps(text_to_speech.get_pronunciation('Watson', format='spr'),
#                  indent=2))


# print(json.dumps(text_to_speech.list_voice_models(), indent=2))

# print(json.dumps(text_to_speech.create_customization('test-customization'),
#  indent=2))

# print(text_to_speech.update_customization('YOUR CUSTOMIZATION ID',
# name='new name'))

# print(json.dumps(text_to_speech.get_customization('YOUR CUSTOMIZATION ID'),
#  indent=2))

# print(json.dumps(text_to_speech.get_customization_words('YOUR CUSTOMIZATION
#  ID'), indent=2))

# print(text_to_speech.add_customization_words('YOUR CUSTOMIZATION ID',
#                                              [{'word': 'resume',
# 'translation': 'rɛzʊmeɪ'}]))

# print(text_to_speech.set_customization_word('YOUR CUSTOMIZATION ID',
# word='resume',
#                                             translation='rɛzʊmeɪ'))

# print(json.dumps(text_to_speech.get_customization_word('YOUR CUSTOMIZATION
# ID', 'resume'), indent=2))

# print(text_to_speech.delete_customization_word('YOUR CUSTOMIZATION ID',
# 'resume'))

# print(text_to_speech.delete_customization('YOUR CUSTOMIZATION ID'))
