import time

find_all = lambda string_to_search, string_to_find: [i for i in range(len(string_to_search)) if string_to_search.startswith(string_to_find, i)]

def compile_list(location_html, location_save):
    fileIn = open(location_html, mode='r', encoding='utf-16').read()
    # Metadata for list

    URL = fileIn.split('\n')[0][fileIn.rfind('<!-- saved from url=') + 26:fileIn.split('\n')[0].rfind('-->')]
    
    fileOut = open(location_save, mode='w+', encoding='utf-16')
    contents = ''

    contents += '!BaseLanguage' # Search for words in base language (English)
    words = []
    indexes = find_all(fileIn, '<div class="baseLanguage question-label native-font ng-binding">')
    indexes = [i + 64 for i in indexes]
    for i in indexes:
        word = ''
        while fileIn[i] != '<' and fileIn[i] != ';':
            word += fileIn[i]
            i += 1
        words.append(word.split('(')[0].rstrip())
    for i in words:
        contents += '\n' + i

    contents += '\n!TargetLanguage' # Search for words in target language (Chinese, etc...)
    words = []
    indexes = find_all(fileIn, '<div class="targetLanguage question-label native-font ng-binding">')
    indexes = [i + 66 for i in indexes]
    for i in indexes:
        word = ''
        while fileIn[i] != '<' and fileIn[i] != ';':
            word += fileIn[i]
            i += 1
        words.append(word)
    for i in words:
        contents += '\n' + i
    
    fileOut.write(contents)
    print(URL)
