# sympa-auditor

These Python scripts automate the extraction of metadata from a Sympa-based mailing list web interface. It performs web scraping to collect details about available mailing lists—such as list names along with their configurations and compiles them into a structured JSON file.

## Features

- Automatically navigates and parses Sympa list index pages
- Extracts metadata for each mailing list
- Outputs a single, clean JSON file for further processing or analysis
- Designed for administrators needing an overview of Sympa lists

## Usage 
Install the depedencies: 
```
pip install -r requirements.txt
```

Run the script:
```
python3 audit.py
```

The first time you run the script, it opens the Sympa Web UI homepage, where you'll log in manually. Your session cookies are then saved for reuse in future runs. If there are errors with session cookies, simply delete ```cookies.pkl``` and rerun the script. 


