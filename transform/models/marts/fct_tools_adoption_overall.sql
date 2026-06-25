WITH overall AS (
    SELECT * FROM {{ ref('int_analytics__setup_overall') }}
)
SELECT
    tool_name as Name,
    tool_desc as Description,
    gh_url as Github_URL,
    pypi_url as PyPI_URL
FROM overall