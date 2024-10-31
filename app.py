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
    camera_healthy = True  # Assume the camera is healthy initially ----------------------------change to True at production 
    messages = ["Test"]  # List to collect health messages

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
        if camera['uptime_sec'] < 3600:  # Example threshold for minimum uptime (1 hour)
            messages.append("Warning: Uptime is below the recommended threshold.")
            camera_healthy = False
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
    "campaign": '%7B%22data%22%3A%7B%22utm_source%22%3Anull%2C%22utm_medium%22%3Anull%2C%22utm_campaign%22%3Anull%2C%22utm_content%22%3Anull%2C%22utm_term%22%3Anull%2C%22referrer%22%3A%22https%3A%2F%2Fring.com%2F%22%2C%22path%22%3A%22%2Faccount%2Fdashboard%22%7D%7D',
    "next-i18next": "en-gb",
    "_shopify_s": "06c6f8f5-aa8e-48f3-b30d-2dff8a023b2b",
    "_shopify_y": "270eb1c3-40fc-44cb-b35a-f88694f25e76",
    "gn_mp": "US",
    "gn_v": "2",
    "userty.core.s.d30cd6": "__SI6MTcyOTkzOTEyMDU4Niwic2lkIjoiN2Q4YmZmOGI4MzMwZjMwNmI3NTZlN2YxMjUxOTE5MDciLCJzdCI6MTcyOTkzNjQxNzkwMiwicHYiOjE3LCJyZWFkeSI6dHJ1ZSwid3MiOiJ7XCJ3XCI6MTkyMCxcImhcIjo5Nzd9IiwiYXVyeWMuZmJ0LjEwNTUyIjoidCJ9eyJzZ",
    "_hp2_id.1155664863": '{"userId":"3649063783902093","pageviewId":"7187138162832867","sessionId":"8539551909480133","identity":null,"trackerVersion":"4.0"}',
    "_hp2_props.1155664863": '{"product_finding_method":"PLP","product_finding_method_pagename":"home-security-cameras","product_finding_method_detail":"Product Recs","utm_source_via_snapshot":null,"utm_medium_via_snapshot":null,"utm_campaign_via_snapshot":null,"utm_content_via_snapshot":null,"utm_term_via_snapshot":null,"referrer_via_snapshot":"","landing_path_via_snapshot":"/account/dashboard"}',
    "analytics_status": "opted-out",
    "cc-privacy-cookie": '{"analytics_heap":false,"analytics_optimizely":false}',
    "userty.core.p.d30cd6": "__2VySWQiOiI0NWRlMTQ1MDlkNDI3NTg1Mzg3NTM4YjFmOGViMjg4NCJ9eyJ1c",
    "optimizelyEndUserId": "oeu1726660636393r0.45507257271588675",
    "rs_an_loc_id": "2bce1860-42cb-401d-9211-20d9e77760ed",
    "cwr_u": "f5e7cd88-29f3-4886-af32-f0010bffcf96",
    "__stripe_mid": "135fc963-71eb-4e8b-94d0-eaeea018460cea5dab",
    "_a_id": "582248bc-cadf-49bd-b7a0-22ed49786032",
    "rsas": "87db3353-393b-44a1-bf64-34f7faa4b98f",
    "rCookie": "ghhm1b1mdg75kogy9qz625m2dlrh7y",
    "lastRskxRun": "1729187789037",
    "rskxRunCookie": "0",
    "rs_session": "2PnANnnIhuHnBO9rwp2Pn2jE0NzA0MDUyMAXtTg-xbu3E_Sx3bFEaqY1oH97FxtJ_o13vW0ePTSEsw",
    "theme-preference_147040520": "system",
    "theme-preference_147042711": "system",
    "rs_hwid": "5ce1e47a-aa39-4e40-a531-ee11d07a4c8f",
    "privacy-banner": "true",
    "privacy-banner-clicked": "true",
    "privacy-cookie": '{"version":12,"analytics_optimizely":true,"analytics_yext":true,"analytics_heap":true,"advertising_kenshoo":true,"advertising_amazonDisplay":true,"advertising_sizmek":true,"consentUrl":"https://ring.com/products/stick-up-cam","consentDate":"Wed, 18 Sep 2024 13:43:01 GMT","rw_mp":"US"}'
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
