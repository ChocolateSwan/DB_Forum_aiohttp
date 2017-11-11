CREATE FUNCTION update_count_of_threads_in_forum() RETURNS TRIGGER AS '
BEGIN
update forum set threads = threads + 1 where id = NEW.forum_id;
return NEW;
END;
' LANGUAGE  plpgsql;

CREATE TRIGGER trigger_update_count_of_threads_in_forum
AFTER INSERT ON thread FOR EACH ROW
EXECUTE PROCEDURE update_count_of_threads_in_forum();
