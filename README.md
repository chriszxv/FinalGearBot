# FinalGearBot

Python bot for lazy people to play [FinalGear](https://www.komoejoy.com/FinalGear//) (TW server)

## Requirement

- Use Windows 10
- Support Python 3.X.X
- Support PyAutoGUI

## Installation

* Download free Android emulator from [NoxPlayer](https://www.bignox.com/)

* Install in to your Windows

* Enable [virtualization](https://support.bluestacks.com/hc/en-us/articles/115003174386-How-can-I-enable-virtualization-VT-on-my-PC-)

* Follow the settings:

  ![](images/readme/setting_1.png)
      
  ![](images/readme/setting_2.png)
      
  ![](images/readme/setting_3.png)
      
  ![](images/readme/setting_4.png)

---

## Mode

Start bot by typing following commands in this current directory

### Normal

1. Go to event screen:

![](images/readme/normal.png)

2. Enter command:

  ```shell
  $ py .\normal_mode.py
  ```

---

### Summer Memory

1. Go to event screen:

![](images/readme/summer_memory.png)

2. Enter command:

| Parameter      | Value            | Detail                              |
| -------------- | ---------------- | ----------------------------------- |
| Chapter Number | `1`-`4`          | Chapter number                      |
| Stage Type     | `q` / `b`        | `q` = quest stage, `b` = boss stage |
| Team           | `1`-`4`          | Team number                         |
| Run Time       | Unsigned Integer | Number of running time              |

  Run summer memory, chapter `1` stage `q`uest using team `4` for `30` times

  ```shell
  $ py .\summer_memory_mode.py 1 q 4 30
  ```
