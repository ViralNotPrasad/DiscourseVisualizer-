import praw
import pandas as pd
import datetime as dt

from praw.models import MoreComments


def main():
    reddit = praw.Reddit(client_id='fQNtP7lajdu7XA',
                         client_secret='GJce-qB0y7ait5bfBNmZfKj7Cb0',
                         user_agent='viewpoint_visualizer',
                         username='cs5984_dhruva',
                         password='cs5984')
    print(reddit.read_only)
    subreddit = reddit.subreddit('changemyview')
    top_subreddit = subreddit.top(limit=1000)

    topics_dict = {"title": [],
                   "score": [],
                   "id": [],
                   "url": [],
                   "comms_num": [],
                   "created": [],
                   "body": [],
                   "comments": []}

    i = 1
    for submission in top_subreddit:
        print(i)
        i += 1
        comments = []
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)

        for top_lvl_comment in submission.comments:
            if isinstance(top_lvl_comment, MoreComments):
                continue
            comments.append((top_lvl_comment.body, top_lvl_comment.score))
        comments.sort(key=lambda x: x[1], reverse=True)
        topics_dict["comments"] = comments

    topics_data = pd.DataFrame(topics_dict)
    topics_data.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
