WITH raw AS (
    SELECT *,
           COALESCE(LAG(value) OVER (PARTITION BY provider, tool_name, metric_name ORDER BY collected_at), value) as previous_value,
           ROW_NUMBER() OVER (PARTITION BY provider, tool_name, metric_name ORDER BY collected_at DESC) as rn
    FROM {{ ref('stg_analytics__raw') }}
)
SELECT
    provider AS 'Source',
    tool_name AS 'Name',
    metric_name AS 'Metrics',
    value AS 'Value',
    value - previous_value AS 'Evolution',
    (value - previous_value) / value * 100 AS 'Evolution_Pct',
    rn AS 'Rank'
FROM raw