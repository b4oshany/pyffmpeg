#!/usr/bin/env python

import csv
import subprocess
import re
import math
import json
import os
from optparse import OptionParser


length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
re_length = re.compile(length_regexp)


def concat_name(videos, save_as=None):
    vs = " ".join(videos)

    if not save_as:
        bn = "-".join([os.path.basename(n).split(".")[0] for n in videos if "." in n])
        ex = videos[0].split(".")[-1]
        save_as = "%s.%s" % (bn, ex)
    dirn = os.path.dirname(os.path.abspath(videos[0]))
    save_as = "%s/%s" % (dirn, save_as)
    return save_as

def resize_video(filename,width=320,height=240, save_as=None):
    resize_cmd = "ffmpeg -i {} -vf scale={}:{} {} -y".format(filename, width, height, save_as or filename)
    try:
        subprocess.call([resize_cmd], shell=True)
    except Exception as e:
        print e


def get_video_info(filename):
    info_cmd = "ffprobe -v quiet -print_format json -show_format -show_streams {}".format(filename)
    try:
        output = subprocess.Popen(info_cmd,
                      shell = True,
                              stdout = subprocess.PIPE
                              ).stdout.read()
        return json.loads(output)
    except Exception as e:
        print e
    return None


def concat_videos(videos, save_as=None, remove_gen=True):
    save_as = concat_name(videos, save_as)
    dirname = os.path.dirname(save_as) or "."
    txt = "{}.txt".format(os.path.basename(save_as))
    txt_location = "{}/{}".format(dirname,txt)
    with open(txt_location, "w") as fp:
        for vid in videos:
            if vid:
                fp.write("file %s\n" % vid)

    concat_cmd = ("ffmpeg -f concat -safe 0 -i %s -c:a copy %s -y %s") % (
        txt_location,
        save_as,
        "&& rm {}".format(txt_location) if remove_gen else ""
    )
    print "---------"
    print concat_cmd
    print "---------"
    print save_as
    try:
        subprocess.call([concat_cmd], shell = True)

    except Exception as e:
        print e
        return ""
    return save_as


def split_by_manifest(filename, manifest, vcodec="copy", acodec="copy",
                      **kwargs):
    """ Split video into segments based on the given manifest file.

    Arguments:
        filename (str)      - Location of the video.
        manifest (str)      - Location of the manifest file.
        vcodec (str)        - Controls the video codec for the ffmpeg video
                            output.
        acodec (str)        - Controls the audio codec for the ffmpeg video
                            output.
    """
    if not os.path.exists(manifest):
        print "File does not exist: %s" % manifest
        raise SystemExit

    with open(manifest) as manifest_file:
        manifest_type = manifest.split(".")[-1]
        if manifest_type == "json":
            config = json.load(manifest_file)
        elif manifest_type == "csv":
            config = csv.DictReader(manifest_file)
        else:
            print "Format not supported. File must be a csv or json file"
            raise SystemExit

        split_cmd = "ffmpeg -i '%s' -vcodec %s -acodec %s -y " % (filename,
                                                                  vcodec,
                                                                  acodec)
        split_count = 1
        split_error = []
        try:
            fileext = filename.split(".")[-1]
        except IndexError as e:
            raise IndexError("No . in filename. Error: " + str(e))
        for video_config in config:
            split_str = ""
            try:
                split_start = video_config["start_time"]
                split_size = video_config.get("end_time", None)
                if not split_size:
                    split_size = video_config["length"]
                filebase = video_config["rename_to"]
                if fileext in filebase:
                    filebase = ".".join(filebase.split(".")[:-1])

                split_str += " -ss " + str(split_start) + " -t " + \
                    str(split_size) + \
                    " '"+ filebase + "." + fileext + \
                    "'"
                print "########################################################"
                print "About to run: "+split_cmd+split_str
                print "########################################################"
                output = subprocess.Popen(split_cmd+split_str,
                                          shell = True, stdout =
                                          subprocess.PIPE).stdout.read()
            except KeyError as e:
                print "############# Incorrect format ##############"
                if manifest_type == "json":
                    print "The format of each json array should be:"
                    print "{start_time: <int>, length: <int>, rename_to: <string>}"
                elif manifest_type == "csv":
                    print "start_time,length,rename_to should be the first line "
                    print "in the csv file."
                print "#############################################"
                print e
                raise SystemExit



def split_by_seconds(filename, split_size, vcodec="copy", acodec="copy",
                     **kwargs):
    if split_size and split_size <= 0:
        print "Split length can't be 0"
        raise SystemExit

    output = subprocess.Popen("ffmpeg -i '"+filename+"' 2>&1 | grep 'Duration'",
                            shell = True,
                            stdout = subprocess.PIPE
                            ).stdout.read()
    print output
    matches = re_length.search(output)
    if matches:
        video_length = int(matches.group(1)) * 3600 + \
                        int(matches.group(2)) * 60 + \
                        int(matches.group(3))
        print "Video length in seconds: "+str(video_length)
    else:
        print "Can't determine video length."
        raise SystemExit
    split_count = int(math.ceil(video_length/float(split_size)))
    if(split_count == 1):
        print "Video length is less then the target split length."
        raise SystemExit

    split_cmd = "ffmpeg -i '%s' -vcodec %s -acodec %s " % (filename, vcodec,
                                                           acodec)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count):
        split_str = ""
        if n == 0:
            split_start = 0
        else:
            split_start = split_size * n

        split_str += " -ss "+str(split_start)+" -t "+str(split_size) + \
                    " '"+filebase + "-" + str(n) + "." + fileext + \
                    "'"
        print "About to run: "+split_cmd+split_str
        output = subprocess.Popen(split_cmd+split_str, shell = True, stdout =
                               subprocess.PIPE).stdout.read()
