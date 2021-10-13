import requests
import json
import string
import random
import os
import ffmpeg
from pytube import YouTube, Playlist
jsonSuffix = ".json"
vid240 = 'DASH_240.mp4'
vid360 = 'DASH_360.mp4'
vid480 = 'DASH_480.mp4'
def generate_name():
    randomNameGenerator = string.ascii_uppercase + string.ascii_lowercase + string.digits
    randomName = ''.join(random.choice(randomNameGenerator) for i in range(16)) + '.mp4'
    return randomName
def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename
downloadOptions = input("Enter URL of video: ")
if 'reddit.com' in downloadOptions:
    postURL = downloadOptions
    videoQuality = input("Input the wanted quality (1: 240p, 2: 360p, 3: 480p): ")
    if postURL.endswith('/'):
        postURL = postURL[:-1]
    postURLjsonified = postURL + jsonSuffix
    response = requests.get(postURLjsonified, headers = {'User-agent': 'your bot 0.1'})
    URLresponse = response.json()
    internalPostURL = URLresponse[0]['data']['children'][0]['data']['url']
    print(internalPostURL)
    video480URL = internalPostURL + '/DASH_480.mp4'
    video360URL = internalPostURL + '/DASH_360.mp4'
    video240URL = internalPostURL + '/DASH_240.mp4'
    audioURL = internalPostURL + '/DASH_audio.mp4'
    print('No Audio: '+video480URL)
    print('No Audio: '+video360URL)
    print('No Audio: '+video240URL)
    print('Just Audio: '+audioURL)
    if videoQuality == '1':
        videoURL = video240URL
        vid = vid240
    elif videoQuality == '2':
        videoURL = video360URL
        vid = vid360
    elif videoQuality == '3':
        videoURL = video480URL
        vid = vid480
    else:
        print('Sorry, the video quality you entered does not exist, switching to 240p')
        videoURL = video240URL
        vid = vid240
    download_file(videoURL)
    download_file(audioURL)
    video = ffmpeg.input(vid)
    audio = ffmpeg.input('DASH_audio.mp4')
    randomname = generate_name()
    try:
        out = ffmpeg.output(video, audio, randomname, vcodec='h264', acodec='aac', strict='experimental')
        out.run()
    except:
        print("Sorry, video quality does not exist, lowering quality.")
        os.remove(vid)
        vid = vid360 if vid == vid480 else vid240
        videoURL = video360URL if videoURL == video480URL else video240URL
        download_file(videoURL)
        video = ffmpeg.input(vid)
        audio = ffmpeg.input('DASH_audio.mp4')
        try:
            out = ffmpeg.output(video, audio, randomname, vcodec='h264', acodec='aac', strict='experimental')
            out.run()
        except:
            print("Sorry, video quality does not exist, lowering quality.")
            os.remove(vid)
            vid = vid240
            videoURL = video240URL
            video = ffmpeg.input(vid)
            audio = ffmpeg.input('DASH_audio.mp4')
            try:
                out = ffmpeg.output(video, audio, randomname, vcodec='h264', acodec='aac', strict='experimental')
                out.run()
            except:
                print('Sorry, no matching qualities could be found, however, an alternative way to download this video is https://redditsave.com/')
    os.remove(vid)
    os.remove('DASH_audio.mp4')
elif 'youtube.com' in downloadOptions:
    youtubeURL = downloadOptions
    if '&list=' or 'playlist' in youtubeURL:
        ytplaylist = Playlist(youtubeURL)
        autodl = input("Would you like to auto-download the playlist? [y/n]\n(Quality automatically maxes out)\n")
        if autodl == 'y' or 'yes' or 'Y' or 'Yes' or 'YES':
            for yt in ytplaylist.videos:
                yt.streams.get_highest_resolution().download()
                print("Downloaded " + yt.title + "\nMoving on!")
        else:
            for yt in ytplaylist.videos:
                streamlist = yt.streams
                for x in streamlist:
                    stream = str(x)
                    indx = streamlist.index(x) + 1
                    vidresloc = stream.find('res')
                    vidfpsloc = stream.find('fps')
                    vidres = stream[vidresloc:vidfpsloc]
                    vidfps = stream[vidfpsloc:stream.find('vcodec')]
                    if vidres == 'ressive="False" type="audio"':
                        h = 1
                    else:
                        vidres = vidres[vidres.find('"')+1:vidres.rfind('"')]
                        vidfps = vidfps[vidfps.find('"')+1:vidfps.rfind('"')]
                        print('Download Option ' + str(indx)+ ':\n' + vidres + ' @ ' + vidfps + '\n')
                DLoption = input('Select wanted download option number: ')
                try:
                    DLoption = int(DLoption) - 1
                except ValueError:
                    print("The answer was not an integer, reverting to first option")
                    DLoption = 0
                except:
                    print("Something else went wrong, reverting to first option")
                    DLoption = 0
                vidtyp = str(yt.streams[DLoption])
                vidtyploc = stream.find('mime_type')
                vidtyp = vidtyp[vidtyploc:stream.find('abr')]
                vidtyp = vidtyp[vidtyp.find('"') + 1:vidtyp.rfind('"')]
                vidtyp = vidtyp[vidtyp.find('/')+1:]
                audtyp = str(yt.streams[len(streamlist)-1])
                audtyploc = stream.find('mime_type')
                audtyp = audtyp[audtyploc:stream.find('abr')]
                audtyp = audtyp[audtyp.find('"') + 1:audtyp.rfind('"')]
                audtyp = audtyp[audtyp.find('/') + 1:]
                tvf = ffmpeg.input('temporaryvideofile.' + vidtyp)
                taf = ffmpeg.input('temporaryaudiofile.' + audtyp)
                yt.streams[DLoption].download(filename='temporaryvideofile.' + vidtyp)
                yt.streams[len(streamlist)-1].download(filename='temporaryaudiofile.' + audtyp)
                randomname = generate_name()
                out = ffmpeg.output(tvf, taf, randomname, vcodec='h264', acodec='aac', strict='experimental')
                out.run()
                os.remove('temporaryvideofile.' + vidtyp)
                os.remove('temporaryaudiofile.' + audtyp)
    else:
        yt = YouTube(youtubeURL)
        streamlist = yt.streams
        for x in streamlist:
            stream = str(x)
            indx = streamlist.index(x) + 1
            vidresloc = stream.find('res')
            vidfpsloc = stream.find('fps')
            vidres = stream[vidresloc:vidfpsloc]
            vidfps = stream[vidfpsloc:stream.find('vcodec')]
            if vidres == 'ressive="False" type="audio"':
                h = 1
            else:
                vidres = vidres[vidres.find('"')+1:vidres.rfind('"')]
                vidfps = vidfps[vidfps.find('"')+1:vidfps.rfind('"')]
                print('Download Option ' + str(indx)+ ':\n' + vidres + ' @ ' + vidfps + '\n')
        DLoption = input('Select wanted download option number: ')
        try:
            DLoption = int(DLoption) - 1
        except ValueError:
            print("The answer was not an integer, reverting to first option")
            DLoption = 0
        except:
            print("Something else went wrong, reverting to first option")
            DLoption = 0
        vidtyp = str(yt.streams[DLoption])
        vidtyploc = stream.find('mime_type')
        vidtyp = vidtyp[vidtyploc:stream.find('abr')]
        vidtyp = vidtyp[vidtyp.find('"') + 1:vidtyp.rfind('"')]
        vidtyp = vidtyp[vidtyp.find('/')+1:]
        audtyp = str(yt.streams[len(streamlist)-1])
        audtyploc = stream.find('mime_type')
        audtyp = audtyp[audtyploc:stream.find('abr')]
        audtyp = audtyp[audtyp.find('"') + 1:audtyp.rfind('"')]
        audtyp = audtyp[audtyp.find('/') + 1:]
        tvf = ffmpeg.input('temporaryvideofile.' + vidtyp)
        taf = ffmpeg.input('temporaryaudiofile.' + audtyp)
        yt.streams[DLoption].download(filename='temporaryvideofile.' + vidtyp)
        yt.streams[len(streamlist)-1].download(filename='temporaryaudiofile.' + audtyp)
        randomname = generate_name()
        out = ffmpeg.output(tvf, taf, randomname, vcodec='h264', acodec='aac', strict='experimental')
        out.run()
        os.remove('temporaryvideofile.' + vidtyp)
        os.remove('temporaryaudiofile.' + audtyp)
elif 'imgur.com' in downloadOptions:
    if downloadOptions.endswith('/'):
        downloadOptions = downloadOptions[:-1]
    response = requests.get(downloadOptions + jsonSuffix, headers = {'User-agent': 'your bot 0.1'})
    URLresponse = response.json()
    filename = URLresponse["data"]["image"]["album_cover"] + ".mp4"
    download_file("https://i.imgur.com/" + filename)
