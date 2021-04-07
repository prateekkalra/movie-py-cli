class bcolors:
    '''
    Bash script styling

    Source: https://stackoverflow.com/a/42449998/12537848
    '''
    
    HEADER = '\033[95m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    WARNING = '\033[93m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

class Cleaner:
    '''
    Get rid of useless contents
    '''

    def __init__(self):
        pass

    def text_cleaner(self, dict_cast):
        '''
        Gets rid of useless characters

        Input:
            :param: text -> A dictionary of movie casts to be gotten rid of the useless characters.
            :type: dict

        Returns:
            A cleaned string list
        '''
        cleaned_text = {}
        for item in dict_cast:
            pos = dict_cast[item].find('|')
            cleaned_text[item] = (dict_cast[item][:pos].strip())
        return cleaned_text