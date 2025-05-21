# sympa-auditor

These Python scripts automate the extraction of metadata from a Sympa-based mailing list web interface. It performs web scraping to collect details about available mailing lists—such as list names along with their configurations and compiles them into a structured JSON file. The web browser used to web scrape is Chrome. Should only be run by listmasters. 

## Features

- Automatically navigates and parses Sympa list index pages
- Extracts metadata for each mailing list
- Outputs a single, clean JSON file for further processing or analysis
- Designed for administrators needing an overview of Sympa lists

## Usage 

#### Retrieve the sympa-session token
Navigate to https://list.ncsa.illinois.edu and sign in using ```Campus Login```. The Developer Window should be open and on the Network tab. Find the request with ```lists``` name, and record the ```sympa_session``` cookie. 

#### Docker Compose
It is best to run the sympa-auditor using docker compose with two services: sympa-auditor and selenium. Sympa-auditor relies on selenium to do the web-scraping work. See the `docker-compose.yml` file for a template. Make sure to include the sympa_session cookie.

#### Command
```
python3 audit.json --sympa-session <TOKEN>               # Data is saved to ENV_FILE
python3 audit.json --sympa-session <TOKEN> --output      # Dumps output to console. Default is save output to ENV_FILE
python3 audit.json --sympa-session <TOKEN> --categorize  # Two files are created: OUTPUT_FILE and CATEGORIZE_FILE

```

#### Output
The output is a file (OUTPUT_FILE). The user can either mount a docker volume (as shown in the docker-compose.yml file), or do a bind mount to save the file. If the `--output` flag is included, the output is dumped to the console, rather than OUTPUT_FILE. If the `--categorize` flag is included, then the CATEGORIZE_FILE is created where each configuration and their selections are categorized and each mailing list are indexed to their respective configurations.

#### Environment Variables 
1. MAILING_LIST_URL='https://lists.ncsa.illinois.edu'
2. ENV OUTPUT_FILE='audit.json' 
- Contains mailing list entries and their configurations
2. ENV CATEGORIZE_FILE='categorize_audit.json' 
- Categorize mailing lists by their configurations. 
3. ENV USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'

These variables can be overwritten in the sympa-auditor section in the docker-compose.yml file. 
