from db_layer import fetch_fields, fetch_logs, fetch_data

workflow_id = 1  # Test for workflow_1

# 1. Show field names
print("🔑 Fields:")
print(fetch_fields(workflow_id))

# 2. Show logs
print("\n📜 Logs:")
for log in fetch_logs(workflow_id):
    print(log)

# 3. Show full data
print("\n📦 Full Data:")
for item in fetch_data(workflow_id):
    print(item)

# 4. Optional: filtered data
print("\n🔥 Filtered Data (lead_type='hot'):")
filters = {"lead_type": "hot"}
for item in fetch_data(workflow_id, filters):
    print(item)
