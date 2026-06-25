---
title: Daily Adoption
---

```sql snapshot
select * from tools_adoption.daily
```

```sql github_stars
select * from tools_adoption.daily
where Metrics = 'stars'
order by Value desc
```

```sql pypi_downloads
select * from tools_adoption.daily
where Metrics = 'downloads'
order by Value desc
```


## GitHub Stars

<BarChart
  data={github_stars}
  x=Name
  y=Value
  yAxisTitle="Stars"
  swapXY=true
/>

<DataTable data={github_stars} rows=10>
  <Column id=Name />
  <Column id=Value title="Stars" fmt=num0 />
  <Column id=Evolution title="Δ J-1" fmt="+#,##0;-#,##0" />
  <Column id=Evolution_Pct title="%" fmt="+0.00%;-0.00%" />
</DataTable>

## PyPI Downloads

<BarChart
  data={pypi_downloads}
  x=Name
  y=Value
  yAxisTitle="Downloads"
  swapXY=true
/>

<DataTable data={pypi_downloads} rows=10>
  <Column id=Name />
  <Column id=Value title="Downloads" fmt=num0 />
  <Column id=Evolution title="Δ J-1" fmt="+#,##0;-#,##0" />
  <Column id=Evolution_Pct title="%" fmt="+0.00%;-0.00%" />
</DataTable>