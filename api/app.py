from flask import Flask, render_template, make_response, request
from threads import Threads
import json

app = Flask(__name__)
threads = Threads()

# TO RUN: python app.py

# called by index.html and results.html
@app.route('/results', methods=['POST'])
def results():
    username = request.form['username']
    return make_html_from_threads(sort_threads_by_likes(all_threads(username)))

def all_threads(username):
    try:
        user_id = threads.public_api.get_user_id(username=username)
    except:
        return []

    user = threads.public_api.get_user(id=user_id)
    user_threads = threads.public_api.get_user_threads(id=user_id)

    threads_list = user_threads["data"]["mediaData"]["threads"]

    # filter out rethreads
    threads_list = [thread["thread_items"][0]["post"] for thread in threads_list if thread["thread_items"][0]["post"]["caption"] is not None]
    return threads_list

def sort_threads_by_likes(threads_list):
    # sort by likes
    threads_list.sort(key=lambda thread : thread["like_count"], reverse = True)
    return threads_list[:10]

def make_html_from_threads(threads_list):
    if threads_list == []:
        html = render_template('error.html')
        response = make_response(html)
        return response

    threads_text_list = [thread["caption"]["text"] for thread in threads_list]
    threads_image_list = [thread["image_versions2"]["candidates"][0]["url"] if len(thread["image_versions2"]["candidates"]) > 0 else None for thread in threads_list]
    threads_video_list = [thread["video_versions"][0]["url"] if len(thread["video_versions"]) > 0 else None for thread in threads_list]
    threads = zip(threads_text_list, threads_image_list, threads_video_list)

    html = render_template('results.html', threads=threads)
    response = make_response(html)
    return response

@app.route("/")
def index():
    html = render_template('index.html')
    response = make_response(html)
    return response

if __name__ == "__main__":
    app.run(debug=True)
