from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("URL")
key = os.getenv("KEY")


supabase = create_client(url,key)
