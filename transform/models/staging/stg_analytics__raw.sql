SELECT
    provider,
    tool_name,
    tool_desc,
    metric_name,
    value,
    collected_at
FROM {{ source('analytics', 'raw') }}
