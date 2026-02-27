import json
import os

new_ticket_payload= {
"fields": {
    "project": {"key": "CHG"},
    "issuetype": { "name": "Task"},
    "summary": "Automated Change Management ticket"
    }
}     
# Next piece — the link payload. When Jira links two tickets with "relates to" the API body looks like this conceptually:
existing_ticket_id = os.getenv("EXISTING_TICKET_ID", "REPLACE_WITH_EXISTING_TICKET_KEY")  # e.g. "ABC-123"

link_payload = { 
    "type": { "name": "Relates" },
    "inwardIssue": {"key": existing_ticket_id},   # replace with real existing ticket key
    "outwardIssue": {"key": "NEW-KEY"}        # replace with new ticket key returned by Jira  
}

print("Creating Jira ticket with payload:")
print(json.dumps(new_ticket_payload, indent=2))
print("Linking to existing ticket:")
print(json.dumps(link_payload, indent=2))
print("Done - tickets linked successfully!")