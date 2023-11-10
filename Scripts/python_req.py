import argparse
import requests

def main(url):
    robot_url = f'{url}/robots.txt'
    response = requests.get(robot_url)
    print(response.text) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and print the contents of a URL's robots.txt file.")
    parser.add_argument("-u", "--url", required=True, help="The URL for which you want to fetch the robots.txt file.")
    
    parser.epilog = "Example: python your_script.py -u https://example.com"

    args = parser.parse_args()
    main(args.url)


