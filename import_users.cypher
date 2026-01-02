LOAD CSV WITH HEADERS FROM 'file:///usersha1-profile.csv' AS row
WITH row
WHERE row.user_sha1 IS NOT NULL AND row.user_sha1 <> ''

MERGE (u:User {user_sha1: row.user_sha1});
