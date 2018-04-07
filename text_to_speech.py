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


def get_voice_models_list():
    print(text_to_speech.list_voice_models('en-US'))


if __name__ == '__main__':
    # pdf_filename = 'Lecture11.pdf'
    pptx_filename = 'graphics.pptx'
    docx_filename = 'homework9.docx'

    text_string = text_scraper.read_pptx(pptx_filename)
    text_list = text_scraper.read_docx(docx_filename)

    filename_string = 'output_string.wav'
    filename_list = 'output_list'

    voice = 'en-US_AllisonVoice'
    get_voice_models_list()

    # text_to_speech_string(text_string, filename_string, voice)
    # text_to_speech_list(text_list, filename_list, voice)

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
