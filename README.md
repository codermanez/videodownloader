# videodownloader
A Python program that downloads videos, gets updates mainly when I feel like it.
## libraries used
### included with python
json: Deals with JSON pages (If you want to see what I mean, add ".json" to the end of a reddit post).<br />
string: String manipulation for filenames, data grabbing, etc.<br />
random: Generates the final name for the video, a random string of 16 characters, including ASCII uppercase and lowercase, and the numbers 0 - 9.<br />
os: File manipulation, deletion of temporary files, file naming and creation, etc.<br />
### not included with python
requests: Internet requests, grabbing JSON data from pages, etc. https://pypi.org/project/ffmpeg-python/<br />
ffmpeg-python: Stitches video and audio together if they are separated. https://pypi.org/project/ffmpeg-python/<br />
pytube: Gets YouTube videos, and lets the program download them. https://pypi.org/project/pytube/<br />
