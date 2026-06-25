---
title: Details by Tools
hide_toc: false
---

```sql tool_list
select name from tools_adoption.daily group by 1;
```

{#each tool_list as tool}
- [{tool.Name}](/tools/{tool.Name})

{/each}