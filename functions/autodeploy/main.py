import functions_framework


@functions_framework.cloud_event
def main_cloud_event(cloud_event):
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")
