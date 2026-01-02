LOAD CSV WITH HEADERS FROM 'file:///usersha1-artmbid-artname-plays.csv' AS row
WITH row
WHERE row.user_sha1 IS NOT NULL
  AND row.artist_id IS NOT NULL
  AND row.plays IS NOT NULL

MERGE (u:User {user_sha1: row.user_sha1})
MERGE (a:Artist {
  artist_id: row.artist_id,
  name: row.artist_name
})
MERGE (u)-[r:LISTENED_TO]->(a)
SET r.plays = toInteger(row.plays);
