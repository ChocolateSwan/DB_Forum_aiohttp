create_user = '''with try_insert as (INSERT INTO "User" (about, email, fullname, nickname) VALUES
                ($1, $2, $3, $4)
                ON CONFLICT DO NOTHING
                RETURNING about, email, fullname, nickname, true)
                
                select * from try_insert
                
                union all
                
                select about, email, fullname, nickname, false from "User" 
                where nickname = $4 or email = $2'''

get_user = '''SELECT about, email fullname, nickname FROM "User" where'''