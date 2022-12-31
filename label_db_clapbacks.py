import json
import psycopg2

credentials = json.loads(open("credentials.json", "r").read())

conn = psycopg2.connect("dbname='" + credentials["dbname"] + "'")
#  + " host='" + credentials['host'] + "' user='" + credentials['user'] + "' password='" + credentials['passw'] + "' port='" + str(credentials['port']) + "'")
cursor = conn.cursor()

for y in [2015]:
    year = str(y)
    for m in [1, 2]:
        month = str(m)
        if len(month) == 1:
            month = "0" + month

        print("index")
        cursor.execute(
            "CREATE INDEX comments_"
            + year
            + "_"
            + month
            + "_idx ON comments_"
            + year
            + "_"
            + month
            + " (id)"
        )

        print("tstamp")
        cursor.execute(
            "ALTER TABLE comments_"
            + year
            + "_"
            + month
            + " ADD COLUMN tstamp TIMESTAMP"
        )
        cursor.execute(
            "UPDATE comments_"
            + year
            + "_"
            + month
            + " SET tstamp = to_timestamp(created_utc)"
        )
        cursor.execute(
            "ALTER TABLE comments_" + year + "_" + month + " DROP COLUMN created_utc"
        )
        conn.commit()

        print("is clapback")
        cursor.execute(
            "ALTER TABLE comments_" + year + "_" + month + " ADD is_clapback BOOLEAN"
        )
        cursor.execute(
            "UPDATE comments_"
            + year
            + "_"
            + month
            + " SET is_clapback = TRUE WHERE score > 7 AND parent_score > 0 AND score > parent_score * 1.5"
        )

        print("label parents")
        cursor.execute(
            "ALTER TABLE comments_"
            + year
            + "_"
            + month
            + " ADD is_relevant_parent BOOLEAN"
        )
        cursor.execute(
            "UPDATE comments_"
            + year
            + "_"
            + month
            + " SET is_relevant_parent = TRUE WHERE id IN (SELECT parent_id FROM comments_"
            + year
            + "_"
            + month
            + " WHERE score > parent_score)"
        )
        conn.commit()

        print("prune unrelated comments")
        cursor.execute(
            "DELETE FROM comments_"
            + year
            + "_"
            + month
            + " WHERE is_relevant_parent IS NULL AND (score <= 0 OR parent_score >= score)"
        )
        conn.commit()
