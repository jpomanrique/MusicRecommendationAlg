# Sistema de Recomendação Musical com Neo4j

Projeto desenvolvido a partir do dataset **Last.fm (Kaggle)**, contendo usuários, artistas e histórico de reproduções (*plays*), com o objetivo de construir um **grafo de recomendação musical** utilizando **Neo4j**.

- Dataset original e descrição do formato dos arquivos:  
  https://www.upf.edu/web/mtg/lastfm360k
- Dataset utilizado neste projeto (Kaggle):  
  https://www.kaggle.com/datasets/neferfufi/lastfm  

> **Recomendação:** utilize a versão do Kaggle, pois é a que contém exatamente os arquivos usados neste projeto.

**Projeto grafo de recomendação musical por Similaridade:**  
**John Peter Oyardo Manrique**

---

## 📌 Visão Geral

Este Sistema de recomendação foi desenvolvido usando Last.fm (Kaggle) qual contêm usuários, artistas, tags, plays… para fazer um grafo de recomendação de Musica.

Este projeto implementa um **sistema de recomendação musical** utilizando **Neo4j** e **Cypher**, baseado em dados reais de escuta de usuários. O objetivo é demonstrar como modelar dados musicais em grafo e extrair recomendações a partir de padrões de comportamento dos usuários.

O sistema utiliza **collaborative filtering baseado em usuários**, explorando relações entre usuários e artistas para sugerir novos artistas que um usuário ainda não escutou.

---

## 🧱 Modelo de Dados

### Nós
- **User**
  - `user_id` (hash SHA-1 do usuário)
  - `age` (opcional)
  - `gender` (opcional)
  - `country` (opcional)

- **Artist**
  - `artist_id`
  - `name`

### Relacionamentos
- **LISTENED_TO**
  - Conecta `User → Artist`
  - Propriedade:
    - `plays`: número de reproduções

---

## 📂 Estrutura de Arquivos

```
.
├── schema.cypher
├── import_users.cypher
├── import_listens.cypher
├── recommendations.cypher
│
├── data/
│   ├── userid-timestamp-artid-artname-traid-traname.tsv
│   ├── usersha1-profile.tsv
│   └── usersha1-profile.csv
│
├── scripts/
│   ├── script01.py
│   └── script02.py
│
└── README.md
```

---

## ⚙️ Pré-requisitos

- Neo4j 5.x ou superior
- Java 17+
- Python 3.9+ (opcional, para pré-processamento)
- Acesso ao Neo4j Browser ou Neo4j Desktop

---

## 🚀 Execução

### 1️⃣ Preparar os dados
Importante: Copie os arquivos `.tsv` ou `.csv` para a pasta de importação local do Neo4j: ../neo4j/import/


Executar Script01.py e sript02.py para converter os arquivos `.tsv` para `.csv` usando python 
```
# SCRIPT 1 — 
# CONVERTER userid-timestamp-artid-artname-traid-traname.tsv
# para istening_events.csv
# SCRIPT 2 — 
CONVERTER usersha1-artmbid-artname-plays.tsv
# para user_artist_plays.csv
---

### 2️⃣ Abrir Neo4j e criar constraints e índices.

Execute no Neo4j Browser:

```cypher
CREATE CONSTRAINT user_id_unique IF NOT EXISTS
FOR (u:User)
REQUIRE u.user_id IS UNIQUE;

CREATE CONSTRAINT artist_id_unique IF NOT EXISTS
FOR (a:Artist)
REQUIRE a.artist_id IS UNIQUE;
```

---

### 3️⃣ Carregar dados de escuta
```cypher
LOAD CSV FROM 'file:///userid-timestamp-artid-artname-traid-traname.tsv' AS row
FIELDTERMINATOR '\t'
WITH row
MERGE (u:User {user_id: row[0]})
MERGE (a:Artist {artist_id: row[2]})
SET a.name = row[3]
MERGE (u)-[r:LISTENED_TO]->(a)
ON CREATE SET r.plays = 1
ON MATCH SET r.plays = r.plays + 1;
```

---

### 4️⃣ Carregar perfis de usuários
```cypher
LOAD CSV WITH HEADERS FROM 'file:///usersha1-profile.csv' AS row
WITH row
WHERE row.user_sha1 IS NOT NULL AND row.user_sha1 <> ''
MERGE (u:User {user_id: row.user_sha1})
SET
  u.gender = row.gender,
  u.country = row.country,
  u.age = CASE
            WHEN row.age IS NULL OR row.age = '' THEN null
            ELSE toInteger(row.age)
          END;
```

Detalhe de execução dos Arquivos Cypher em Neo4j:

1.- schema.cypher        → copiar / colar / run
2.- import_users.cypher  → run
3.- import_listens.cypher→ run
4.- recommendations.cypher → testar


🔹 Passo 1 — Criar Schema

Arquivo: schema.cypher

Cria constraints e índices para garantir unicidade e performance.

➡️ Deve ser executado primeiro.

🔹 Passo 2 — Importar Usuários

Arquivo: import_users.cypher

Carrega os perfis dos usuários (idade, país, gênero) e cria nós User.

🔹 Passo 3 — Importar Escutas

Arquivo: import_listens.cypher

Cria nós Artist e relacionamentos LISTENED_TO, acumulando o número de reproduções (plays).

Este é o passo mais pesado do projeto.

🔹 Passo 4 — Gerar Recomendações

Arquivo: recommendations.cypher

Executa o algoritmo de recomendação baseado em usuários com gostos similares.

Substitua <USER_ID> por um user_id válido do banco. 
---

### 5️⃣ Executar recomendações
```cypher
MATCH (u:User {user_id:'<USER_ID>'})-[:LISTENED_TO]->(a:Artist)
MATCH (other:User)-[:LISTENED_TO]->(a)
WHERE other <> u
MATCH (other)-[r:LISTENED_TO]->(rec:Artist)
WHERE NOT (u)-[:LISTENED_TO]->(rec)
RETURN rec.name AS artist, sum(r.plays) AS score
ORDER BY score DESC
LIMIT 10;
```

exemplo -> <USER_ID> = user_sha1:'00000c289a1829a808ac09c00daf10bc3c4e223b'

---

## 📊 Resultados Esperados:

Após a execução completa do pipeline:

Milhões de relações LISTENED_TO

Usuários com histórico real de escuta

Recomendações personalizadas por usuário

🔎 Exemplo de Saída

Para um usuário que escuta rock alternativo:

artist	score
Radiohead	8421
Muse	7904
Arctic Monkeys	7550
The Strokes	7312
Pixies	6981

➡️ Esses artistas são populares entre usuários por similaridade (comportamento semelhante).

O score representa a relevância baseada no volume de reproduções dos usuários similares.

- O banco Neo4j conterá milhões de relações `LISTENED_TO`
- Usuários válidos terão histórico de escuta (`degree > 0`)
- As consultas de recomendação retornarão artistas:
  - Não escutados pelo usuário-alvo
  - Populares entre usuários com gostos semelhantes
- O score indica relevância baseada em volume de reproduções

---

## 🧪 Validação Rápida

```cypher
MATCH (:User)-[r:LISTENED_TO]->(:Artist)
RETURN count(r);
```

```cypher
MATCH (u:User {user_id:'<USER_ID>'})-[:LISTENED_TO]->(a)
RETURN count(a);
```

---

## 📌 Observações

- Certifique-se de usar o valor correto de `user_id` (hash SHA-1).
- Recomenda-se testar com usuários que possuam histórico significativo.
- O modelo pode ser facilmente estendido para outros tipos de recomendação.

---

## 📄 Licença
Projeto acadêmico / educacional.

John Peter Oyardo Manrique
jpomanrique@gmail.com
