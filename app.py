from flask import Flask, render_template, make_response
from threads import Threads
import json

app = Flask(__name__)
threads = Threads()

# print(user_threads)

# TO RUN: python app.py


def preprocess_threads(username):
    # retrieve threads
    user_id = threads.public_api.get_user_id(username=username)
    user = threads.public_api.get_user(id=user_id)
    user_threads = threads.public_api.get_user_threads(id=user_id)


    threads_list = user_threads["data"]["mediaData"]["threads"]

    # filter out rethreads
    threads_list = [thread["thread_items"][0]["post"] for thread in threads_list if thread["thread_items"][0]["post"]["caption"] is not None]

    # sort by likes
    threads_list.sort(key=lambda thread : thread["like_count"], reverse = True)

    return threads_list[:10]

@app.route("/debug")
def debug():
    return preprocess_threads("briantieu")

@app.route("/")
def index():
    threads_list = preprocess_threads("briantieu")
    threads_text_list = [thread["caption"]["text"] for thread in threads_list]
    threads_image_list = [thread["image_versions2"]["candidates"][0]["url"] if len(thread["image_versions2"]["candidates"]) > 0 else None for thread in threads_list]
    threads_video_list = [thread["video_versions"][0]["url"] if len(thread["video_versions"]) > 0 else None for thread in threads_list]

    threads = zip(threads_text_list, threads_image_list, threads_video_list)
    html = render_template('index.html', threads=threads)

    response = make_response(html)
    return response


if __name__ == "__main__":
    app.run(debug=True)
