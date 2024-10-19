# OpenPhotoFinish
A video processing app to determine race times for athletic events.
# What you'll need beforehand:
A tripod, a video recording device (mobile phone), blank firing pistol, PC
The video recording of the race, starting from before the start signal (shot of pistol) ends after all the athletes pass the finish.
The video must be captured on the finish line, with a steady camera aligned with the finish line.
# How To Use The App
Import the video of the race
![1](https://github.com/user-attachments/assets/4c54beb5-725d-456d-9743-b5ef7b3f05e9)
Choose the start time by clicking on the start signal
![2](https://github.com/user-attachments/assets/126c959e-e2fe-4011-98b2-a6bce14fb256)
# Sound Parameters:
1) Start signal - microphone distance: the distance between the pistol and the recording device.
2) Race start - start signal distance: the distance between the athletes and the pistol.
3) Speed of sound: Speed of sound travelling in the open air.
4) Wind speed: The wind speed's component in the direction from pistol to recording device (negligible)
5) Additional time offset: In case you need. This parameter adds to the times.

_You can also use a pair of mobile radios & walkie talkies to transfer the sound from pistol to recording device on the finish line. In that case, you can input "0" for 1st parameter since the sound travels at nearly the speed of light via radio signal._

# Image Processing
After you are done with the parameters, navigate to second tab. First, input "BEGIN" and "END" times to import. These are AFTER the start of the race (pistol shot) and not since the beginning of the video.

_Example: In a 100 m race, all the athletes finished the race about between 11 seconds and 15 seconds: you input 11 to the "seconds" entry of BEGIN, 15 to "seconds" entry of END._

**FPS Increase combobox:** Since the frame rate of an ordinary device is for low compared to that of a high end photo-finish device, this tool enables you to artificially increase the FPS by adding new frames within existing frames by calculating the speed of moving objects. The higher the FPS increase, the more accurate the results but with longer render time.

After you are set up with times and FPS increase, you can hit "Generate Image"

![3](https://github.com/user-attachments/assets/6308715c-34ca-421d-a09e-8034984905bc)
