# sympa-auditor

Sympa-auditor automate the extraction of metadata from a Sympa-based mailing list web interface. It performs web scraping to collect details about available mailing lists—such as list names along with their configurations and compiles them into a structured JSON file. The web browser used to web scrape is Chrome. Should only be run by listmasters. 

## Features

- Automatically navigates and parses Sympa list index pages
- Extracts metadata for each mailing list
- Outputs a single, clean JSON file for further processing or analysis
- Designed for administrators needing an overview of Sympa lists

## Usage 

#### Retrieve the sympa-session token
Navigate to https://list.ncsa.illinois.edu and sign in using ```Campus Login```. The Developer Window should be open and on the Network tab. Find the request with the ```lists``` name, and record the ```sympa_session``` cookie. 

#### Docker Compose
It is best to run the sympa-auditor using docker compose with two services: sympa-auditor and selenium. Sympa-auditor relies on selenium to do the web-scraping work. See the `docker-compose.yml` file for a template. Make sure to include the sympa_session cookie.

#### Flags 
```--option```: This flag is required. There are 3 options: ```list```, ```categorize```, ```match```. The ```list``` option outputs each mailing list entries along with their configurations. The ```categorize``` option lists the different configurations and index each mailing list into their respective configuration. The ```match``` outputs the mailing list entries that don't match to any use cases. If the ```match``` option is used, the USE_CASE_PATH must also be specified and mounted onto the container in the docker-compose.yml file (see docker-compose.yml for example)

```--console```: Prints the output to console. If not used, the output is saved to OUTPUT_FILE. 

#### Command
```
python3 audit.json --sympa-session <TOKEN> --option list              # Output is saved to OUTPUT_FILE
python3 audit.json --sympa-session <TOKEN> --option list --console    # Dumps output to console. Default is save output to ENV_FILE
python3 audit.json --sympa-session <TOKEN> --option categorize        # Output is saved to OUTPUT_FILE
python3 audit.json --sympa-session <TOKEN> --option match             # Output is saved to OUTPUT_FILE. The USE_CASE_PATH environment variable must be specified. If not, an error will be thrown.
```

#### Output
The output is a file (OUTPUT_FILE). The user can either mount a docker volume (as shown in the docker-compose.yml file), or do a bind mount to save the file. If the `--console` flag is included, the output is dumped to the console, rather than OUTPUT_FILE. 

#### Environment Variables 
1. MAILING_LIST_URL='https://lists.ncsa.illinois.edu'
2. ENV OUTPUT_FILE='audit.json' 
- Contains mailing list entries and their configurations
3. ENV USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
4. ENV USE_CASE_PATH=''
- Specifies where the configuration file that specifies the different use cases are located. Must be specified if you specify the ```match``` option. See `use_cases.json` for an example of the format. All fields must be specified. If not, there may be unexpected behavior.

These variables can be overwritten in the sympa-auditor section in the docker-compose.yml file. 
