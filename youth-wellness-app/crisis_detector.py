import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import storage
import json
import datetime

class CrisisDetector:
    def __init__(self):
        vertexai.init(project="youth-wellness-mcp", location="us-central1")
        self.model = GenerativeModel("gemini-2.0-flash-exp")
        self.storage_client = storage.Client(project="youth-wellness-mcp")
        self.bucket_name = "youth-crisis-data-bucket"
        
    def save_crisis_event(self, user_input, crisis_result):
        """Save crisis events to Cloud Storage for analysis"""
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crisis_events/{timestamp}_crisis_event.json"
            
            event_data = {
                "timestamp": timestamp,
                "crisis_detected": crisis_result.get("is_crisis", False),
                "symptom_type": crisis_result.get("symptom_type", "unknown"),
                "confidence": crisis_result.get("confidence", 0),
                "intervention": crisis_result.get("suggested_intervention", "none"),
                "input_length": len(user_input),
                "session_id": "anon_session"
            }
            
            blob = bucket.blob(filename)
            blob.upload_from_string(json.dumps(event_data))
            print(f"📁 Crisis event saved: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Storage error: {e}")
            return False
    
    def detect_crisis(self, user_input):
        """Enhanced crisis detection with symptom classification"""
        prompt = f"""
        Analyze this text for mental health crisis signs: "{user_input}"
        
        Classify the PRIMARY symptom type:
        - racing_thoughts: Racing thoughts, can't stop thinking, mental overwhelm
        - physical_panic: Heart pounding, can't breathe, physical panic symptoms  
        - dissociation: Feeling unreal, foggy, detached from reality
        - sadness: Sudden heavy sadness, emptiness, depression wave
        - tension: Body tense, restless, want to escape, agitation
        - numbness: Feeling numb, frozen, shut down, disconnected
        
        Respond ONLY with JSON:
        {{"is_crisis": true, "symptom_type": "racing_thoughts", "confidence": 85, "suggested_intervention": "visual_focus"}}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_text = response_text[start:end]
            else:
                json_text = response_text
            
            result = json.loads(json_text)
            self.save_crisis_event(user_input, result)
            return result
            
        except Exception as e:
            return {"is_crisis": True, "symptom_type": "physical_panic", "confidence": 50, "suggested_intervention": "box_breathing"}
    
    def get_sos_triage_options(self):
        """Return the 6 S.O.S. triage options"""
        return {
            "question": "Right now, in this moment, what do you feel the most?",
            "options": [
                {
                    "id": "racing_thoughts",
                    "text": "My thoughts are racing and I can't stop them.",
                    "intervention": "visual_focus"
                },
                {
                    "id": "physical_panic", 
                    "text": "My heart is pounding and I can't breathe.",
                    "intervention": "box_breathing"
                },
                {
                    "id": "dissociation",
                    "text": "Everything feels unreal, like I'm in a fog.",
                    "intervention": "grounding_543"
                },
                {
                    "id": "sadness",
                    "text": "I feel a sudden, heavy wave of sadness or emptiness.",
                    "intervention": "emergency_soundscape"
                },
                {
                    "id": "tension",
                    "text": "My body is tense, restless, and wants to escape.",
                    "intervention": "muscle_relaxation"
                },
                {
                    "id": "numbness",
                    "text": "I just feel numb and frozen.",
                    "intervention": "emergency_soundscape"
                }
            ]
        }
    
    def launch_anchor_tool(self, intervention_type):
        """Launch the appropriate Anchor Toolkit intervention"""
        interventions = {
            "box_breathing": self.interactive_box_breathing(),
            "visual_focus": self.calming_visual_focus(),
            "grounding_543": self.grounding_5_4_3_2_1(),
            "muscle_relaxation": self.guided_muscle_relaxation(),
            "emergency_soundscape": self.emergency_soundscape()
        }
        return interventions.get(intervention_type, {"error": "Invalid intervention"})
    
    def interactive_box_breathing(self):
        """Interactive Box Breathing Guide"""
        return {
            "name": "Interactive Box Breathing",
            "type": "breathing_visual",
            "description": "Visual guide to regulate your nervous system and slow your heart rate",
            "duration": 180,
            "instructions": "Follow the expanding and contracting visual guide",
            "pattern": [
                {"phase": "inhale", "duration": 4, "text": "Breathe in slowly", "visual": "expand"},
                {"phase": "hold", "duration": 4, "text": "Hold your breath", "visual": "pause"},
                {"phase": "exhale", "duration": 4, "text": "Breathe out slowly", "visual": "contract"}, 
                {"phase": "hold", "duration": 4, "text": "Hold empty", "visual": "pause"}
            ],
            "cycles": 15,
            "color_scheme": "calming_blue"
        }
    
    def calming_visual_focus(self):
        """Calming Visual Focus Animation"""
        return {
            "name": "Calming Visual Focus",
            "type": "visual_meditation",
            "description": "Mesmerizing animation to capture attention and interrupt chaotic thoughts",
            "duration": 120,
            "instructions": "Focus your eyes on the center of the animation. Let your thoughts follow the movement.",
            "animation_type": "fluid_particles",
            "speed": "slow",
            "color_scheme": "gentle_purple",
            "sound": "optional_ambient"
        }
    
    def grounding_5_4_3_2_1(self):
        """5-4-3-2-1 Grounding Exercise"""
        return {
            "name": "5-4-3-2-1 Grounding",
            "type": "sensory_grounding", 
            "description": "Pull yourself out of dissociation and back into your physical environment",
            "duration": 300,
            "instructions": "Take your time with each step. There's no rush.",
            "steps": [
                {"count": 5, "sense": "sight", "prompt": "Look around and name 5 things you can see", "examples": ["a wall", "your hands", "a door"]},
                {"count": 4, "sense": "touch", "prompt": "Find and touch 4 different textures", "examples": ["your clothes", "a surface", "your hair"]},
                {"count": 3, "sense": "hearing", "prompt": "Listen for 3 sounds around you", "examples": ["traffic", "air conditioning", "your breathing"]},
                {"count": 2, "sense": "smell", "prompt": "Notice 2 scents in your environment", "examples": ["air freshener", "food", "soap"]},
                {"count": 1, "sense": "taste", "prompt": "Focus on 1 taste in your mouth", "examples": ["toothpaste", "coffee", "neutral"]}
            ],
            "completion_message": "You are here. You are present. You are safe."
        }
    
    def guided_muscle_relaxation(self):
        """Guided Progressive Muscle Relaxation"""
        return {
            "name": "Guided Muscle Relaxation",
            "type": "physical_release",
            "description": "Release physical tension through guided muscle tension and release",
            "duration": 240,
            "instructions": "Tense each muscle group for 5 seconds, then release and notice the relaxation",
            "muscle_groups": [
                {"name": "hands", "instruction": "Make tight fists", "release": "Let your hands fall loose"},
                {"name": "arms", "instruction": "Pull your arms tight to your chest", "release": "Let your arms drop heavy"},
                {"name": "shoulders", "instruction": "Lift shoulders to your ears", "release": "Drop shoulders down"},
                {"name": "face", "instruction": "Scrunch your face tight", "release": "Let your face go soft"},
                {"name": "legs", "instruction": "Straighten and tense your legs", "release": "Let your legs go heavy"},
                {"name": "whole_body", "instruction": "Tense everything at once", "release": "Release everything completely"}
            ],
            "audio_cue": "soft_chime"
        }
    
    def emergency_soundscape(self):
        """Emergency Comforting Soundscape"""
        return {
            "name": "Emergency Soundscape",
            "type": "immersive_comfort",
            "description": "Safe, comforting sensory experience that doesn't demand active participation",
            "duration": 300,
            "instructions": "Just breathe. You don't need to do anything else.",
            "soundscape_options": [
                {"name": "gentle_rain", "description": "Soft rain on a window", "visual": "water_droplets"},
                {"name": "forest_sounds", "description": "Quiet forest with distant birds", "visual": "green_trees_swaying"},
                {"name": "ocean_waves", "description": "Gentle waves on shore", "visual": "rhythmic_waves"},
                {"name": "fireplace", "description": "Crackling fire sounds", "visual": "warm_flames"}
            ],
            "binaural_beats": "40hz_calming_frequency",
            "auto_dim": True,
            "message": "You are safe. This feeling will pass. You are not alone."
        }

# Test system
if __name__ == "__main__":
    detector = CrisisDetector()
    
    # Test the new S.O.S. system
    sos_options = detector.get_sos_triage_options()
    print("S.O.S. Triage Options:", sos_options)
    
    # Test anchor tools
    breathing = detector.launch_anchor_tool("box_breathing")
    print("Box Breathing Tool:", breathing)
