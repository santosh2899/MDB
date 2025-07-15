# chatbot.py

def generate_chatbot_response(logs, question):
    question = question.lower()

    if "status" in question:
        status_count = {}
        for log in logs:
            status = log.get("status", "unknown")
            status_count[status] = status_count.get(status, 0) + 1
        return f"Status breakdown: {status_count}"

    elif "response time" in question:
        times = [int(log["response_time"].replace("s", "")) for log in logs if "response_time" in log]
        avg_time = sum(times) / len(times) if times else 0
        return f"Average response time is {avg_time:.2f} seconds"

    else:
        return "I can help with questions about status or response time."
