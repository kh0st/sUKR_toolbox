import shodan
import os

def search_shodan(api_key):
    # Initialize the Shodan API client
    api = shodan.Shodan(api_key)

    # Step 1: Prompt the user to enter the city
    city = input("Enter the city to search devices in: ")

    # Step 2: Prompt the user for the type of search
    print("Choose the type of search:")
    print("1. Camera")
    print("2. OS")
    print("3. Port")
    print("4. Service")
    search_type = input("Enter the number for the search type (1-4): ")

    # Step 3: Based on the type of search, ask for further details
    query_parts = [f'city:"{city}"']

    if search_type == '1':
        banner = input("Enter camera type (e.g., Dahua, Hikvision) or press Enter for all cameras: ")
        if banner:
            query_parts.append(f'"{banner}"')
        else:
            query_parts.append('(WebcamXP OR Dahua OR Hikvision)')
    elif search_type == '2':
        os_name = input("Enter the operating system to search for (e.g., Windows, Linux): ")
        if os_name:
            query_parts.append(f'os:"{os_name}"')
    elif search_type == '3':
        port = input("Enter the port number to search (e.g., 80, 443, 554): ")
        if port:
            query_parts.append(f'port:{port}')
    elif search_type == '4':
        service = input("Enter the service to search for (e.g., ssh, http): ")
        if service:
            query_parts.append(f'"{service}"')

    # Step 4: Construct the final query
    query = " ".join(query_parts)

    # Step 5: Perform the Shodan search
    try:
        results = api.search(query)
        print(f"Found {results['total']} devices in {city} matching the criteria.")
        for result in results['matches']:
            print(f"IP: {result['ip_str']} | Port: {result.get('port', 'N/A')} | Org: {result.get('org', 'N/A')} | Product: {result.get('product', 'N/A')} | Info: {result.get('info', 'N/A')}")
    except shodan.APIError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Get the Shodan API key from the environment variable $SHODAN
    api_key = os.getenv('SHODAN')
    if api_key:
        search_shodan(api_key)
    else:
        print("Error: Shodan API key not found in environment variable $SHODAN.")
