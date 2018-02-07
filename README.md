# Pool
Use main_pic.py to detect a single picture, and main_vid.py to record the pool table via a webcam.
<br>usage: python3 main_pic.py -f your_file_path or python3 main_vid.py -c your_camera_number

work flow:
1. use 'a' to get the image
2. use 'b' or 'c' to determine the boundary of the pool table
(use 'b' for auto detection, however, it may not work for some cases. If this happens, use 'c' to determine the boundary by chosing the four corners)
3. use 'd' to make sure the boundary is correct
4. use 'e', 'f', or 'g' to start detecting balls/cue
5. use 'q' to quit
6. use 'help' to show available commands
