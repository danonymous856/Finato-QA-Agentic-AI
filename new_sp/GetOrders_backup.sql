DECLARE @definition NVARCHAR(MAX);
SELECT @definition = OBJECT_DEFINITION(OBJECT_ID('GetOrders'));

IF @definition IS NULL
BEGIN
    RAISERROR('Procedure GetOrders not found.', 16, 1);
    RETURN;
END;

DECLARE @asPos INT;
SET @asPos = PATINDEX('%AS%', UPPER(@definition));

IF @asPos = 0
BEGIN
    RAISERROR('Unable to locate AS keyword in procedure definition for GetOrders.', 16, 1);
    RETURN;
END;

DECLARE @body NVARCHAR(MAX);
SET @body = SUBSTRING(@definition, @asPos, LEN(@definition) - @asPos + 1);

IF OBJECT_ID('GetOrders_bkp_19Mar2026') IS NOT NULL
BEGIN
    DROP PROCEDURE GetOrders_bkp_19Mar2026;
END;

DECLARE @createStmt NVARCHAR(MAX);
SET @createStmt = 'CREATE PROCEDURE GetOrders_bkp_19Mar2026 ' + CHAR(13) + CHAR(10) + @body;

EXEC sp_executesql @createStmt;
