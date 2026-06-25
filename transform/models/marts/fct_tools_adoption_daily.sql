WITH lag_values AS (
    SELECT *, FROM {{ ref('int_analytics__lag_values') }}
)
SELECT Source, Name, Metrics, Value, Evolution, Evolution_Pct FROM lag_values
WHERE Rank = 1