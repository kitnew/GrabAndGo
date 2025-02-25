#import argparse
#from wizard import run_wizard
#from parser import parse_urls

#def main():
#    parser = argparse.ArgumentParser(description="Media Harvester - Parse and download media from websites.")
#    parser.add_argument("--url", help="Single URL to parse.")
#    parser.add_argument("--file", help="File containing list of URLs.")
#    parser.add_argument("--root", help="Root URL for recursive parsing.")
#    parser.add_argument("--output", help="Output folder for saved files.", default="output/")
#    parser.add_argument("--formats", help="Comma-separated list of formats to download (e.g., jpg,png,mp4).")
#    args = parser.parse_args()
#    if not any([args.url, args.file, args.root]):
#        print("No arguments provided. Starting wizard mode...")
#        run_wizard()
#    else:
#    print("Starting CLI mode...")
#    
#    #Pass arguments to the parser
#    parse_urls(args.url, args.file, args.root, args.formats, args.output)

#if __name__ == "__main__":
#    main()

#from parser import parse_coomer_post
#
#def main():
#    url = "https://coomer.su/onlyfans/user/segodnyai/post/1169858566"  # Пример URL для теста
#    print(f"Parsing URL: {url}")
#    
#    result = parse_coomer_post(url)
#    print("Parsed media links:")
#    print(f"Images: {result['images']}")
#    print(f"Videos: {result['videos']}")
#    print(f"Folder name: {result['folder_name']}")
#
#if __name__ == "__main__":
#    main()
from parser.parser import parse_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    url = "https://coomer.su/onlyfans/user/segodnyai"  # Пример ссылки на папку
    media = parse_url(url, False)
    print(media)

if __name__ == "__main__":
    main()