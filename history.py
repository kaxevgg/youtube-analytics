import json
import requests
# from pprint import pp
import re

def get_video_ids(history_file_path):
    with open(history_file_path, 'r') as json_file:
        data = json.load(json_file)
        id_list = []
        removed_videos = []
        video_id = ''
        for video in data:
            if ('titleUrl' in video.keys()):
                video_id = video['titleUrl'].replace("https://www.youtube.com/watch?v=","")
                id_list.append(video_id)
            else:
                removed_videos.append(video)
        json_file.close()
        return id_list

def get_video_data(video_id_list_string, api_key):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={
        'part': 'snippet,contentDetails,statistics',
        'id': video_id_list_string,
        'key': api_key
    })
    return json.loads(response.content)

def parse_duration_in_seconds(duration_string):
    #P3Y6M2W4DT12H30M5S
    matches = re.search("(-)?P(?:([.,\d]+)Y)?(?:([.,\d]+)M)?(?:([.,\d]+)W)?(?:([.,\d]+)D)?T(?:([.,\d]+)H)?(?:([.,\d]+)M)?(?:([.,\d]+)S)?", duration_string)
    total_seconds = 0
    if matches is not None:
        days = matches.groups()[4]
        hours = matches.groups()[5]
        minutes = matches.groups()[6]
        seconds = matches.groups()[7]
        if (days is not None):
            total_seconds += int(days) * 86400
        if (hours is not None):
            total_seconds += int(hours) * 3600
        if (minutes is not None):
            total_seconds += int(minutes) * 60
        if (seconds is not None):
            total_seconds += int(seconds)
        return total_seconds
    return 0
    
def print_result(video_data):
    total_time_in_seconds = 0
    for video in video_data:
        video_duration = video['contentDetails']['duration']
        total_time_in_seconds += parse_duration_in_seconds(video_duration)

    print("\n")
    print("----------TIME WASTED ON YOUTUBE (IN SECONDS)-----------")
    print(total_time_in_seconds)
    
    
def main():
    print("Welcome to the Youtube Time Wasted Program. Please enter the following details:\n")
    api_key = input("Google Cloud API Key: ")
    video_history_file_name = input("Watch history file name: ")
    output_file_name = input("Output file name: ")

    video_ids = get_video_ids(video_history_file_name)
    video_data = []
    limit = len(video_ids)
    step = 50

    with open(output_file_name,'r+') as videoDataFile:
        try:
            vdata = json.load(videoDataFile)
            print(len(vdata))
            if (len(vdata) > 0):
                print("File contains data! Using cached information")
                print_result(vdata)
        except:
            print("File is empty! Starting fresh update")

            for i in range(0,limit,step):
                print("Starting Index: " + str(i))
                if (i+step >= limit):
                    print("Over limit")
                    id_list_string = ",".join(video_ids[i:limit])
                    print("Ending Index: " + str(limit-1))
                    print('Added ' + str(limit) + " videos\n")
                else:
                    print("I'm okay")
                    id_list_string = ",".join(video_ids[i:i+step])
                    print("Ending Index: " + str(i+step-1))
                    print('Added ' + str(i+step) + " videos\n")

                response = get_video_data(id_list_string, api_key)['items']
                video_data.extend(response)

            videoDataFile.write(json.dumps(video_data, indent=4, sort_keys=True))

            print_result(video_data)
        
        videoDataFile.close()
    

if __name__ == "__main__":
    main()