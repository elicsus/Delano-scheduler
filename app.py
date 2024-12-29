import requests
from bs4 import BeautifulSoup
import json
import os


def fetch_camera_data(url, cookies):
    """Fetch the camera data from a webpage by extracting JSON data from a specific script tag."""
    try:
        # Fetch the HTML content of the page
        response = requests.get(url, cookies=cookies, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the specific script tag containing the JSON data
        script_tag = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})

        # Check if the script tag was found
        if script_tag and script_tag.string:
            # Load the JSON data from the script content
            camera_data = json.loads(script_tag.string)
            return camera_data
        else:
            print("Camera data not found in the HTML.")
            return None

    except requests.RequestException as e:
        print(f"An error occurred while fetching camera data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        return None

def load_camera_data_from_file(file_path):
    try:
        # Open and read the JSON file
        with open(file_path, 'r') as file:
            print ("break point 1")
            css_data = file.read()
            print ("break point 2")
        return css_data

    except (FileNotFoundError) as e:
        print(f"An error occurred while loading camera data from file: {e}")
        return None

def check_camera_health(camera):
    camera_healthy = False  # Assume the camera is healthy initially ----------------------------change to True for production 
    messages = []  # List to collect health messages

    if camera['connected']:
        # RSSI Health Check
        if camera['rssi'] < -70:  # Example threshold for RSSI
            messages.append("Warning: RSSI is low. Consider improving signal strength.")
            camera_healthy = False

        # Bandwidth Health Check
        if camera['bandwidth'] < 1000:  # Example threshold for bandwidth (1 Mbps)
            messages.append("Warning: Bandwidth is low. Streaming quality may be affected.")
            camera_healthy = False

        # Stream Resolution Health Check
        #if camera['stream_resolution'] < 720:  # Minimum recommended resolution
        #    messages.append("Warning: Stream resolution " + str(camera['stream_resolution']) + " is below the recommended level.")
        #    camera_healthy = False

        # Battery Error Check
        if camera['battery_error']:
            messages.append("Warning: Battery error detected.")
            camera_healthy = False

        # Uptime Check
        #if camera['uptime_sec'] < 3600:  # Example threshold for minimum uptime (1 hour)
        #    messages.append("Warning: Uptime is below the recommended threshold.")
        #    camera_healthy = False
    else:
        messages.append("Status: Not connected.")
        camera_healthy = False
    
    # Print overall health status and messages if not healthy
    if not camera_healthy:
        print("Camera Health Report:")
        print(f"Camera Healthy: {'No'}")
        for message in messages:
            print(f"- {message}")
    else:
        print("Camera Healthy: Yes")

    return messages
#-------------------------------------------------------------------------------------USE SECRETS !!!!!!
def send_telegram_message(message):
    bot_token = "7741198322:AAFEUJ84tSBimWKcaLV8UdRG3xyjFnCPCLw"
    chat_ids = ["6333434597", "142181097"]  # Add more chat IDs as needed 
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    
    full_message = "\n".join(message) 
    payload = {'text': full_message}

    for chat_id in chat_ids:
        payload['chat_id'] = chat_id
        requests.post(url, data=payload)

# Test with a sample URL and cookies
url = "https://account.ring.com/account/dashboard?l=2bce1860-42cb-401d-9211-20d9e77760ed&lv_d=554788975"

   
cookies = {
    'campaign': '%7B%22data%22%3A%7B%22utm_source%22%3Anull%2C%22utm_medium%22%3Anull%2C%22utm_campaign%22%3Anull%2C%22utm_content%22%3Anull%2C%22utm_term%22%3Anull%2C%22referrer%22%3A%22https%3A%2F%2Fring.com%2F%22%2C%22path%22%3A%22%2Faccount%2Fdashboard%22%7D%7D',
    'next-i18next': 'en-gb',
    '_shopify_s': '5c9e298b-4524-449a-92d8-e631544d6d75',
    '_shopify_y': 'ef6f1ab6-4324-491e-a581-80e7839d8ec4',
    'rs_an_loc_id': '2bce1860-42cb-401d-9211-20d9e77760ed',
    'cc-privacy-cookie': '%7B%22analytics_heap%22%3A%22false%22%2C%22analytics_optimizely%22%3A%22false%22%7D',
    'rs_session': '2XvvVcxMSKjuqdyrpZerTFjE0NzA0MDUyMAZHJf6etpUF9NEqcciEasGYWV08fmMEg-ngUo9XBNbg0',
    'userty.core.s.d30cd6': '__SI6MTczNTQ3NDE3MTE5Miwic2lkIjoiNzE4N2QxNDNkZWVhY2U3NjBhMWI5MTM1YzFmYTI1YTciLCJzdCI6MTczNTQ3MTI1ODYyMSwicHYiOjQsInJlYWR5Ijp0cnVlLCJ3cyI6IntcIndcIjoxNDQwLFwiaFwiOjc5N30ifQ==eyJzZ',
    '_hp2_id.1155664863': '%7B%22userId%22%3A%223146994307127478%22%2C%22pageviewId%22%3A%224716282867253367%22%2C%22sessionId%22%3A%221094559028117651%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D',
    '_hp2_props.1155664863': '%7B%22utm_source_via_snapshot%22%3Anull%2C%22utm_medium_via_snapshot%22%3Anull%2C%22utm_campaign_via_snapshot%22%3Anull%2C%22utm_content_via_snapshot%22%3Anull%2C%22utm_term_via_snapshot%22%3Anull%2C%22referrer_via_snapshot%22%3A%22%22%2C%22landing_path_via_snapshot%22%3A%22%2F%22%7D',
    'userty.core.p.d30cd6': '__2VySWQiOiI0ODYxMGYxNDJiZGY3MjE1N2IxMTk4Nzg2ZjI5MTk5MSJ9eyJ1c',
    'optimizelyEndUserId': 'oeu1735070327196r0.5091819696980051',
    'geo': 'IL',
    '_a_id': '8e659d0d-a406-4495-bf7d-2cd84e17b882',
    'cwr_u': 'f5e7cd88-29f3-4886-af32-f0010bffcf96',
    '__stripe_mid': '135fc963-71eb-4e8b-94d0-eaeea018460cea5dab',
    'rsas': 'c3205203-1424-49e7-b636-f4bdba15ad6c',
    'rCookie': 'ghhm1b1mdg75kogy9qz625m2dlrh7y',
    'lastRskxRun': '1729187789037',
    'rskxRunCookie': '0',
    'theme-preference_147040520': 'system',
    'theme-preference_147042711': 'system',
    'rs_geo': 'IL',
    'rs_hwid': '97530a57-d0d3-400b-93f6-8b2a77a32f93',
    'privacy-banner': 'true',
    'privacy-banner-clicked': 'true',
    'privacy-cookie': '%7B%22version%22%3A12%2C%22analytics_optimizely%22%3Atrue%2C%22analytics_yext%22%3Atrue%2C%22analytics_heap%22%3Atrue%2C%22advertising_kenshoo%22%3Atrue%2C%22advertising_amazonDisplay%22%3Atrue%2C%22advertising_sizmek%22%3Atrue%2C%22consentUrl%22%3A%22https%3A%2F%2Fring.com%2F%22%2C%22consentDate%22%3A%22Sun%2C%2029%20Dec%202024%2011%3A20%3A54%20GMT%22%2C%22rw_mp%22%3A%22US%22%7D'
}

# Fetch camera data
camera_data = fetch_camera_data(url, cookies)

# Access the cameras list
data_health = camera_data["props"]["userDevices"]["stickup_cams"][0]["health"]

if __name__ == "__main__":
    #Check Camera health
    message = check_camera_health(data_health)
    if bool(message):
        send_telegram_message(message)
