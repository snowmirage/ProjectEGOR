#!/bin/python
import sys
import os

#had to install youtube-dl  and ffmpeg
#ffmpeg i think is taking an audio file and a video file and muxing them together.
#With these settings youtube-dl should be downloading the best video it finds (that isn't higher than 1080p) and the best audio stream then combining them.  Its omitting webm types of downloads what ever those are.
# it writes a youtube-dl_channelname_archive_list file that lists the id's of all videos it doewnloads when its run again it wont down load those videos but will download new ones.
#its also downloading to a chanelname subdirectory per channel
#want to ask bob how to make this a service?
#thoughts...
#run as a service?  get a list of channel names from a file.  loggs the output that normally goes to stdout to a file


chname = str(raw_input("Enter the youtube channel name: "))

print "you entered", chname

print "Here is the command i'll run\n"

command = "youtube-dl --download-archive '/home/dev@egor.betoria.dyndns.org/mnt/freenas/devcifs/youtube-dl/youtube-dl_" + chname + "_archive_list' -o '/home/dev@egor.betoria.dyndns.org/mnt/freenas/devcifs/youtube-dl/%(uploader)s/%(title)s___(id)s___%(format)s.%(ext)s' -f 'bestvideo[ext!=webm][height<=?1080]+bestaudio[ext!=webm]/best[ext!=webm]' ytuser:" + chname

print command

print "\n\n *** Running Command *** \n\n"

os.system(command)

