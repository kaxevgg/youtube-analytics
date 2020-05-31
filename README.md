# YouTube Analytics

This is an analytics script written in Python that parses the data output provided by Google. Currently the functionality is limited to calculating total time in seconds spent on YouTube.

The Youtube Video API can be found [here](https://developers.google.com/youtube/v3/docs/videos)

## Setup Instructions

1. Go to [Google Takeout](https://takeout.google.com/)
2. Scroll down to section that reads "YouTube and YouTube Music"
3. Click on "All YouTube data included"
4. Click on "Deselect all"
5. Select "history" and "subscriptions" and click "OK"
6. Click on "Multiple formats"
7. Change the output format for "history" to `JSON` and click "OK"
8. Click on "Next step"
9. Select your preferred method of delivery. Google may take some time to export it.
10. Once it's ready, copy the `watch-history.json` file in the downloaded folder to the cloned git repository
11. Run `python3 history.py`. The script will ask you for some inputs.
12. Enter your Google Cloud API Key. Learn how to get one [here](https://cloud.google.com/docs/authentication/api-keys).
13. Enter the name of the video-history file (By default, this is called `watch-history.json`.
14. Enter the name of the output file to cache the results
15. Hooray! You have successfully the script. Hopefully you haven't wasted too much time on YouTube! :-)
