create_user = '''with try_insert as (INSERT INTO "User" (about, email, fullname, nickname) VALUES
                ($1, $2, $3, $4)
                ON CONFLICT DO NOTHING
                RETURNING about, email, fullname, nickname, true)
                
                select * from try_insert
                
                union all
                
                select about, email, fullname, nickname, false from "User" 
                where nickname = $4 or email = $2'''

get_user = '''SELECT about, email, fullname, nickname FROM "User" where nickname = $1'''

up_u = '''with conflict_email as (
                select id,about,email,fullname,nickname, false from "User" where email = {}
                ), 
                
                '''

up_u_2 = '''
union all
select * from conflict_email
                
                '''

update_user = '''
try_update as (
                UPDATE "User" set {} where nickname = {} and {} not in (select email from conflict_email)
                returning id, about, email,fullname, nickname, true
                )
                
                select * from try_update'''

