import json
import pandas as pd
import pickle
import datetime as dt

def main():
    TOP_COMMENTS = 20
    data = {"title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": [],
            "comments": []}

    with open("cmv_20161111.jsonlist", "rb") as f:
        datalines = f.readlines()
        count = 0
        for dataline in datalines:

            submission = json.loads(dataline)
            data["title"].append(submission["title"])
            data["score"].append(submission["score"])
            data["id"].append(submission["id"])
            data["url"].append(submission["url"])
            data["comms_num"].append(submission["num_comments"])
            data["created"].append(submission["created"])
            data["body"].append(submission["selftext"])
            comments = []
            for top_lvl_comment in submission["comments"]:
                if "body" in top_lvl_comment and top_lvl_comment["body"] != "[removed]" and top_lvl_comment['body'] != "[deleted]":
                    comments.append((top_lvl_comment['body'], top_lvl_comment["score"]))
            comments = sorted(comments, key=lambda x: x[1], reverse=True)[:TOP_COMMENTS]

            data["comments"].append(comments)
            count+=1
            print("iteration:", count)

        now = dt.datetime.now()
        with open("data_"+str(now.day)+"-"+str(now.hour)+"-"+str(now.minute)+".pickle", "wb") as f:
            pickle.dump(data, f)

if __name__ == '__main__':
    main()

