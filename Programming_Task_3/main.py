import io
import os
from Perceptron import Perceptron


def main():

    print('Choose mode: ')
    print('\t• write \'f\' to select prepared text from files')
    print('\t• write \'i\' to write your own input text')
    mode = input('Enter: ')

    if mode == 'f':
        training_folder = 'data/training/'
        training_dict, available_languages = get_paths_from_folder(training_folder)

        test_folder = 'data/test/'
        test_dict, available_languages = get_paths_from_folder(test_folder)

        training_data = get_data_from_dict(training_dict)
        test_data = get_data_from_dict(test_dict)

        training_package = get_training_package(training_data)

        print('Choose language ( available languages: ', available_languages, ' )')
        lang_tag = input('Enter: ')
        lang_tag = lang_tag.strip()
        execute_perceptron_from_file(training_package, test_data, lang_tag)

    else:
        if mode == 'i':
            training_folder = 'data/training/'
            training_dict, available_languages = get_paths_from_folder(training_folder)
            training_data = get_data_from_dict(training_dict)
            training_package = get_training_package(training_data)

            print('available languages for determining: ', available_languages)
            print('Provide text to discover its language: ')
            text = input()
            file = io.open('data/short_text/tmp/input.txt', 'w', encoding="utf8")
            file.write(text)
            file.close()
            test_dict, available_languages = get_paths_from_folder('data/short_text/')
            test_data = get_data_from_dict(test_dict)
            execute_perceptron_from_file(training_package, test_data, 'tmp')


def execute_perceptron_from_file(training_package, test_data, lang_package):
    predictions = list()
    for i in training_package.keys():
        perceptron = Perceptron(i)
        prediction = dict()
        prediction[i] = perceptron.perceptron(training_package[i], get_test_data_of_language(test_data, lang_package))
        predictions.append(prediction)

    language_name = ''
    sum_of_probabilities = float(0)
    greatest_probability = float(0)
    for i in predictions:
        for j in i.keys():
            sum_of_probabilities += i[j][0]
            if greatest_probability < i[j][0]:
                language_name = j
                greatest_probability = i[j][0]

    # normalize output
    normalizer = 1 / sum_of_probabilities
    for i in predictions:
        for j in i.keys():
            i[j][0] = i[j][0] * normalizer

    # greatest_probability = float(0)
    # for i in predictions:
    #     for j in i.keys():
    #         if greatest_probability < i[j][0]:
    #             greatest_probability = i[j][0]

    for i in predictions:
        for j in i.keys():
            i[j][0] = str(float(round(i[j][0] * 100, 2))) + ' %'

    greatest_probability = str(float(round(greatest_probability * 100, 2))) + ' %'

    print(predictions)

    print('The greatest probability among all perceptrons is:', greatest_probability,
          'of perceptron of language: ', language_name)


def get_training_package(training_data):
    first_lang = ''
    for i in training_data.keys():
        first_lang = training_data[i]
        break

    training_package = dict()
    for i in training_data.keys():
        if training_data[i] == first_lang:
            lang_tag = training_data[i]
            training_package[lang_tag] = extract_training_data_of_language(training_data, lang_tag)
        else:
            if training_data[i] != lang_tag:
                lang_tag = training_data[i]
                training_package[lang_tag] = extract_training_data_of_language(training_data, lang_tag)
            else:
                continue
    return training_package


def get_data_from_dict(_dict):
    data = dict()
    for k in _dict.keys():
        # print(k, _dict[k])
        tmp = open(k, encoding="utf8")
        tmp = prepare_text(tmp)
        tmp = counter(tmp)
        data[str(tmp)] = _dict[k]

    # for i in data.keys():
    #     print(i, data[i])

    return data


def get_paths_from_folder(folder):
    folders = os.listdir(folder)

    available_languages = list()
    _dict = dict()
    for i in folders:
        language_folder = os.listdir(folder + i + '/')
        # print(language_folder, i)
        files_per_language = len(language_folder)
        available_languages.append(i)
        for j in language_folder:
            # print(folder + i + '/' + j)
            _dict[folder + i + '/' + j] = i
            # f = open(training_folder + i + '/' + j)
            # for k in f:
            #     print(k)

    # print("------------------")
    return _dict, available_languages


def extract_training_data_of_language(training_data, lang_tag):
    dataset = list()
    for i in training_data.keys():
        tmp_set = list()
        # tmp = (''.join(j for j in i if ord(j) == '[' or ord(j) == ']'))
        tmp = i.replace('[', '').replace(']', '').replace(' ', '')
        if training_data[i] == lang_tag:
            for j in tmp.split(','):
                tmp_set.append(float(j))
        else:
            arr = tmp.split(',')
            for j in arr:
                if j == arr[-1]:
                    tmp_set.append(float(0))
                else:
                    tmp_set.append(float(j))
        dataset.append(tmp_set)
    return dataset


def get_test_data_of_language(test_data, lang_tag):
    dataset = list()
    for i in test_data.keys():
        if test_data[i] == lang_tag:
            tmp_set = list()
            # tmp = (''.join(j for j in i if ord(j) == '[' or ord(j) == ']'))
            tmp = i.replace('[', '').replace(']', '').replace(' ', '')
            for j in tmp.split(','):
                tmp_set.append(float(j))
            dataset.append(tmp_set)
    return dataset


def prepare_text(data):
    parts = list()
    for i in data:
        parts.append(''.join(j for j in i if 64 < ord(j) < 91 or 96 < ord(j) < 123).lower())
    return parts


def counter(data):
    occurrences = dict()
    for i in range(97, 123):
        occurrences[chr(i)] = 0
    data = ''.join(data)
    for i in data:
        occurrences[i] += 1
    dataset = list()
    total_chars = 0
    for k in occurrences.keys():
        total_chars += occurrences[k]
        dataset.append(occurrences[k])
    # print(total_chars)
    dataset.append(1)
    # for i in range(len(dataset)):
    for i in range(len(dataset) - 1):
        dataset[i] = dataset[i] / total_chars
    return dataset


if __name__ == '__main__':
    main()
