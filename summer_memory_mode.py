import time
import pyautogui
import cv2
import sys

from enum import Enum

pyautogui.FAILSAFE = True


class GameState(Enum):
    ChapterSelection = 'ChapterSelection'
    StageSelection = 'StageSelection'
    BattlePreparation = 'BattlePreparation'
    InBattle = 'InBattle'
    MissionClear = 'MissionClear'
    Other = 'Other'


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
    pyautogui.PAUSE = 1.0

    location = localeImage(
        '.\\images\\summer_memory\\chapter_1', confidence=0.9)
    if location is not None:
        return GameState.ChapterSelection

    location = localeImage(
        '.\\images\\summer_memory\\story', confidence=0.9)
    if location is not None:
        return GameState.StageSelection

    location = localeImage(
        '.\\images\\summer_memory\\quest', confidence=0.9)
    if location is not None:
        return GameState.StageSelection

    location = localeImage(
        '.\\images\\summer_memory\\boss', confidence=0.9)
    if location is not None:
        return GameState.StageSelection

    location = localeImage(
        '.\\images\\general\\battle_preparation_case', confidence=0.9)
    if location is not None:
        return GameState.BattlePreparation

    location = localeImage('.\\images\\general\\auto', confidence=0.9)
    if location is not None:
        return GameState.InBattle

    location = localeImage('.\\images\\general\\mission_clear', confidence=0.7)
    if location is not None:
        return GameState.MissionClear
    return GameState.Other


def handleOtherState():
    print('wait...')

    print('click battle if exist...')
    location = localeImage('.\\images\\general\\battle', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\battle', confidence=0.7)
        return

    print('click start mission if exist...')
    location = localeImage('.\\images\\general\\start_mission', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\start_mission', confidence=0.7)
        return

    print('click touch if exist...')
    location = localeImage('.\\images\\general\\touch', confidence=0.7)
    if location is not None:
        clickImage('.\\images\\general\\touch', confidence=0.7)
        return
    return


def handleChapterSelectionState(targetChapter):
    print('click chapter ' + str(targetChapter) + ' if exist...')
    clickImage('.\\images\\summer_memory\\chapter_' +
               str(targetChapter), confidence=0.7)
    return


def handleStageSelectionState(targetChapter):

    global targetBossRunCount
    global targetQuestRunCount
    global ranBossStage
    global ranQuestStage

    ranBossStage = False
    ranQuestStage = False

    if targetBossRunCount > 0:
        print('click chapter ' + str(targetChapter) + ' boss stage if exist...')
        clickImage('.\\images\\summer_memory\\boss', confidence=0.7)
        clickImage('.\\images\\summer_memory\\' +
                   str(targetChapter) + '_ex', confidence=0.9)
        ranBossStage = True

    elif targetQuestRunCount > 0:
        print('click chapter ' + str(targetChapter) + ' quest stage if exist...')
        clickImage('.\\images\\summer_memory\\quest', confidence=0.7)
        clickImage('.\\images\\summer_memory\\' +
                   str(targetChapter) + '_t', confidence=0.9)
        ranQuestStage = True

    return


def handleBattlePreparationState(targetTeam):
    print('click team ' + str(targetTeam) + ' if exist...')
    clickImage('.\\images\\general\\team_' +
               str(targetTeam), confidence=0.9)

    print('click start mission glow if exist...')
    clickImage('.\\images\\general\\start_mission_glow', confidence=0.7)
    return


def handleInBattleState():
    print('wait...')
    return


def handleMissionClearState():

    global targetBossRunCount
    global targetQuestRunCount
    global ranBossStage
    global ranQuestStage

    print('click next...')
    clickImage('.\\images\\general\\next', confidence=0.9)

    print('click next...')
    clickImage('.\\images\\general\\next', confidence=0.9)

    if ranBossStage == True:
        targetBossRunCount = targetBossRunCount - 1

    if ranQuestStage == True:
        targetQuestRunCount = targetQuestRunCount - 1

    print('run boss stage remains: ' + str(targetBossRunCount) + ' time(s)')
    print('run quest stage remains: ' + str(targetQuestRunCount) + ' time(s)')
    return


def main():
    global targetBossRunCount
    global targetQuestRunCount

    scriptName = str(sys.argv[0])
    targetChapter = str(sys.argv[1])
    targetTeam = str(sys.argv[2])
    targetBossRunCount = int(sys.argv[3])
    targetQuestRunCount = int(sys.argv[4])

    print('start running: ' + str(scriptName))
    print('chapter: ' + str(targetChapter))
    print('team: ' + str(targetTeam))
    print('run boss stage: ' + str(targetBossRunCount) + ' time(s)')
    print('run quest stage: ' + str(targetQuestRunCount) + ' time(s)')
    print('press Ctrl-C to quit.')

    while True:
        print('...')

        if targetBossRunCount == 0 and targetQuestRunCount == 0:
            print('finish')
            return

        currentGameState = checkGameState()
        print(
            '============================================================================')
        print('game state: ' + currentGameState.name)

        if currentGameState == GameState.Other:
            handleOtherState()

        elif currentGameState == GameState.ChapterSelection:
            handleChapterSelectionState(targetChapter)

        elif currentGameState == GameState.StageSelection:
            handleStageSelectionState(targetChapter)

        elif currentGameState == GameState.BattlePreparation:
            handleBattlePreparationState(targetTeam)

        elif currentGameState == GameState.InBattle:
            handleInBattleState()

        elif currentGameState == GameState.MissionClear:
            handleMissionClearState()

    return


if __name__ == '__main__':
    main()
