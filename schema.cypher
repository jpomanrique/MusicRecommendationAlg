CREATE INDEX user_sha1_index IF NOT EXISTS
FOR (u:User) ON (u.user_sha1);

CREATE INDEX artist_id_index IF NOT EXISTS
FOR (a:Artist) ON (a.artist_id);