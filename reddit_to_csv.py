import json, csv

csvout = csv.writer(
    open("../2015_02.csv", "w"),
    quoting=csv.QUOTE_NONNUMERIC,
    escapechar="\\",
    quotechar='"',
)

parent_scores = {}
bore_comments = ["[deleted]", "[removed]", "#"]

with open("../RC_2015-02", "r") as allcomments:
    index = 0
    for comment_text in allcomments:
        comment = json.loads(comment_text)
        if comment["body"].strip() not in bore_comments:
            parent_scores[comment["id"]] = comment["score"]

        # every 100,000 rows, let us know there's progress
        index = index + 1
        if index % 100_000 == 0:
            print(index)

print("converting to csv")
with open("../RC_2015-02", "r") as allcomments:
    index = 0
    for comment_text in allcomments:
        comment = json.loads(comment_text)
        if comment["body"].strip() not in bore_comments and comment["score"] > 0:
            parent_score = 0
            parent_id = comment["parent_id"][3:]
            if parent_id in parent_scores:
                parent_score = parent_scores[parent_id]
                if parent_score <= 0:
                    continue
            cleantext = (
                comment["body"]
                .replace("\n", " ")
                .replace("\r", "")
                .lower()
                .replace(".", " ")
                .replace("?", "")
                .replace("!", "")
                .replace(" ", "")
            )
            csvout.writerow(
                [
                    comment["id"],
                    comment["body"].replace("\n", " ").replace("\r", "").encode(),
                    comment["score"],
                    parent_id,
                    comment["author"],
                    comment["subreddit"],
                    comment["created_utc"],
                    parent_score,
                    cleantext.encode(),
                ]
            )

        index = index + 1
        if index % 100_000 == 0:
            print(index)
