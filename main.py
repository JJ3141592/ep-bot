from selenium import webdriver
import time
import listcompile
import pyautogui
import keyboard
import pyperclip as pc
import os

pyautogui.PAUSE = 0

target = input('Task URL: ')
langTarget = input('Input answer in Reading(1) or Writing(2) mode? ')
listloc = input(f'Path of list (Program saved at {__file__}, default to List.txt): ')
if listloc == '':
    listloc = 'List.txt'

p = os.path.dirname(__file__)
if input('Compile new list? '):
    listcompile.compile_list(p + r'\Snapshots\EP.txt', listloc)

l = open(listloc, mode='r', encoding='utf-16')
listWords = l.read()
listWords = listWords.replace('!BaseLanguage\n', '').replace('!TargetLanguage\n', '!TargetLanguage').split('!TargetLanguage')

baseWords = listWords[0].split('\n')
baseWords = [i.rstrip() for i in baseWords]
targetWords = listWords[1].split('\n')
targetWords = [i.rstrip() for i in targetWords]

print('Number of words:', len(baseWords) - 1)

#print(listWords)
    
browser=webdriver.Firefox() # CHANGE BACK TO FIREFOX ASAP (or not)
browser.get(target)
input('Waiting for ready. Press enter when done. ')
pyautogui.click()
time.sleep(1)
hackRunning = True

sleepTime = 0.25 # set to 0.31 for dash

lastWord = 'foo bar spam splat'

while True:
    if keyboard.is_pressed('esc'):
        hackRunning = not hackRunning
        print(f'hackRunning is {str(hackRunning)}')
        while keyboard.is_pressed('esc'):
            pass
    if hackRunning:
        html = browser.page_source[3730000:3800000]
        try:
            try:
                index = html.index('<span id="question-text" ng-click="self.onRefreshClick()" class="native-font">') + len('<span id="question-text" ng-click="self.onRefreshClick()" class="native-font">')
                word = html[index:].split('<')[0].replace(';', '').split('(')[0].rstrip()
                if word == '':
                    raise
            except:
                try:
                    index = html.index('''<span style="color: #F80; border-bottom: null">''') + len('''<span style="color: #444; border-bottom: null">''')
                    word = html[index:].split('<')[0].replace(';', '').split('(')[0].rstrip()
                except:
                    index = html.index('''<span style="color: #444; border-bottom: null">''') + len('''<span style="color: #444; border-bottom: null">''')
                    word = html[index:].split('<')[0].replace(';', '').split('(')[0].rstrip()
            if word.endswith(','):
                word = word[:-1]
            print('WORD:' + word)
            if True:
                if langTarget == '1': # Output in English
                    if word in targetWords:
                        answer = baseWords[targetWords.index(word)]
                    else:
                        answer = baseWords[targetWords.index(word.split(',')[0].rstrip())]
                    pc.copy(answer)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.write('\n')
                    time.sleep(sleepTime)

                if langTarget == '2': # Output in TargetLanguage
                    answer = targetWords[baseWords.index(word)]
                    pc.copy(answer)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.write('\n')
                    time.sleep(sleepTime)
            lastWord = word
        except ValueError:
            pass
