import os
import re
import shutil
from datetime import datetime


NEW_SP_DIR = "new_sp"
SQL_EXECUTOR_DIR = "SQLExecutor"


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def detect_sp_name(sql_text: str) -> str | None:
    """
    Detect stored procedure name from statements like:
      CREATE PROCEDURE SP_NAME
      ALTER PROCEDURE SP_NAME
      CREATE PROC dbo.SP_NAME
      ALTER PROC [dbo].[SP_NAME]

    Returns base SP name without schema/brackets (e.g., 'SP_NAME').
    """
    pattern = re.compile(
        r"\b(CREATE|ALTER)\s+PROC(?:EDURE)?\s+([\[\]\w\.]+)",
        re.IGNORECASE,
    )
    m = pattern.search(sql_text)
    if not m:
        return None

    full = m.group(2).strip().replace("[", "").replace("]", "")
    parts = [p for p in full.split(".") if p]
    return parts[-1].strip() if parts else None


def backup_proc_name(sp_name: str, when: datetime) -> str:
    # Example: GetOrders_bkp_15Mar2026
    return f"{sp_name}_bkp_{when.strftime('%d%b%Y')}"


def build_backup_sql(sp_name: str, backup_name: str) -> str:
    """
    Generates a backup script that:
    - Reads current proc definition using OBJECT_DEFINITION(OBJECT_ID('SP_NAME'))
    - Extracts body from the first AS occurrence
    - Creates a new proc named SP_NAME_bkp_<DDMMMYYYY>
    """
    return f"""\
DECLARE @definition NVARCHAR(MAX);
SELECT @definition = OBJECT_DEFINITION(OBJECT_ID('{sp_name}'));

IF @definition IS NULL
BEGIN
    RAISERROR('Procedure {sp_name} not found.', 16, 1);
    RETURN;
END;

DECLARE @asPos INT;
SET @asPos = PATINDEX('%AS%', UPPER(@definition));

IF @asPos = 0
BEGIN
    RAISERROR('Unable to locate AS keyword in procedure definition for {sp_name}.', 16, 1);
    RETURN;
END;

DECLARE @body NVARCHAR(MAX);
SET @body = SUBSTRING(@definition, @asPos, LEN(@definition) - @asPos + 1);

IF OBJECT_ID('{backup_name}') IS NOT NULL
BEGIN
    DROP PROCEDURE {backup_name};
END;

DECLARE @createStmt NVARCHAR(MAX);
SET @createStmt = 'CREATE PROCEDURE {backup_name} ' + CHAR(13) + CHAR(10) + @body;

EXEC sp_executesql @createStmt;
"""


def write_backup_file(sp_name: str, backup_sql: str) -> str:
    """
    Writes backup file to NEW_SP_DIR as: SP_NAME_backup.sql
    Returns the path.
    """
    filename = f"{sp_name}_backup.sql"
    out_path = os.path.join(NEW_SP_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(backup_sql)
    return out_path


def copy_to_sqlexecutor(*paths: str) -> None:
    ensure_dir(SQL_EXECUTOR_DIR)
    for src in paths:
        dst = os.path.join(SQL_EXECUTOR_DIR, os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"[INFO] Copied '{src}' -> '{dst}'")


def main() -> None:
    ensure_dir(NEW_SP_DIR)
    ensure_dir(SQL_EXECUTOR_DIR)

    sql_files = [
        os.path.join(NEW_SP_DIR, f)
        for f in os.listdir(NEW_SP_DIR)
        if f.lower().endswith(".sql")
    ]

    if not sql_files:
        print(f"[INFO] No .sql files found in '{NEW_SP_DIR}'. Nothing to do.")
        return

    print(f"[INFO] Found {len(sql_files)} .sql file(s) in '{NEW_SP_DIR}'.")
    today = datetime.today()

    for file_path in sql_files:
        print(f"\n[INFO] Processing: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                sql_text = f.read()
        except Exception as exc:
            print(f"[ERROR] Failed to read '{file_path}': {exc}")
            continue

        sp_name = detect_sp_name(sql_text)
        if not sp_name:
            print(f"[WARN] Could not detect stored procedure name in '{file_path}'. Skipping.")
            continue

        print(f"[INFO] Detected SP name: {sp_name}")

        bkp_name = backup_proc_name(sp_name, today)
        backup_sql = build_backup_sql(sp_name, bkp_name)
        backup_file = write_backup_file(sp_name, backup_sql)
        print(f"[INFO] Backup script created: {backup_file} (creates {bkp_name})")

        copy_to_sqlexecutor(backup_file, file_path)

    print("\n[INFO] Done.")


if __name__ == "__main__":
    main()

