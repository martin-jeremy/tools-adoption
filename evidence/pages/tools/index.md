---
title: Details by Tools
full_width: true
---

```sql tool_list
select *, '/tools/' || Name as detailed_link from tools_adoption.overall;
```

<DataTable data={tool_list} search=true>
    <Column id=Name />
    <Column id=Description />
    <Column id=Github_URL contentType="link" />
    <Column id=PyPI_URL contentType="link" />
    <Column id=detailed_link contentType="link" linkLabel="Details →" />
 </DataTable>