def run_wizard():
    print("Welcome to Media Harvester Wizard!")
    url = input("Enter a URL (or leave empty to use a file): ")
    if not url:
        file_path = input("Enter the path to the file with URLs: ")
    else:
        file_path = None

    root = input("Enter a root URL for recursive parsing (or leave empty): ")
    formats = input("Enter file formats to download (e.g., jpg,png): ").split(",")
    output = input("Enter output folder (default: output/): ") or "output/"

    print("Starting parsing with the provided inputs...")
    
    #Call the parser with wizard inputs
    from main.parser.parser import parse_urls
    parse_urls(url, file_path, root, formats, output)
