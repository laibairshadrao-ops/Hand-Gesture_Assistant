
import cv2
import mediapipe as mp
import pyautogui
import pyttsx3
import time
import os
import asyncio
from datetime import datetime

# Windows Media Control
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
)


# ==========================================
# MEDIAPIPE HAND SETUP
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85
)


# ==========================================
# SCREENSHOT FOLDER
# ==========================================

BASE_FOLDER = r"C:\Users\AL-SAEED\OneDrive\Pictures\Screenshots"

if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)


# ==========================================
# VOICE
# ==========================================

def say_screenshot_saved():
    try:
        engine = pyttsx3.init()

        voices = engine.getProperty("voices")

        # Microsoft Zira
        engine.setProperty(
            "voice",
            voices[1].id
        )

        engine.setProperty(
            "rate",
            170
        )

        engine.say(
            "Screenshot saved."
        )

        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print(
            "⚠️ Voice error:",
            e
        )


# ==========================================
# VOLUME FUNCTIONS
# ==========================================

def increase_volume():

    pyautogui.press(
        "volumeup"
    )

    print(
        "🔊 Volume increased"
    )


def decrease_volume():

    pyautogui.press(
        "volumedown"
    )

    print(
        "🔉 Volume decreased"
    )


# ==========================================
# PAUSE MUSIC ONLY
# ==========================================

async def pause_current_media():

    try:

        # Ask Windows for the current media session
        sessions = await MediaManager.request_async()

        current_session = sessions.get_current_session()

        # No media player is active
        if current_session is None:

            print(
                "ℹ️ No active media session found."
            )

            return


        # ------------------------------------------
        # CHECK CURRENT PLAYBACK STATUS
        # ------------------------------------------

        playback_info = (
            current_session.get_playback_info()
        )

        status = playback_info.playback_status.name

        print(
            "🎵 Current media status:",
            status
        )


        # ------------------------------------------
        # ONLY SEND PAUSE COMMAND IF PLAYING
        # ------------------------------------------

        if status == "PLAYING":

            print(
                "⏸️ Sending pause command..."
            )

            # Windows media Play/Pause command
            pyautogui.press(
                "playpause"
            )

            # Give Windows time to update
            await asyncio.sleep(
                0.8
            )


            # ------------------------------------------
            # CHECK AGAIN AFTER COMMAND
            # ------------------------------------------

            playback_info_after = (
                current_session.get_playback_info()
            )

            status_after = (
                playback_info_after.playback_status.name
            )

            print(
                "🎵 Media status after command:",
                status_after
            )


            # ------------------------------------------
            # CONFIRM THAT MUSIC REALLY PAUSED
            # ------------------------------------------

            if status_after == "PAUSED":

                print(
                    "⏸️ Music successfully paused."
                )

            else:

                print(
                    "⚠️ Music did NOT pause."
                )

                print(
                    "⚠️ Windows still reports:",
                    status_after
                )


        # ------------------------------------------
        # ALREADY PAUSED
        # ------------------------------------------

        elif status == "PAUSED":

            print(
                "⏸️ Music is already paused."
            )

            print(
                "ℹ️ No command was sent."
            )


        # ------------------------------------------
        # ANY OTHER MEDIA STATE
        # ------------------------------------------

        else:

            print(
                "ℹ️ Media is not currently playing."
            )

            print(
                "ℹ️ No command was sent."
            )


    except Exception as e:

        print(
            "⚠️ Could not pause media:",
            e
        )


# ==========================================
# STOP MUSIC
# ==========================================

def stop_music():

    try:

        asyncio.run(
            pause_current_media()
        )

    except Exception as e:

        print(
            "⚠️ Media control error:",
            e
        )


# ==========================================
# VARIABLES
# ==========================================

last_screenshot_time = 0

cooldown_seconds = 4

fist_was_detected = False

victory_was_detected = False

thumbs_up_was_detected = False

thumbs_down_was_detected = False

open_hand_was_detected = False

latest_screenshot = None


# ==========================================
# WEBCAM
# ==========================================

cap = cv2.VideoCapture(0)


if not cap.isOpened():

    print(
        "❌ Error: Could not open webcam."
    )

    exit()


print(
    "=========================================="
)

print(
    "🚀 GESTURE SCREENSHOT TOOL STARTED"
)

print(
    "=========================================="
)

print(
    "👊 Fist        = Take Screenshot"
)

print(
    "✌️ Victory     = Open Latest Screenshot"
)

print(
    "👍 Thumbs Up   = Increase Volume"
)

print(
    "👎 Thumbs Down = Decrease Volume"
)

print(
    "✋ Open Palm   = Pause Music"
)

print(
    "🔊 Voice       = Screenshot saved"
)

print(
    "📁 Screenshots organized by date"
)

print(
    "🛑 Press Q to quit"
)

print(
    "=========================================="
)


# ==========================================
# MAIN LOOP
# ==========================================

while cap.isOpened():

    success, frame = cap.read()


    if not success:

        print(
            "❌ Could not read webcam frame."
        )

        break


    frame = cv2.flip(
        frame,
        1
    )


    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    results = hands.process(
        rgb_frame
    )


    # ==========================================
    # RESET GESTURE STATES
    # ==========================================

    is_fist = False

    is_victory = False

    is_thumbs_up = False

    is_thumbs_down = False

    is_open_hand = False


    # ==========================================
    # HAND DETECTED
    # ==========================================

    if results.multi_hand_landmarks:

        for hand_lms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_lms,
                mp_hands.HAND_CONNECTIONS
            )


            # ==========================================
            # LANDMARKS
            # ==========================================

            wrist = hand_lms.landmark[0]

            thumb_tip = hand_lms.landmark[4]

            thumb_ip = hand_lms.landmark[3]

            index_tip = hand_lms.landmark[8]

            index_pip = hand_lms.landmark[6]

            middle_tip = hand_lms.landmark[12]

            middle_pip = hand_lms.landmark[10]

            ring_tip = hand_lms.landmark[16]

            ring_pip = hand_lms.landmark[14]

            pinky_tip = hand_lms.landmark[20]

            pinky_pip = hand_lms.landmark[18]

            palm_center = hand_lms.landmark[9]


            # ==========================================
            # FINGER STATES
            # ==========================================

            index_up = (
                index_tip.y <
                index_pip.y
            )

            middle_up = (
                middle_tip.y <
                middle_pip.y
            )

            ring_up = (
                ring_tip.y <
                ring_pip.y
            )

            pinky_up = (
                pinky_tip.y <
                pinky_pip.y
            )

            ring_down = (
                ring_tip.y >
                ring_pip.y
            )

            pinky_down = (
                pinky_tip.y >
                pinky_pip.y
            )


            # ==========================================
            # VICTORY SIGN ✌️
            # ==========================================

            if (
                index_up
                and middle_up
                and ring_down
                and pinky_down
            ):

                is_victory = True

                cv2.putText(
                    frame,
                    "VICTORY - OPENING LAST SCREENSHOT",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 255),
                    2
                )


            # ==========================================
            # THUMBS UP 👍
            # ==========================================

            thumb_up = (
                thumb_tip.y <
                thumb_ip.y
            )

            index_folded = (
                index_tip.y >
                index_pip.y
            )

            middle_folded = (
                middle_tip.y >
                middle_pip.y
            )

            ring_folded = (
                ring_tip.y >
                ring_pip.y
            )

            pinky_folded = (
                pinky_tip.y >
                pinky_pip.y
            )


            if (
                thumb_up
                and index_folded
                and middle_folded
                and ring_folded
                and pinky_folded
            ):

                is_thumbs_up = True

                cv2.putText(
                    frame,
                    "THUMBS UP - VOLUME UP",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )


            # ==========================================
            # THUMBS DOWN 👎
            # ==========================================

            thumb_down = (
                thumb_tip.y >
                thumb_ip.y
            )


            if (
                thumb_down
                and index_folded
                and middle_folded
                and ring_folded
                and pinky_folded
            ):

                is_thumbs_down = True

                cv2.putText(
                    frame,
                    "THUMBS DOWN - VOLUME DOWN",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )


            # ==========================================
            # OPEN PALM ✋
            # FINGERS MUST BE SPREAD APART
            # ==========================================

            thumb_distance = (
                (thumb_tip.x - palm_center.x) ** 2
                +
                (thumb_tip.y - palm_center.y) ** 2
            ) ** 0.5


            thumb_extended = (
                thumb_distance > 0.10
            )


            # Distance between neighboring fingertips

            index_middle_distance = abs(
                index_tip.x -
                middle_tip.x
            )

            middle_ring_distance = abs(
                middle_tip.x -
                ring_tip.x
            )

            ring_pinky_distance = abs(
                ring_tip.x -
                pinky_tip.x
            )


            # Fingers must be clearly separated

            fingers_spread = (
                index_middle_distance > 0.025
                and middle_ring_distance > 0.025
                and ring_pinky_distance > 0.025
            )


            # Open palm requires:
            # 1. All four fingers up
            # 2. Thumb extended
            # 3. Fingers spread apart

            if (
                index_up
                and middle_up
                and ring_up
                and pinky_up
                and thumb_extended
                and fingers_spread
            ):

                is_open_hand = True

                cv2.putText(
                    frame,
                    "OPEN PALM - PAUSE MUSIC",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255, 255, 0),
                    3
                )


            # ==========================================
            # FIST 👊
            # ==========================================

            finger_tips = [
                8,
                12,
                16,
                20
            ]


            folded_fingers = 0


            for tip_id in finger_tips:

                tip = hand_lms.landmark[
                    tip_id
                ]

                knuckle = hand_lms.landmark[
                    tip_id - 3
                ]


                if tip.y > knuckle.y:

                    folded_fingers += 1


            thumb_distance_fist = (
                (thumb_tip.x - palm_center.x) ** 2
                +
                (thumb_tip.y - palm_center.y) ** 2
            ) ** 0.5


            if thumb_distance_fist < 0.07:

                folded_fingers += 1


            if folded_fingers == 5:

                is_fist = True

                cv2.putText(
                    frame,
                    "FIST DETECTED!",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )


            elif (
                not is_victory
                and not is_thumbs_up
                and not is_thumbs_down
                and not is_open_hand
            ):

                cv2.putText(
                    frame,
                    "Make a FIST, VICTORY, THUMBS UP, THUMBS DOWN or OPEN PALM",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )


    # ==========================================
    # ACTIONS
    # ==========================================

    current_time = time.time()


    # ==========================================
    # FIST → SCREENSHOT
    # ==========================================

    if (
        is_fist
        and not fist_was_detected
        and (
            current_time -
            last_screenshot_time >
            cooldown_seconds
        )
    ):

        print(
            "\n📸 FIST DETECTED!"
        )

        print(
            "Taking desktop screenshot..."
        )


        today = datetime.now().strftime(
            "%Y-%m-%d"
        )


        daily_folder = os.path.join(
            BASE_FOLDER,
            today
        )


        if not os.path.exists(
            daily_folder
        ):

            os.makedirs(
                daily_folder
            )


        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )


        filename = os.path.join(
            daily_folder,
            f"screenshot_{timestamp}.png"
        )


        screenshot = pyautogui.screenshot()

        screenshot.save(
            filename
        )


        latest_screenshot = filename


        print(
            "💾 Screenshot saved:"
        )

        print(
            filename
        )


        say_screenshot_saved()


        last_screenshot_time = (
            current_time
        )


    # ==========================================
    # VICTORY → OPEN LAST SCREENSHOT
    # ==========================================

    if (
        is_victory
        and not victory_was_detected
    ):

        if latest_screenshot is not None:

            print(
                "\n✌️ VICTORY SIGN DETECTED!"
            )

            print(
                "Opening latest screenshot:"
            )

            print(
                latest_screenshot
            )


            try:

                os.startfile(
                    latest_screenshot
                )

            except Exception as e:

                print(
                    "❌ Could not open screenshot:",
                    e
                )

        else:

            print(
                "\n⚠️ No screenshot has been taken yet."
            )


    # ==========================================
    # THUMBS UP → INCREASE VOLUME
    # ==========================================

    if (
        is_thumbs_up
        and not thumbs_up_was_detected
    ):

        print(
            "\n👍 THUMBS UP DETECTED!"
        )

        increase_volume()


    # ==========================================
    # THUMBS DOWN → DECREASE VOLUME
    # ==========================================

    if (
        is_thumbs_down
        and not thumbs_down_was_detected
    ):

        print(
            "\n👎 THUMBS DOWN DETECTED!"
        )

        decrease_volume()


    # ==========================================
    # OPEN PALM → PAUSE MUSIC ONLY
    # ==========================================

    if (
        is_open_hand
        and not open_hand_was_detected
    ):

        print(
            "\n✋ OPEN PALM DETECTED!"
        )

        stop_music()


    # ==========================================
    # UPDATE GESTURE STATES
    # ==========================================

    fist_was_detected = is_fist

    victory_was_detected = is_victory

    thumbs_up_was_detected = (
        is_thumbs_up
    )

    thumbs_down_was_detected = (
        is_thumbs_down
    )

    open_hand_was_detected = (
        is_open_hand
    )


    # ==========================================
    # SHOW CAMERA
    # ==========================================

    cv2.imshow(
        "Gesture Screenshot Tool",
        frame
    )


    # ==========================================
    # PRESS Q TO QUIT
    # ==========================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cv2.destroyAllWindows()

hands.close()

print(
    "\n🛑 Program stopped."
)

