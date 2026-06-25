WITH overall AS (
    SELECT * FROM {{ ref('stg_analytics__raw') }}
),
github AS (
    SELECT
        tool_name,
        tool_desc,
        tool_url AS github_url
    FROM overall
    WHERE provider = 'Github'
),
pypi AS (
    SELECT
        tool_name,
        tool_desc,
        tool_url AS pypi_url
    FROM overall
    WHERE provider = 'PyPI Stats'
)
SELECT
    COALESCE(g.tool_name, p.tool_name) AS tool_name,
    COALESCE(g.tool_desc, p.tool_desc) AS tool_desc,
    g.github_url AS gh_url,
    p.pypi_url AS pypi_url
FROM github g
FULL OUTER JOIN pypi p ON g.tool_name = p.tool_name