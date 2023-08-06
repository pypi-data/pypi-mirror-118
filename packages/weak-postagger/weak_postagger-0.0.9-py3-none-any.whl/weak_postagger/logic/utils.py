import typing as tp
from weak_postagger.logic.param import FILE_NAME_DIVIDERS


def get_class_name_from_file(file_name: str) -> str:
    """
        Retrieves the POS Tag class name from the file name.

        This method expects that the file name will be of the format `classname_specifier.txt`

    :param file_name: The file name containing the POS Tag name.
    :type file_name: `str`
    :return: POS Tag class name as specified on the file name.
    :rtype: `str`
    """
    return file_name[:min(map(lambda x: (file_name.index(x) if (x in file_name) else len(file_name)),
                              FILE_NAME_DIVIDERS))]


def replace_abbreviations(sentence: tp.List[str], abbreviations: tp.Dict[str, str]) -> tp.List[str]:
    """
        Checks if there is abbreviated words on the sentence and replaces it with the full word.

    :param sentence: Sentence to be processed.
    :type sentence: `str`
    :param abbreviations: Dictionary containing word abbreviations and their full form.
    :type abbreviations: `tp.Dict[str, str]`
    :return: Sentence with all words in their full form.
    :rtype: `tp.List[str]`
    """
    modified_sentence = []
    for word in sentence:
        if word in abbreviations:
            modified_sentence += abbreviations[word].split()
        else:
            modified_sentence += [word]
    return modified_sentence
