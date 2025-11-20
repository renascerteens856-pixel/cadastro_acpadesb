from supabase import create_client

url = "https://nhfpldkvqrvgyddbpbnw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oZnBsZGt2cXJ2Z3lkZGJwYm53Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIyNTk4MDMsImV4cCI6MjA3NzgzNTgwM30.0weuBxaHTPXhdn6BWjZSAxmG7LpcfVQsJGFTC0KdaAs"
# Conexão com o banco de dados
def connect_db():
    supabase = create_client(url, key)
    return supabase