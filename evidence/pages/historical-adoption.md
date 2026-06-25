---
title: Historical Adoption
---


```sql history_stars
select * from tools_adoption.history
where Metrics = 'stars'
order by name, collectiondate desc
```

```sql history_downloads
select * from tools_adoption.history
where Metrics = 'downloads'
```

## Historical — Stars

<LineChart
  data={history_stars}
  x=CollectionDate
  y=Value
  series=Name
  yAxisTitle="Stars"
/>

<DataTable data={history_stars} rows=10>
  <Column id=Name />
  <Column id=Value title="Stars" fmt=num0 />
  <Column id=Evolution title="Δ J-1" fmt="+#,##0;-#,##0" />
  <Column id=Evolution_Pct title="%" fmt="+0.00%;-0.00%" />
  <Column id=CollectionDate title="Collection Date" fmt="yyyy-MM-dd hh:mm:ss"/>
</DataTable>


## Historical — PyPI Downloads

<LineChart
  data={history_downloads}
  x=CollectionDate
  y=Value
  series=Name
  yAxisTitle="Downloads / day"
/>

<DataTable data={history_downloads} rows=10>
  <Column id=Name />
  <Column id=Value title="Stars" fmt=num0 />
  <Column id=Evolution title="Δ J-1" fmt="+#,##0;-#,##0" />
  <Column id=Evolution_Pct title="%" fmt="+0.00%;-0.00%" />
  <Column id=CollectionDate title="Collection Date" fmt="yyyy-MM-dd hh:mm:ss"/>"
</DataTable>