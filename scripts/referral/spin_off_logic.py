class ParallelSpinOffEngine:
    """
    Simulation of the Parallel Adventure Spin-off Engine.
    Handles the transition from Player to Creator.
    """
    
    def __init__(self):
        self.builder_base_url = "https://builder.parallel.adventure"
        self.completed_missions = {
            "mission_paris_heist": {
                "title": "Le Casse de Paris",
                "genre": "Braquage",
                "difficulty": "Medium"
            }
        }

    def generate_builder_cta(self, mission_id):
        """Generates a contextual CTA for the player."""
        if mission_id not in self.completed_missions:
            return "Mission not found."
            
        mission = self.completed_missions[mission_id]
        
        # Narrative-driven CTA
        cta_text = f"Félicitations Agent. {mission['title']} est un succès. Mais l'histoire ne s'arrête pas là..."
        cta_subtext = f"Tu as vécu l'aventure, maintenant écris la suite. Utilise {mission['title']}' comme base dans le Builder."
        
        # Deep link to pre-load templates
        builder_link = f"{self.builder_base_url}/new?template={mission_id}&ref=player_conversion"
        
        return {
            "cta": cta_text,
            "subtext": cta_subtext,
            "link": builder_link
        }

# Example Usage
if __name__ == "__main__":
    spinoff = ParallelSpinOffEngine()
    
    # Player just finished 'mission_paris_heist'
    conversion = spinoff.generate_builder_cta("mission_paris_heist")
    
    print("--- MISSION COMPLETE ---")
    print(f"NPC: {conversion['cta']}")
    print(f"Action: {conversion['subtext']}")
    print(f"Builder Link: {conversion['link']}")
