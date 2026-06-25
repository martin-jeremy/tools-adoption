WITH lag_values AS (
    SELECT * FROM {{ ref('int_analytics__lag_values') }}
)

SELECT Source, Name, Metrics, Value, Evolution, Evolution_Pct, collected_at AS CollectionDate FROM lag_values
ORDER BY Name, Metrics, collected_at