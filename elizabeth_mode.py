import time
import pyautogui
import cv2
import sys

from enum import Enum

pyautogui.FAILSAFE = True


class GameState(Enum):
    ToBattle = 'to_battle'
    Walking = 'walking'
    InBattle = 'in_battle'
    MissionClear = 'mission_clear'
    Complete = 'complete'
    Other = 'other'


def localeImage(image, confidence=0.7, grayscale=True):
    return pyautogui.locateOnScreen(image + '.png', confidence=confidence, grayscale=grayscale)


def clickImage(targetImage, confidence=0.7):
    location = localeImage(targetImage, confidence=confidence)
    if location is not None:
        x, y = pyautogui.center(location)
        pyautogui.click(x, y)
        pyautogui.PAUSE = 1.0
    return


def clickImageUntilSuccess(targetImage, confidence=0.7):
    location = None
    while location is None:
        print('...')
        location = localeImage(targetImage, confidence=confidence)
    x, y = pyautogui.center(location)
    pyautogui.click(x, y)
    pyautogui.PAUSE = 1.0
    return


def checkGameState():

    pyautogui.PAUSE = 2.0
    location = localeImage('.\\images\\general\\file', confidence=0.9)
    if location is not None:
        return GameState.ToBattle

    location = localeImage(
        '.\\images\\general\\current_region', confidence=0.9)
    if location is not None:
        return GameState.ToBattle

    location = localeImage('.\\images\\general\\auto', confidence=0.9)
    if location is not None:
        return GameState.InBattle

    location = localeImage('.\\images\\general\\timer', confidence=0.7)
    if location is not None:
        return GameState.Walking

    location = localeImage('.\\images\\general\\mission_clear', confidence=0.7)
    if location is not None:
        return GameState.MissionClear

    location = localeImage('.\\images\\general\\complete', confidence=0.7)
    if location is not None:
        return GameState.Complete

    return GameState.Other


def handleOtherState():
    print('click battle to if exist...')
    location = localeImage('.\\images\\general\\battle', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\battle', confidence=0.7)
        return

    print('click back if exist...')
    location = localeImage('.\\images\\general\\back', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\back', confidence=0.7)
        return

    print('click touch if exist...')
    location = localeImage('.\\images\\general\\touch', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\touch', confidence=0.7)
        return

    return


def handleToBattleState():
    print('click explain_mission_list...')
    clickImage('.\\images\\general\\explain_mission_list', confidence=0.9)

    print('click bounty...')
    clickImage('.\\images\\general\\bounty', confidence=0.9)

    print('click attack...')
    clickImage('.\\images\\general\\attack', confidence=0.9)

    print('click start_mission...')
    clickImage('.\\images\\general\\start_mission', confidence=0.9)
    return


def handleWalkingState():
    print('click quick_deploy...')
    clickImage('.\\images\\general\\quick_deploy', confidence=0.9)

    print('click auto_command...')
    clickImage('.\\images\\general\\auto_command', confidence=0.9)

    print('click start_battle...')
    clickImage('.\\images\\general\\start_battle', confidence=0.9)
    return


def handleInBattleState():
    print('wait...')
    return


def handleMissionClearState():
    print('click next...')
    clickImage('.\\images\\general\\next', confidence=0.9)
    return


def handleCompleteState():
    print('click confirm...')
    clickImage('.\\images\\general\\confirm', confidence=0.9)
    return


def main():
    scriptName = sys.argv[0]
    print('Start running: ' + scriptName)
    print('Press Ctrl-C to quit.')

    while True:
        print('...')
        currentGameState = checkGameState()
        print(
            '============================================================================')
        print('Current Game State: ' + currentGameState.name)

        if currentGameState == GameState.Other:
            handleOtherState()

        elif currentGameState == GameState.ToBattle:
            handleToBattleState()

        elif currentGameState == GameState.Walking:
            handleWalkingState()

        elif currentGameState == GameState.MissionClear:
            handleMissionClearState()

        elif currentGameState == GameState.InBattle:
            handleInBattleState()

        elif currentGameState == GameState.Complete:
            handleCompleteState()

    return


if __name__ == '__main__':
    main()
