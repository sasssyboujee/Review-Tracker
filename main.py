import asyncio
import aiosqlite
# pyrefly: ignore [missing-import]
from google.antigravity import Agent, LocalAgentConfig

DB_FILE = "leads.db"

# 1. Asynchronous Database Initialization with WAL Mode enabled
async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                query TEXT PRIMARY KEY,
                status TEXT
            )
        ''')
        await db.commit()

async def get_lead_status(query: str) -> str:
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT status FROM leads WHERE query = ?', (query,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "NEW"

async def update_lead_status(query: str, status: str):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('INSERT OR REPLACE INTO leads (query, status) VALUES (?, ?)', (query, status))
        await db.commit()

# 2. Sequential Lead Processing Loop
async def process_lead(query: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        status = await get_lead_status(query)
        if status == "OUTREACHED":
            print(f"[{query}] Already fully processed.")
            return

        print(f"[{query}] Starting pipeline. Current status: {status}")
        
        # Configure the Antigravity Agent Session natively
        config = LocalAgentConfig()
        
        async with Agent(config) as agent:
            if status == "NEW":
                print(f"[{query}] Dispatching Prospector Skill...")
                # Instruct the agent to locate the custom tool module within your workspace folder
                response = await agent.chat(
                    f"Load your maps_scraper tool in mock_mode=True. Find reviews for '{query}' and save the output text."
                )
                print(f"[{query}] Prospector output: {await response.text()}")
                await update_lead_status(query, "PROSPECTED")
                status = "PROSPECTED"
                
            if status == "PROSPECTED":
                print(f"[{query}] Dispatching Analyst Skill...")
                response = await agent.chat(
                    "Analyze the reviews saved from the previous step. Isolate exactly 3 high-probability fake reviews."
                )
                print(f"[{query}] Analyst output: {await response.text()}")
                await update_lead_status(query, "ANALYZED")
                status = "ANALYZED"
                
            if status == "ANALYZED":
                print(f"[{query}] Dispatching Enrichment Skill...")
                response = await agent.chat(
                    "Load your contact_enricher tool in mock_mode=True. Find the owner email address for this business domain."
                )
                print(f"[{query}] Enrichment output: {await response.text()}")
                await update_lead_status(query, "ENRICHED")
                status = "ENRICHED"
                
            if status == "ENRICHED":
                print(f"[{query}] Dispatching Outreach Skill...")
                response = await agent.chat(
                    "Load your email_sender tool in mock_mode=True. Draft and send the cold email using the 3 reviews as evidence."
                )
                print(f"[{query}] Outreach output: {await response.text()}")
                await update_lead_status(query, "OUTREACHED")
                status = "OUTREACHED"

        print(f"[{query}] Processing complete.")

async def main():
    await init_db()
    
    leads = [
        "Singapore + Plumber",
        "Singapore + Electrician",
        "Singapore + Locksmith",
        "Singapore + Aircon Servicing"
    ]
    
    # Enforce concurrency threshold
    semaphore = asyncio.Semaphore(3)
    
    tasks = [process_lead(lead, semaphore) for lead in leads]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
