# `database-files` Folder

You'll put your data model (SQL DDL) in this folder along with sample data.  To get MySQL to execute the SQL files, you need to delete your MySQL Container and totally recreate it.  You can use:

```bash
docker compose down && docker compose up
```

This will delete and recreate all the containers, including MySQL. 