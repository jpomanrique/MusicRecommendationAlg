MATCH (u:User {user_sha1:'00000c289a1829a808ac09c00daf10bc3c4e223b'})
      -[:LISTENED_TO]->(a)
MATCH (other:User)-[:LISTENED_TO]->(a)
WHERE other <> u
MATCH (other)-[r:LISTENED_TO]->(rec:Artist)
WHERE NOT EXISTS {
  MATCH (u)-[:LISTENED_TO]->(rec)
}

RETURN rec.name AS artist, sum(r.plays) AS score
ORDER BY score DESC
LIMIT 10;
