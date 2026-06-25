SELECT
    provider,
    tool_name,
    tool_desc,
    tool_url,
    metric_name,
    value,
    collected_at
FROM {{ source('analytics', 'raw') }}
