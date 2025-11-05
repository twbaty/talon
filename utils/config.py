from dotenv import load_dotenv
import os


def init_env():
load_dotenv()
return {
"ABUSEIPDB_API_KEY": os.getenv("ABUSEIPDB_API_KEY"),
"SHODAN_API_KEY": os.getenv("SHODAN_API_KEY"),
"CENSYS_API_ID": os.getenv("CENSYS_API_ID"),
"CENSYS_API_SECRET": os.getenv("CENSYS_API_SECRET"),
"VIRUSTOTAL_API_KEY": os.getenv("VIRUSTOTAL_API_KEY"),
}
