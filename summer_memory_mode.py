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


class StageType(Enum):
    Quest = 'q'
    Boss = 'b'


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


def handleStageSelectionState(targetChapter, targetStage):

    global targetRunCount

    print('run time remains: ' + str(targetRunCount))

    print('click stage ' + str(targetChapter) +
          ' ' + str(targetStage) + ' if exist...')

    if targetStage == StageType.Quest:
        clickImage('.\\images\\summer_memory\\quest', confidence=0.7)
        clickImage('.\\images\\summer_memory\\' +
                   str(targetChapter) + '_t', confidence=0.9)

    elif targetStage == StageType.Boss:
        clickImage('.\\images\\summer_memory\\boss', confidence=0.7)
        clickImage('.\\images\\summer_memory\\' +
                   str(targetChapter) + '_ex', confidence=0.9)

    targetRunCount = targetRunCount - 1
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
    print('click next...')
    clickImage('.\\images\\general\\next', confidence=0.9)
    return


def main():
    global targetRunCount

    scriptName = str(sys.argv[0])
    targetChapter = str(sys.argv[1])
    targetStage = StageType(sys.argv[2])
    targetTeam = str(sys.argv[3])
    targetRunCount = int(sys.argv[4])

    print('start running: ' + str(scriptName))
    print('chapter: ' + str(targetChapter))
    print('stage: ' + str(targetStage))
    print('team: ' + str(targetTeam))
    print('run: ' + str(targetRunCount) + ' time(s)')
    print('press Ctrl-C to quit.')

    while True:
        print('...')

        if targetRunCount < 0:
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
            handleStageSelectionState(targetChapter, targetStage)

        elif currentGameState == GameState.BattlePreparation:
            handleBattlePreparationState(targetTeam)

        elif currentGameState == GameState.InBattle:
            handleInBattleState()

        elif currentGameState == GameState.MissionClear:
            handleMissionClearState()

    return


if __name__ == '__main__':
    main()
