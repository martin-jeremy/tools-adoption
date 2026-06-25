WITH overall AS (
    SELECT * FROM {{ ref('stg_analytics__raw') }}
)
SELECT
    provider AS Source,
    tool_name AS Name,
    tool_desc AS Description,
    tool_url AS URL
FROM overall