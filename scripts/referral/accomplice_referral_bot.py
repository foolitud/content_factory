import json
import base64
import time

class ParallelGrowthEngine:
    """
    Simulation of the Parallel Adventure Growth Engine.
    Handles recruitment logic and referral tracking.
    """
    
    def __init__(self):
        self.players = {
            "agent_001": {"name": "Lolo", "referrals": 0, "status": "Active"},
        }
        self.accomplices = {}
        self.mission_data = {
            "clean_phone": {
                "npc": "The Liaison",
                "briefing": "I need a fresh contact. Send a recruitment link to someone you trust."
            }
        }

    def generate_recruitment_link(self, player_id, mission_id):
        """Generates a base64 encoded token for the recruitment URL."""
        if player_id not in self.players:
            return "Error: Player not found."
            
        payload = f"{player_id}|{mission_id}|{int(time.time())}"
        token = base64.b64encode(payload.encode()).decode()
        return f"https://parallel.adventure/recruit/{token}"

    def handle_webhook_onboarding(self, token, friend_name, friend_phone):
        """Simulates a webhook from the landing page when a friend joins."""
        try:
            decoded = base64.b64decode(token).decode()
            player_id, mission_id, timestamp = decoded.split('|')
        except Exception:
            return {"status": "error", "message": "Invalid recruitment token."}

        # 1. Register the Accomplice
        accomplice_id = f"acc_{int(time.time())}"
        self.accomplices[accomplice_id] = {
            "name": friend_name,
            "phone": friend_phone,
            "referred_by": player_id,
            "mission": mission_id
        }

        # 2. Reward the Player
        self.players[player_id]["referrals"] += 1
        
        return {
            "status": "success",
            "accomplice_id": accomplice_id,
            "player_notified": True,
            "npc_message": f"Welcome, Accomplice {friend_name}. Agent {self.players[player_id]['name']} said you were the best for the job."
        }

# Example Usage
if __name__ == "__main__":
    engine = ParallelGrowthEngine()
    
    # 1. Player Lolo wants to recruit a friend for 'clean_phone' mission
    link = engine.generate_recruitment_link("agent_001", "clean_phone")
    print(f"--- MISSION START ---\nNPC to Player: {engine.mission_data['clean_phone']['briefing']}")
    print(f"Generated Recruitment Link: {link}\n")
    
    # 2. Friend 'Alice' clicks the link and signs up
    token = link.split('/')[-1]
    result = engine.handle_webhook_onboarding(token, "Alice", "+33600000000")
    
    print(f"--- WEBHOOK RECEIVED ---\nFriend joined: {result['status']}")
    print(f"NPC to Accomplice: {result['npc_message']}")
    print(f"Player Stats: {engine.players['agent_001']}")
