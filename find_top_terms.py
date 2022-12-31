import json
import psycopg2

credentials = json.loads(open("credentials.json", "r").read())

conn = psycopg2.connect("dbname='" + credentials["dbname"] + "'")
#  + " host='" + credentials['host'] + "' user='" + credentials['user'] + "' password='" + credentials['passw'] + "' port='" + str(credentials['port']) + "'")
cursor = conn.cursor()

cand_terms = []
top_terms = []
for y in [2014]:
    for m in range(1, 13):
        mnth = str(m)
        if len(mnth) == 1:
            mnth = "0" + mnth
        print(str(y) + "_" + mnth)
        cursor.execute(
            "SELECT cleantext FROM comments_"
            + str(y)
            + "_"
            + mnth
            + " where is_clapback group by cleantext order by count(*) desc limit 25"
        )
        results = cursor.fetchall()
        for r in results:
            cleaned = r[0]
            if (
                (cleaned not in top_terms)
                and len(cleaned) > 0
                and ("http://" not in cleaned)
                and ("https://" not in cleaned)
            ):
                if cleaned in cand_terms:
                    top_terms.append(cleaned)
                else:
                    cand_terms.append(cleaned)
        print(top_terms)
