# :books: Table of Contents

- [About](#about)
- [Get Started](#get-started)
- [To-Do](#to-do)
- [Contribute](#contribute)

# :pushpin: About

This is an low-code / no-code application that _dramatically_ reduces the complexity of using pose estimation frameworks to extract pose keypoints/landmarks. It will support two libraries for pose keypoint extraction. ( MMPose, MediaPipePoseModel).

This application is intended for anyone (commercial, research, non-profit, hobbyist) who wants to easily ultilize common pose estimation frameworks. Supports Windows and Linux.

### Example Usage (WIP)

#### CLI:

"win_keypoint_extraction_cli.exe -input_path _input_path_ -output_path _output_path_ -pose_framework mediapipe"

# :chart_with_upwards_trend: Get Started

No prereqs required.

NOTE: Application yet to be implemented.

## CLI:

1.  Download the CLI application for your OS
2.  Use the app in your terminal with the following arguments:

    Required:

        1. *-input_path* Path to your input directory or file. Pass "webcam" or webcam device number to use a webcam.
        2. *-output_path* Path to your output directory.
        3. *-pose_framework* Name of the framework you are using. Future supported options: "mediapipe" or "mmpose"

    Optional:

        4. *--pose_config* Optionally specify path to a model configuration file
        5. *--pose_checkpoint* Optionally specify poth to model checkpoint file.
        6. *--detection_framework* Optionally specify name of detection framework to use
        7. *--detection_config* Optionally specify path to detection model configuration file.
        8. *--detection_checkpoint* Optionally specify path to detection model checkpoint file.

3.  Pour yourself a cup of coffee while you wait for your results.

## GUI (WIP):

Still Needed

## Test Data

1. Images: https://github.com/jeffffffli/CrowdPose
2. Videos: Still needed

# :dart: To-Do

- [ ] Finish Todo List (#1)
- [ ] Make Working Demo (#2)

# :raising_hand: Contribute

We welcome contributions from everyone! Whether you're fixing bugs, adding features, improving documentation, or just asking questions - your help makes this project better.
