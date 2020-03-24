import time
import pyautogui
import cv2
import sys

from enum import Enum

pyautogui.FAILSAFE = True


class GameState(Enum):
    BattleTypeSelection = 'BattleTypeSelection'
    RecollectionSelection = 'RecollectionSelection'
    ToBattle = 'ToBattle'
    Walking = 'Walking'
    InBattle = 'InBattle'
    MissionClear = 'MissionClear'
    Complete = 'Complete'
    Other = 'Other'


def localeImage(image, confidence=0.7, grayscale=True):
    return pyautogui.locateOnScreen(image + '.png', confidence=confidence, grayscale=grayscale)


def waitAnimation(second):
    print('wait animation for ' + str(second) + ' s')
    time.sleep(1.0)
    return


def clickImage(targetImage, confidence=0.7):
    print('click ' + targetImage)
    location = localeImage(targetImage, confidence=confidence)
    if location is not None:
        x, y = pyautogui.center(location)
        pyautogui.click(x, y)
        time.sleep(1.0)
    return


def clickImageUntilSuccess(targetImage, confidence=0.7):
    print('click ' + targetImage + ' until success...')
    location = None
    while location is None:
        print('...')
        location = localeImage(targetImage, confidence=confidence)
    x, y = pyautogui.center(location)
    pyautogui.click(x, y)
    time.sleep(1.0)
    return


def clickBackImageUntil(backImage, targetImage):
    print('backImage: ' + backImage)
    print('targetImage: ' + targetImage)
    targetLocation = localeImage(targetImage, confidence=0.9)
    while targetLocation is None:
        clickImage(backImage)
        time.sleep(1.0)
        targetLocation = localeImage(targetImage, confidence=0.9)
    return


def dragImageDownUntil(dragImage, targetImage):
    print('dragImage: ' + dragImage)
    print('targetImage: ' + targetImage)
    dragLocation = localeImage(dragImage)
    if dragLocation is None:
        return
    targetLocation = localeImage(targetImage)
    while targetLocation is None:
        dragLocation = None
        while dragLocation is None:
            dragLocation = localeImage(dragImage)
        x, y = pyautogui.center(dragLocation)
        pyautogui.moveTo(x, y)
        pyautogui.dragTo(x, y - 50, 0.5, button='left')
        time.sleep(1.0)
        targetLocation = localeImage(targetImage)
    return


def checkGameState():
    waitAnimation(2.0)
    location = localeImage('.\\images\\general\\file', confidence=0.9)
    if location is not None:
        return GameState.BattleTypeSelection
    location = localeImage(
        '.\\images\\general\\current_region', confidence=0.9)
    if location is not None:
        return GameState.BattleTypeSelection
    location = localeImage(
        '.\\images\\daily\\enter_region', confidence=0.9)
    if location is not None:
        return GameState.BattleTypeSelection
    location = localeImage(
        '.\\images\\daily\\hero_difficulty', confidence=0.8)
    if location is not None:
        return GameState.BattleTypeSelection

    location = localeImage(
        '.\\images\\daily\\mode_selection_story_mode', confidence=0.9)
    if location is not None:
        return GameState.RecollectionSelection
    location = localeImage(
        '.\\images\\daily\\mode_selection_special_development', confidence=0.9)
    if location is not None:
        return GameState.RecollectionSelection

    location = localeImage('.\\images\\general\\timer', confidence=0.7)
    if location is not None:
        return GameState.Walking

    location = localeImage('.\\images\\general\\auto', confidence=0.9)
    if location is not None:
        return GameState.InBattle

    location = localeImage('.\\images\\general\\mission_clear', confidence=0.7)
    if location is not None:
        return GameState.MissionClear

    location = localeImage('.\\images\\general\\complete', confidence=0.7)
    if location is not None:
        return GameState.Complete

    return GameState.Other


def handleOtherState():
    location = localeImage('.\\images\\daily\\start_mission', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\daily\\start_mission', confidence=0.7)
        return

    location = localeImage(
        '.\\images\\daily\\start_mission_glow', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\daily\\start_mission_glow', confidence=0.7)
        return

    location = localeImage('.\\images\\general\\battle', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\battle', confidence=0.7)
        return

    location = localeImage('.\\images\\general\\touch', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\touch', confidence=0.7)
        return

    location = localeImage('.\\images\\general\\back')
    if location is not None:
        clickImage('.\\images\\general\\back')
        return
    return


def handleBattleTypeSelectionState():
    global currentRecollectionDoneCount
    global currentInstanceRemainCount

    print('currentRecollectionDoneCount: ' + str(currentRecollectionDoneCount))
    print('currentInstanceRemainCount: ' + str(currentInstanceRemainCount))
    clickBackImageUntil('.\\images\\general\\back',
                        '.\\images\\daily\\i_lv60')
    clickImage('.\\images\\general\\battle', confidence=0.7)
    waitAnimation(2.0)
    if currentRecollectionDoneCount < 2:
        clickImage('.\\images\\daily\\recollection', confidence=0.7)
        clickImage('.\\images\\daily\\recollection_tiled', confidence=0.7)
        waitAnimation(2.0)
        clickImage('.\\images\\daily\\lucid_dream', confidence=0.9)
        clickImage('.\\images\\daily\\enter_region', confidence=0.9)

    elif currentInstanceRemainCount > 0:
        clickImage('.\\images\\general\\explain_mission_list', confidence=0.9)
        waitAnimation(1.0)
        clickImage('.\\images\\general\\bounty', confidence=0.9)
        waitAnimation(1.0)
        clickImage('.\\images\\daily\\important', confidence=0.9)
        if currentInstanceRemainCount == 5:
            waitAnimation(1.0)
            clickImage('.\\images\\daily\\instance_5', confidence=0.8)
        elif currentInstanceRemainCount == 4:
            dragImageDownUntil('.\\images\\daily\\instance_5',
                               '.\\images\\daily\\instance_4')
            clickImage('.\\images\\daily\\instance_4', confidence=0.8)
        elif currentInstanceRemainCount == 3:
            dragImageDownUntil('.\\images\\daily\\instance_5',
                               '.\\images\\daily\\instance_3')
            dragImageDownUntil('.\\images\\daily\\instance_4',
                               '.\\images\\daily\\instance_3')
            clickImage('.\\images\\daily\\instance_3', confidence=0.8)
        elif currentInstanceRemainCount == 2:
            dragImageDownUntil('.\\images\\daily\\instance_5',
                               '.\\images\\daily\\instance_2')
            dragImageDownUntil('.\\images\\daily\\instance_4',
                               '.\\images\\daily\\instance_2')
            dragImageDownUntil('.\\images\\daily\\instance_3',
                               '.\\images\\daily\\instance_2')
            clickImage('.\\images\\daily\\instance_2', confidence=0.8)
        elif currentInstanceRemainCount == 1:
            dragImageDownUntil('.\\images\\daily\\instance_5',
                               '.\\images\\daily\\instance_1')
            dragImageDownUntil('.\\images\\daily\\instance_4',
                               '.\\images\\daily\\instance_1')
            dragImageDownUntil('.\\images\\daily\\instance_3',
                               '.\\images\\daily\\instance_1')
            dragImageDownUntil('.\\images\\daily\\instance_2',
                               '.\\images\\daily\\instance_1')
            clickImage('.\\images\\daily\\instance_1', confidence=0.8)
        waitAnimation(1.0)
        clickImage('.\\images\\daily\\hero_difficulty', confidence=0.8)
        clickImage('.\\images\\daily\\start_mission', confidence=0.9)
        waitAnimation(2.0)
        currentInstanceRemainCount = currentInstanceRemainCount - 1
    else:
        currentRecollectionDoneCount = -1
        currentInstanceRemainCount = -1
        waitAnimation(2.0)
    return


def handleRecollectionSelectionState():
    global currentRecollectionDoneCount

    print('currentRecollectionDoneCount: ' + str(currentRecollectionDoneCount))

    if currentRecollectionDoneCount < 2:
        clickImage('.\\images\\daily\\story_mode', confidence=0.9)
        clickImage('.\\images\\daily\\recollection_4', confidence=0.9)
        clickImage('.\\images\\daily\\confirm', confidence=0.9)
        waitAnimation(2.0)
    else:
        clickImage('.\\images\\general\\back')

    currentRecollectionDoneCount = currentRecollectionDoneCount + 1
    return


def handleToBattleState():
    clickImage('.\\images\\general\\explain_mission_list', confidence=0.9)
    clickImage('.\\images\\general\\bounty', confidence=0.9)
    clickImage('.\\images\\general\\attack', confidence=0.9)
    clickImage('.\\images\\general\\start_mission', confidence=0.9)
    return


def handleWalkingState():
    clickImage('.\\images\\general\\quick_deploy', confidence=0.9)
    clickImage('.\\images\\general\\auto_command', confidence=0.9)
    clickImage('.\\images\\general\\start_battle', confidence=0.9)
    return


def handleInBattleState():
    print('wait...')
    return


def handleMissionClearState():
    clickImage('.\\images\\general\\next', confidence=0.9)
    return


def handleCompleteState():
    clickImage('.\\images\\general\\confirm', confidence=0.9)
    waitAnimation(5.0)
    return


def main():
    global currentRecollectionDoneCount
    global currentInstanceRemainCount

    currentRecollectionDoneCount = 0  # 0
    currentInstanceRemainCount = 5  # 5

    scriptName = sys.argv[0]
    print('Start running: ' + scriptName)
    print('Press Ctrl-C to quit.')

    while True:
        print('...')
        currentGameState = checkGameState()
        print(
            '============================================================================')
        print('Current Game State: ' + currentGameState.name)

        if currentRecollectionDoneCount == -1 and currentInstanceRemainCount == -1:
            print('Finish')
            return

        if currentGameState == GameState.Other:
            handleOtherState()

        elif currentGameState == GameState.BattleTypeSelection:
            handleBattleTypeSelectionState()

        elif currentGameState == GameState.RecollectionSelection:
            handleRecollectionSelectionState()

        elif currentGameState == GameState.ToBattle:
            handleToBattleState()

        elif currentGameState == GameState.Walking:
            handleWalkingState()

        elif currentGameState == GameState.InBattle:
            handleInBattleState()

        elif currentGameState == GameState.MissionClear:
            handleMissionClearState()

        elif currentGameState == GameState.Complete:
            handleCompleteState()
    return


if __name__ == '__main__':
    main()
