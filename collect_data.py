import praw
import pickle
import pandas as pd
import datetime as dt

from praw.models import MoreComments


def main():
    ###CONSTANTS###

    LIMIT = 30000
    TOP_COMMENTS = 20

    ###



    reddit = praw.Reddit(client_id='fQNtP7lajdu7XA',
                         client_secret='GJce-qB0y7ait5bfBNmZfKj7Cb0',
                         user_agent='viewpoint_visualizer',
                         username='cs5984_dhruva',
                         password='cs5984')
    subreddit = reddit.subreddit('changemyview')
    top_subreddit = subreddit.top(limit=LIMIT)

    data = {"title": [],
            "score": [],
            "id": [],
            "url": [],
            "comms_num": [],
            "created": [],
            "body": [],
            "comments": []}

    # with open("data.pickle", 'rb') as file:
    #     data = pickle.load(file)
    #
    # old_id_set = set(data["id"])

    i = 1
    for submission in top_subreddit:
        # if submission.id in old_id_set:
        #     print(submission.id)
        #     continue
        # else:
        #     print(submission.id)
        print("iteration: ",i)  # iteration number
        i += 1
        data["title"].append(submission.title)
        data["score"].append(submission.score)
        data["id"].append(submission.id)
        data["url"].append(submission.url)
        data["comms_num"].append(submission.num_comments)
        data["created"].append(submission.created)
        data["body"].append(submission.selftext)

        comments = []
        for top_lvl_comment in submission.comments:
            if isinstance(top_lvl_comment, MoreComments):
                continue
            if top_lvl_comment.body != "[removed]" and top_lvl_comment.body != "[deleted]":
                comments.append((top_lvl_comment.body, top_lvl_comment.score))
        comments = sorted(comments, key=lambda x: x[1], reverse=True)[:TOP_COMMENTS]

        data["comments"].append(comments)
        if (i % 1000 == 0):
            now = dt.datetime.now()
            with open("data_"+str(now.day)+"-"+str(now.hour)+"-"+str(now.minute)+".pickle", "wb") as f:
                pickle.dump(data, f)

    # topics_data = pd.DataFrame(topics_dict)
    # topics_data.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
