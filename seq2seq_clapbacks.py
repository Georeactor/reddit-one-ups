import json
import psycopg2

credentials = json.loads(open("credentials.json", "r").read())

conn = psycopg2.connect("dbname='" + credentials["dbname"] + "'")
#  + " host='" + credentials['host'] + "' user='" + credentials['user'] + "' password='" + credentials['passw'] + "' port='" + str(credentials['port']) + "'")
cursor = conn.cursor()

starter_table = "comments_2014_01"
years = ["2014"]
monthly_seq = int(20_000 / 12)
clapbacks = [
    "yes",
    "no",
    "you'rewelcome",
    "darude-sandstorm",
    "ಠ◡ಠ",
    "nope",
    "notwiththatattitude",
    "lol",
    "mom'sspaghetti",
    "what",
    "exactly",
    "k",
    "wat",
    "andmyaxe",
    "thatsthejokejpg",
    "why",
    "thanks",
    ":(",
    "/r/shittytumblrgifs",
    "┬─┬ノ(ಠ_ಠノ)",
    "stopit",
    "ok",
    "whoosh",
    "that'swhatshesaid",
    "(͡°͜ʖ͡°)",
    "you'refuckingwelcome",
    "/r/theydidthemonstermath",
    "both",
    "yep",
    "ಠ_ಠ",
    '"couldn\'tcareless"',
    "yup",
    "allofthem",
    "ayylmao",
    "yeah",
    "woosh",
    "that'sthejoke",
]

cursor.execute(
    "CREATE TABLE seq_clapbacks AS (SELECT * FROM " + starter_table + ") LIMIT 0"
)
cursor.execute("ALTER TABLE seq_clapbacks ADD COLUMN parent_body TEXT")
conn.commit()

for y in years:
    for m in range(1, 13):
        mnth = str(m)
        if len(mnth) == 1:
            mnth = "0" + mnth
        print(str(y) + "_" + mnth)

        cursor.execute(
            "INSERT INTO seq_clapbacks (id, body, score, parent_id, author, subreddit, parent_score, cleantext, tstamp, is_clapback, is_relevant_parent) (SELECT id, body, score, parent_id, author, subreddit, parent_score, cleantext, tstamp, is_clapback, is_relevant_parent FROM comments_"
            + str(y)
            + "_"
            + mnth
            + " where is_clapback and cleantext != ANY(%s) AND subreddit != 'IAmA' ORDER BY score DESC LIMIT %s)",
            (clapbacks, monthly_seq),
        )
        conn.commit()

for y in years:
    for m in range(1, 13):
        mnth = str(m)
        if len(mnth) == 1:
            mnth = "0" + mnth
        print(str(y) + "_" + mnth)
        cursor.execute(
            "WITH parents AS (SELECT id, body FROM comments_"
            + str(y)
            + "_"
            + mnth
            + " WHERE is_relevant_parent) UPDATE seq_clapbacks SET parent_body = (SELECT body FROM parents WHERE parents.id = seq_clapbacks.parent_id) WHERE parent_body IS NULL"
        )
cursor.execute("DELETE FROM seq_clapbacks WHERE parent_body IS NULL")
cursor.execute("ALTER TABLE seq_clapbacks DROP COLUMN is_clapback")
cursor.execute("ALTER TABLE seq_clapbacks DROP COLUMN is_relevant_parent")
cursor.execute("ALTER TABLE seq_clapbacks DROP COLUMN cleantext")
conn.commit()
