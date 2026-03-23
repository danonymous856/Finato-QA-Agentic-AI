-- Example new stored procedure deployment script
-- (This is the "new SP script" you drop into new_sp/)

CREATE PROCEDURE dbo.GetOrders
AS
BEGIN
    SET NOCOUNT ON;
    SELECT 1 AS Ok;
END
GO

