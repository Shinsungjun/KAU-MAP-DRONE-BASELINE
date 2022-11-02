# KDR-2022 - Adam's Room
Repository for KAU AI-Drone Challenge

## 📝 Skill
* Perception
  * Yolov5 Object Detection for Gate Detection
  * Calculate Coordinate
* Drone Control
  * Airsim API
* etc ..
  * MultiThreading Programming for Control 🎮 & Perception 👁

## 📌 TODO
- [ ] Gate Detection  (Perception)
- [ ] Optimal Path Algorithm (Control)
- [ ] Additional AI Training


## 👤 Collaborator
* holy_joon 🦋
* adam_gold 🏅
* vvonto 🐣
## How To Start Simulator
 Korea Aerospace University Drone Racing Trials 2022
 
 1. Clone this directory
 2. Download KDR 2022 simulator from 
   - https://scm.kau.ac.kr/ko/program/all/view/813/notice/view/46?p=1
   - https://drive.google.com/drive/u/1/folders/1wLymWa2mLiU6dSUah2lqV5ZtwY6eTgS_/
 3. Open KDR 2022 simulator (KDR_2022.exe)
 5. Check license acknowledgements
 6. Enter permission code
 7. Click run simulator to open simulator 
 8. Open and run multirotor_example/DemoBaseline.py




- KDR 2022 simulator runs based on AirSim (https://microsoft.github.io/AirSim/)
- Server connection is not stable at the moment, however bestlap data is always stored loaclly. By pressing upload best lap button, your locally saved best lap data will be posted online, only if server is online.
- Feel free to ask questions : retelligence@kakao.com

- Create your own code based on DemoBaseline.py and don't forget to add AI functionallity. The gates inside the simulator will have random noises every session. That being said, with only the baseline code, the drone will not make it through the whole path.

- To update the simulator, copy the new .Pak file and paste it into KDR 2022 simulator/KDR_2022/Content/Paks/
