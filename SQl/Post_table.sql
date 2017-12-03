CREATE TABLE Post
(
    id SERIAL PRIMARY KEY NOT NULL,
    author_id INT NOT NULL,
    author citext COLLATE pg_catalog.ucs_basic NOT NULL,
    created TIMESTAMP with time zone DEFAULT now() NOT NULL,
    forum_id INT NOT NULL,
    forum citext COLLATE pg_catalog.ucs_basic NOT NULL,
    isEdited BOOLEAN DEFAULT FALSE NOT NULL,
    message TEXT NOT NULL,
    root_parent INT NOT NULL DEFAULT 0,
    parent INT NOT NULL DEFAULT 0,
    path integer[] DEFAULT '{}'::integer[],
    thread_id INT NOT NULL,

  CONSTRAINT Post_forum_id_fk FOREIGN KEY (forum_id)
      REFERENCES Forum (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT Post_thread_id_fk FOREIGN KEY (thread_id)
      REFERENCES public.thread (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT Post_user_id_fk FOREIGN KEY (author_id)
      REFERENCES public."User" (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);