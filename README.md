# DeepClapback

A Reddit comment dataset which searches for 'clapbacks' (comments
 which are scored higher than the original comments) and
 set up CSVs for a classification model.

Article on V1: "Can DeepClapback learn to lol?" https://blog.goodaudience.com/can-deepclapback-learn-when-to-lol-e4a2092a8f2c

## Setup

Install PostgreSQL, Python / PIP. Create a database called 'comments'.

Download a monthly archive from https://files.pushshift.io/reddit/comments

- unzstd RC_2014-02.zst --memory=2048MB
- rm RC_2014-02.zst
- python3 clean_clapbacks_csv.py
- psql -d comments

Import the CSV into the database:

```sql
CREATE TABLE comments_2014_08 (
    id VARCHAR(20),
    body TEXT,
    score INT,
    parent_id VARCHAR(20),
    author VARCHAR(30),
    subreddit TEXT,
    created_utc BIGINT,
    parent_score INT,
    cleantext TEXT
);
\copy comments_2014_02 FROM '2014_02.csv' CSV;
```

Scripts to index rows, find clapbacks, and label relevant parent comments:

- pip3 install psycopg2
- python3 label_db_clapbacks.py

Find top terms (appear in top 25 clapback-meme replies for the month, for 2 or more months):

- python3 find_top_terms.py

Use the top terms to create one clapbacks table, with parent_body column filled (will remove some comments from early January where the parent comment is missing from the year).

- python3 extract_clapbacks.py

Save the clapbacks to a CSV file:

```
\copy clapbacks to 'clapbacks.csv' DELIMITER ',' CSV HEADER;
```

To list seq2seq clapbacks, run this script which picks several freeform clapbacks, i.e. they are not repetitive meme replies. The number of comments picked from each month is `monthly_seq` (default of 20,000 / 12), with only the highest score replies within each month being selected. The IAmA subreddit is excluded, because answers generally score higher than questions.

- python3 seq2seq_clapbacks.py

```
\copy seq_clapbacks to 'seq2seq_clapbacks.csv' DELIMITER ',' CSV HEADER;
```


## Content Warning

Comments and responses in the Reddit archives and output datasets all include NSFW language and links!

When you use the dataset, you can use the subreddit and score columns to perhaps filter out NSFW and otherwise toxic content.

## License

Reddit comments are properties of Reddit and comment owners using their Terms of Service

MIT license on this version
