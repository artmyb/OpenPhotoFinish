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

# Image Alignment
On the left frame, you can adjust the alignment of the cropped frame. For the creation of the photo-finish image, the part inside the red dashed rectangle is used.
The non-dashed red line must align with the _leading edge_ of the finish line.
You can click and drag the rectangle. You can adjust the width of the rectangle by scrolling, adjust the height of the rectangle by ctrl+scrolling.
You can adjust the rotation of the frame by hovering on the "rotation" entry and scrolling.
All of the parameters can be adjusted by inputting the parameters into the entries as well.

![4](https://github.com/user-attachments/assets/8bcf0112-2560-44c6-a4d8-c227149d027a)

You must click _Update Image_ after any variable change on the Image Alignment section.
# Closer Look At The Frames
By riht-clicking on a part of the photo-finish image, you can view the full frame of that moment on the upper screen.
The rightmost frame is at the moment you clicked on the photo-finish image. Moving backwards, the frames go forward in time, up to 1.5 seconds.

![5](https://github.com/user-attachments/assets/4c38a606-5cec-4d12-886a-d8797cac59a4)

# Determining Race Times
All you have do to determine the race times for each athlete is to place the hashlines on the foremost part af athletes' torsos; by clicking.
![6](https://github.com/user-attachments/assets/bafdabcc-3d74-4a70-871c-cbb62b9060a3)
_You can save the photo-finsih image as a PNG by the export button, which is the rightmost of the buttons on the bottom._

# Creating Results Table
There are basically three ways to create a results table.
1) By clicking the "+" button and adding the data by typing.
![7](https://github.com/user-attachments/assets/f133f7af-f516-436e-bd3a-7b758fcc0e53)

2) By pasting data from clipboard, which should be copied from a spreadsheet (excel or google sheets)
3) By importing an excel file that includes the data of the heat.
![8](https://github.com/user-attachments/assets/99a86d62-720e-4700-816d-d85f4d7cd4c3)

![9](https://github.com/user-attachments/assets/55ef60c9-5837-4aa6-8f9a-16e3b97cd806)

Whatever the import method is, you can choose the times by double-clicking on the times cells and selecting the time via the combobox opened. The times are loaded according to where you have placed the hashlines on the photo-finish image.
You can click the filmstrip button to view the photo-finish image to better-recognize athletes while creating the table.
![10](https://github.com/user-attachments/assets/6a8c8def-a6e2-4713-a131-1399d499b898)

# Exporting Results
There are also 4.5 ways to export results.
1) By clicking "Copy to Clipboard" to paste to a spreadsheet afterwards.
2) By clicking export button on the rightmost and;
   ![11](https://github.com/user-attachments/assets/93098a96-edb0-4f19-979c-7835921da9a6)

a) Saving as excel

b) Saving as text

c1) Saving the table as PNG
![gt1](https://github.com/user-attachments/assets/a29ffa2a-0f43-4401-8a2e-3a9c4c0a1fd8)

c2) Saving the table and the photo-finish image (combined) as PNG
![gt2](https://github.com/user-attachments/assets/c540dcc8-2d94-4939-957e-709b41ef1d0f)

# How Accurate is OpenPhotoFinish?
For a mobile video recording file, the audio data's timestamps and image frames' timestamps, which this app uses, are already prefectly aligned.
For a recording device with 60 FPS frame rate, the maximum error is simple: 1/60 (0.017) seconds.
Remember that this app has Frame Interpolation feature, which creates new frames in between existing frames, which artificially increases frame rate by up to x6.
With maximum 60 FPS recording and maximum frame interpolation, the accuracy level drops down to 0.004 seconds (4 ms)
To attain the theoretical accuracy level, the only thing to calibrate is to measure the speed of in open air, and know the distance between the start piston and the recording device.
How to measure speed of sound? Put the sound recorders (phones?) side by side and shot the gun. Now bring one of them 100 m apart and shot the gun again. 
Import the recordings, adjust them so that the first shots are aligned. Now, the time difference between the second shots is the time it requires for sound to travel 100m.
Now you can do the math and find speed of sound.
