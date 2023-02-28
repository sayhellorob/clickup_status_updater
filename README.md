# clickup_status_updater

Sets tasks to "In Progress" if ClickUp Custom Date is equal to or less than current date. 


# Installation

1. Load full bundle into Lambda
2. Set Environment Variables
  * CLICKUP_API_KEY
  * CLICKUP_TASK_LIST_ID
  * CLICKUP_CUSTOM_DATE_FIELD_ID
   
# Getting ClickUp Team/List/Custom ID(s)

1. Generate a Personal Token to retrieve your custom IDs

   A. ClickUp Portal > Personal Settings > Apps > generate API Token

2. Retrieve Team ID:
```
curl -X GET -H "Authorization: YOUR_CLICKUP_PAT" "https://api.clickup.com/api/v2/team"
```

3. Retrieve List IDs for the Workspace:

```
curl -X GET -H "Authorization: YOUR_CLICKUP_PAT" "https://api.clickup.com/api/v2/team/{TEAM_ID}/list"
```

4. Retrieve Custom Field IDs associated w/ the List:

```
curl -X GET -H "Authorization: YOUR_CLICKUP_PAT" "https://api.clickup.com/api/v2/list/{LIST_ID}/field"
```

# Optional

1. Setup AWS Eventbridge Scheduler to run a daily (or time-based) cron job
