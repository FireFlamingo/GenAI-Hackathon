from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import json
import asyncio
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youth-portal")

app = FastAPI()

class YouthPortalMCPClient:
    """Youth Portal that connects to the MCP server via subprocess"""
    
    def __init__(self):
        self.mcp_process = None
        
    async def call_mcp_tool(self, tool_name: str, arguments: dict = None):
        """Call MCP tool via subprocess communication"""
        try:
            if arguments is None:
                arguments = {}
            
            # Prepare MCP request
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            # For now, simulate MCP responses based on tool name
            # In production, this would communicate with the actual MCP server
            mock_responses = {
# =============================================================================
# FEATURE 1: CRISIS INTERVENTION TOOLS (S.O.S. System)
# =============================================================================

                "crisis_detection": {
                    "mcp_tool": "crisis_detection",
                    "analysis": {
                        "is_crisis": True,
                        "symptom_type": "physical_panic",
                        "confidence": 85,
                        "suggested_tool": "box_breathing"
                    },
                    "timestamp": "2024-09-18T01:55:00"
                },
                "sos_triage": {
                    "mcp_tool": "sos_triage",
                    "question": "Right now, in this moment, what do you feel the most?",
                    "options": [
                        {"id": "racing_thoughts", "text": "💭 My thoughts are racing and I can't stop them.", "recommended_tool": "visual_focus"},
                        {"id": "physical_panic", "text": "💓 My heart is pounding and I can't breathe.", "recommended_tool": "box_breathing"},
                        {"id": "dissociation", "text": "🌫️ Everything feels unreal, like I'm in a fog.", "recommended_tool": "grounding_543"},
                        {"id": "sadness", "text": "😔 I feel a sudden, heavy wave of sadness or emptiness.", "recommended_tool": "emergency_soundscape"},
                        {"id": "tension", "text": "⚡ My body is tense, restless, and wants to escape.", "recommended_tool": "muscle_relaxation"},
                        {"id": "numbness", "text": "🧊 I just feel numb and frozen.", "recommended_tool": "emergency_soundscape"}
                    ]
                },
                "box_breathing": {
                    "mcp_tool": "box_breathing",
                    "intervention": {
                        "name": "Interactive Box Breathing",
                        "type": "breathing_visual",
                        "description": "Visual guide to regulate nervous system and reduce heart rate",
                        "duration_seconds": 120,
                        "total_cycles": 7,
                        "breathing_pattern": [
                            {"phase": "inhale", "duration": 4, "instruction": "Breathe in slowly", "visual_cue": "expand"},
                            {"phase": "hold_in", "duration": 4, "instruction": "Hold your breath", "visual_cue": "pause_expanded"},
                            {"phase": "exhale", "duration": 4, "instruction": "Breathe out slowly", "visual_cue": "contract"},
                            {"phase": "hold_out", "duration": 4, "instruction": "Hold empty", "visual_cue": "pause_contracted"}
                        ]
                    }
                },
                "visual_focus": {
                    "mcp_tool": "visual_focus",
                    "intervention": {
                        "name": "Calming Visual Focus",
                        "type": "visual_meditation",
                        "description": "Mesmerizing animation to interrupt racing thoughts",
                        "duration_seconds": 120,
                        "animation": {
                            "type": "spiral_particles",
                            "speed": "slow",
                            "color_scheme": "calming_gradient"
                        },
                        "instructions": "Focus on the center of the animation. Let your thoughts follow the gentle movement."
                    }
                },
                "grounding_543": {
                    "mcp_tool": "grounding_543",
                    "intervention": {
                        "name": "5-4-3-2-1 Grounding Exercise",
                        "type": "sensory_grounding",
                        "description": "Reconnect with your physical environment through your senses",
                        "steps": [
                            {"step": 1, "sense": "sight", "count": 5, "instruction": "Look around and name 5 things you can see", "examples": ["the wall", "your hands", "a door"]},
                            {"step": 2, "sense": "touch", "count": 4, "instruction": "Find and touch 4 different textures", "examples": ["your clothing", "a surface", "your hair"]},
                            {"step": 3, "sense": "hearing", "count": 3, "instruction": "Listen carefully for 3 distinct sounds", "examples": ["your breathing", "distant sounds"]},
                            {"step": 4, "sense": "smell", "count": 2, "instruction": "Notice 2 different scents", "examples": ["the air", "soap"]},
                            {"step": 5, "sense": "taste", "count": 1, "instruction": "Focus on 1 taste you can detect", "examples": ["your mouth", "neutral"]}
                        ],
                        "completion_message": "Perfect! You are here, in this moment, in this place. You are present and safe."
                    }
                },
                "muscle_relaxation": {
                    "mcp_tool": "muscle_relaxation",
                    "intervention": {
                        "name": "Guided Progressive Muscle Relaxation",
                        "type": "physical_release",
                        "description": "Release physical tension through systematic muscle tension and release",
                        "estimated_duration": 240,
                        "instructions": "Tense each muscle group for 5 seconds, then completely release and notice the relaxation",
                        "muscle_groups": [
                            {"name": "hands_and_forearms", "tension_instruction": "Make tight fists and tense your forearms", "release_instruction": "Open your hands and let your arms fall completely loose", "focus": "Notice the contrast between tension and relaxation"},
                            {"name": "upper_arms_and_shoulders", "tension_instruction": "Pull your arms tight against your body and lift your shoulders to your ears", "release_instruction": "Let your arms drop heavy and your shoulders fall down", "focus": "Feel the weight of your arms as they relax"},
                            {"name": "face_and_head", "tension_instruction": "Scrunch your face tight - close eyes, clench jaw, furrow brow", "release_instruction": "Let your entire face go soft and smooth", "focus": "Allow your jaw to drop slightly open"},
                            {"name": "legs_and_feet", "tension_instruction": "Straighten your legs, point your toes, tense your thighs", "release_instruction": "Let your legs become completely heavy and loose", "focus": "Feel your legs sinking into relaxation"}
                        ],
                        "completion_message": "Excellent work. Your body has released significant tension. Take a moment to appreciate how much calmer you feel."
                    }
                },
                "emergency_soundscape": {
                    "mcp_tool": "emergency_soundscape",
                    "intervention": {
                        "name": "Emergency Comfort: Gentle Rain",
                        "type": "immersive_comfort",
                        "description": "A safe, comforting sensory experience that requires no effort from you",
                        "duration_seconds": 300,
                        "soundscape": {"name": "Gentle Rain", "description": "Soft rain on a window"},
                        "primary_message": "You are safe. This feeling will pass. You are not alone.",
                        "instructions": "Just breathe and let the sounds wash over you."
                    }
                },
# =============================================================================
# FEATURE 2: VALUES COMPASS - Personal Values Discovery & Decision Framework  
# =============================================================================
                "values_discovery_expedition": {
                    "mcp_tool": "values_discovery_expedition",
                    "stage": "scenario", 
                    "current_scenario": {
                        "id": 1,
                        "domain": "career",
                        "scenario": "You're offered two job opportunities:",
                        "path_a": {"text": "A secure, well-paying job with a defined career ladder that your family would be proud of"},
                        "path_b": {"text": "A lower-paying role at a startup with high risk, but complete creative freedom"}
                    },
                    "progress": {"current": 1, "total": 7},
                    "intro_message": "Let's explore what truly drives you. There are no right or wrong answers, only what feels most authentic to you."
                },

                "values_synthesis_analysis": {
                    "mcp_tool": "values_synthesis_analysis", 
                    "ai_insight": "I've noticed a pattern in your expedition. You consistently chose paths that involved personal freedom and creative expression, even when they were less secure. This suggests that Autonomy and Creativity might be very important to you.",
                    "suggested_values": [
                        {"name": "autonomy", "count": 4, "definition": "The freedom to make your own choices", "highlighted": True},
                        {"name": "creativity", "count": 3, "definition": "The drive to express yourself", "highlighted": True},
                        {"name": "growth", "count": 2, "definition": "Continuous learning and development", "highlighted": True},
                        {"name": "adventure", "count": 3, "definition": "The desire for new experiences", "highlighted": True},
                        {"name": "authenticity", "count": 2, "definition": "Being true to yourself", "highlighted": False},
                        {"name": "community", "count": 1, "definition": "Connection with others", "highlighted": False},
                        {"name": "security", "count": 1, "definition": "Stability and safety", "highlighted": False}
                    ],
                    "instruction": "Do these resonate? Please select the 3-5 that feel like your 'True North'—the values that are most essentially you."
                },

                "values_compass_creation": {
                    "mcp_tool": "values_compass_creation",
                    "compass": {
                        "true_north_values": ["autonomy", "creativity", "growth"],
                        "supporting_values": ["adventure", "authenticity"],
                        "personalized_definitions": {
                            "autonomy": "For you, Autonomy means more than just being independent. It's the freedom to chart your own course and build your life on your own terms, even if that path is uncertain.",
                            "creativity": "Your Creativity isn't just about art—it's about finding innovative solutions and expressing your unique perspective in everything you do.",
                            "growth": "For you, Growth represents your deep curiosity and drive to continuously evolve, learn, and become the best version of yourself."
                        }
                    },
                    "completion_message": "Your Personal Values Compass is ready! This is your guide for authentic decision-making."
                },

                "values_compass_check": {
                    "mcp_tool": "values_compass_check",
                    "guidance": "Looking at your core values of Autonomy and Creativity, this decision seems to create some tension. The secure option honors stability but might limit your creative freedom. Consider: Is there a way to negotiate more creative control in the secure role? Or could you find ways to express your creativity outside of work while maintaining financial security?",
                    "framework": {
                        "alignment": "Which option aligns most closely with your 'True North' values?",
                        "tension": "Does this choice create significant tension with any of your core values?",
                        "integration": "Is there a third path that could honor multiple values at once?"
                    }
                },
# =============================================================================
# END OF FEATURE 2: VALUES COMPASS
# =============================================================================
# =============================================================================
# FEATURE 3: EMPATHY MAP BUILDER  
# =============================================================================

                "empathy_map_setup": {
                    "mcp_tool": "empathy_map_setup",
                    "setup_complete": True,
                    "person_name": "My Dad",
                    "goal": "Tell him I'm switching from pre-med to graphic design",
                    "message": "Perfect! We're building an empathy map for My Dad. Remember, the goal isn't to win an argument, but to build a bridge of understanding so your message can be truly heard.",
                    "next_step": "inquiry"
                },

                "empathy_map_inquiry": {
                    "mcp_tool": "empathy_map_inquiry",
                    "stage": "question",
                    "category": "hopes",
                    "question_number": 1,
                    "question": "What is their biggest dream for your future?",
                    "category_title": "HOPES & VALUES (What they want for you)",
                    "instruction": "Take your time to really think about their perspective. There are no wrong answers.",
                    "progress": {"current": 1, "total": 8}
                },

                "empathy_map_synthesis": {
                    "mcp_tool": "empathy_map_synthesis",
                    "empathy_map": {
                        "person_name": "My Dad",
                        "conversation_goal": "Tell him I'm switching from pre-med to graphic design",
                        "ai_insight": "Deep down, his primary motivation is a fear of your vulnerability. His desire for you to be a doctor is his strategy to keep you safe.",
                        "raw_analysis": "Based on your responses, here's what drives your dad..."
                    },
                    "message": "Your empathy map has been created! This reveals the deeper motivations and fears driving their perspective."
                },

                "empathy_map_strategy": {
                    "mcp_tool": "empathy_map_strategy",
                    "guidance": "Instead of starting with 'I'm quitting pre-med,' consider opening with: 'Dad, I know you've always wanted me to have a stable and secure future, and I'm grateful for that. I've been thinking about the best way to achieve that security, and I want to share a plan I've made...'",
                    "message": "Your strategic conversation plan is ready! You now have the insights and approach to have a meaningful, empathetic dialogue."
                },

# =============================================================================
# FEATURE 5: DIALOGUE GYM - Interactive Social Skills Training
# =============================================================================

                "dialogue_gym_scenarios": {
                    "mcp_tool": "dialogue_gym_scenarios",
                    "action": "list_zones", 
                    "zones": [
                        {"id": "assertiveness", "name": "Assertiveness Zone", "description": "Practice setting boundaries and saying 'no' confidently", "scenario_count": 2},
                        {"id": "reaching_out", "name": "Reaching Out Zone", "description": "Practice asking for help and support", "scenario_count": 1},
                        {"id": "social_connection", "name": "Social Connection Zone", "description": "Practice building friendships and social skills", "scenario_count": 1},
                        {"id": "heart_to_heart", "name": "Heart-to-Heart Zone", "description": "Practice vulnerable and significant conversations", "scenario_count": 1}
                    ]
                },

                "dialogue_gym_persona": {
                    "mcp_tool": "dialogue_gym_persona",
                    "persona_response": "Hey! I'm in a really tight spot right now. Could you possibly lend me $200? I promise I'll pay you back next month.",
                    "turn_number": 1
                },

                "dialogue_gym_coach": {
                    "mcp_tool": "dialogue_gym_coach", 
                    "feedback": "Good start! You clearly stated your boundary. Now try adding empathy to acknowledge their situation."
                },

                "dialogue_gym_analysis": {
                    "mcp_tool": "dialogue_gym_analysis",
                    "performance_analysis": "★★★★☆ Clarity: You communicated your boundaries clearly\n★★★☆☆ Empathy: Could acknowledge their feelings more\n★★★★☆ Goal Achievement: Successfully declined while preserving friendship\n\nAlternative phrase: 'I understand you're stressed, but I can't lend money right now. How else can I support you?'"
                }


            }
            
            return mock_responses.get(tool_name, {"error": f"Tool {tool_name} not found"})
            
        except Exception as e:
            logger.error(f"MCP call error: {e}")
            return {"error": str(e)}

# Initialize MCP client
mcp_client = YouthPortalMCPClient()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Youth Portal - MCP Powered Mental Wellness</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; padding: 20px; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 20px; text-align: center; }
            .mcp-badge { background: #10b981; color: white; padding: 5px 15px; border-radius: 20px; font-size: 14px; margin-bottom: 20px; display: inline-block; }
            .sos-button { background: linear-gradient(45deg, #ff4444, #cc3333); color: white; padding: 25px 50px; font-size: 24px; font-weight: bold; border: none; border-radius: 50px; cursor: pointer; width: 100%; margin: 20px 0; box-shadow: 0 6px 20px rgba(255,68,68,0.4); transition: all 0.3s ease; }
            .sos-button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(255,68,68,0.6); }
            .send-button { background: #4299e1; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; margin-top: 15px; transition: all 0.3s ease; }
            .send-button:hover { background: #3182ce; }
            #user-input { width: 100%; height: 100px; padding: 15px; border: 2px solid #ddd; border-radius: 10px; font-size: 16px; margin: 10px 0; resize: vertical; }
            
            .triage-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); display: none; flex-direction: column; justify-content: center; align-items: center; padding: 20px; z-index: 1000; }
            .intervention-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: #1a202c; color: white; display: none; flex-direction: column; justify-content: center; align-items: center; padding: 20px; z-index: 1001; }
            
            .triage-option { background: rgba(255,255,255,0.9); color: #333; padding: 20px 25px; margin: 8px; border: none; border-radius: 15px; cursor: pointer; font-size: 18px; width: 90%; max-width: 500px; text-align: left; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            .triage-option:hover { background: white; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
            
            .exit-button { position: fixed; top: 20px; right: 20px; background: rgba(255,255,255,0.2); color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; font-size: 18px; }
            
            .breathing-circle { width: 200px; height: 200px; border-radius: 50%; background: radial-gradient(circle, #4299e1, #2b6cb0); margin: 20px; transition: transform 4s ease-in-out; }
            .breathing-expanded { transform: scale(1.3); }
            .breathing-contracted { transform: scale(0.7); }
            
            .visual-focus {
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: conic-gradient(from 0deg, #805ad5, #d69e2e, #38b2ac, #805ad5);
    animation: rotate 20s linear infinite;
    margin: 40px auto;
    display: block;
}
            @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            
            .grounding-step { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px; text-align: center; max-width: 500px; }
            .soundscape-visual { width: 100%; height: 200px; background: linear-gradient(45deg, #2d3748, #4a5568); border-radius: 15px; margin: 20px 0; position: relative; overflow: hidden; }
            .soundscape-visual::after { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent); animation: shimmer 3s infinite; }
            @keyframes shimmer { 0% { left: -100%; } 100% { left: 100%; } }
            
            .intervention-button { background: #48bb78; color: white; padding: 15px 30px; border: none; border-radius: 10px; cursor: pointer; font-size: 16px; margin: 10px; }
            .intervention-button:hover { background: #38a169; }
            
            #response { margin-top: 20px; padding: 15px; border-radius: 8px; display: none; }
            .success { background: #c6f6d5; color: #22543d; }
            .mcp-info { background: #e6fffa; color: #234e52; }

            .rain-animation {
                position: relative;
                width: 100%;
                height: 300px;
                background: linear-gradient(45deg, #2c5f70, #1a4c63);
                border-radius: 15px;
                overflow: hidden;
                margin: 20px 0;
            }

            .rain-animation::before {
                content: '';
                position: absolute;
                top: -100%;
                left: 0;
                width: 100%;
                height: 200%;
                background-image: 
                    radial-gradient(2px 10px at 20px 30px, rgba(255,255,255,0.3), transparent),
                    radial-gradient(2px 8px at 40px 70px, rgba(255,255,255,0.2), transparent),
                    radial-gradient(1px 12px at 90px 40px, rgba(255,255,255,0.4), transparent),
                    radial-gradient(2px 15px at 60px 80px, rgba(255,255,255,0.2), transparent);
                background-repeat: repeat;
                background-size: 100px 120px;
                animation: rainfall 3s linear infinite;
            }

            @keyframes rainfall {
                from { transform: translateY(-100%); }
                to { transform: translateY(100%); }
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }


            /* Fix Visual Focus alignment */
/* Fix Visual Focus alignment */
.visual-focus-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 80vh;
    padding: 20px;
}

.visual-focus-circle {
    width: 300px;
    height: 300px;
    border-radius: 50%;
    margin: 30px auto;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.visual-focus-text {
    max-width: 600px;
    margin: 20px auto;
    text-align: center;
    line-height: 1.6;
}


            .visual-focus-circle {
                width: 300px;
                height: 300px;
                border-radius: 50%;
                margin: 30px auto;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .visual-focus-text {
                max-width: 600px;
                margin: 20px auto;
                text-align: center;
                line-height: 1.6;
            }
            /* Fix S.O.S. Triage alignment */
.sos-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    padding: 20px;
    text-align: center;
}

.sos-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    max-width: 1000px;
    margin: 30px auto;
    width: 100%;
}

.sos-option {
    padding: 20px;
    border-radius: 15px;
    cursor: pointer;
    transition: transform 0.2s ease;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 120px;
}

.sos-option:hover {
    transform: translateY(-2px);
}
/* Fix Box Breathing alignment */
.breathing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    min-height: 80vh;
    padding: 20px;
}

.breathing-circle {
    width: 250px;
    height: 250px;
    border-radius: 50%;
    margin: 40px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.breathing-instructions {
    max-width: 500px;
    margin: 20px auto;
    text-align: center;
    font-size: 18px;
    line-height: 1.5;
}

.breathing-controls {
    margin-top: 30px;
    text-align: center;
}


.breathing-circle {
    width: 250px;
    height: 250px;
    border-radius: 50%;
    margin: 40px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.breathing-instructions {
    max-width: 500px;
    margin: 20px auto;
    text-align: center;
    font-size: 18px;
    line-height: 1.5;
}

.breathing-controls {
    margin-top: 30px;
    text-align: center;
}

/* Global fixes for tool containers */
.tool-interface {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    min-height: 100vh;
    padding: 20px;
    box-sizing: border-box;
}

.tool-content {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Responsive design fixes */
@media (max-width: 768px) {
    .visual-focus-circle,
    .breathing-circle {
        width: 200px;
        height: 200px;
    }
    
    .sos-options {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .tool-interface {
        padding: 10px;
    }
}

/* Center all buttons */
.action-button {
    display: block;
    margin: 20px auto;
    padding: 15px 30px;
    border: none;
    border-radius: 25px;
    background: #28a745;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.action-button:hover {
    background: #218838;
    transform: translateY(-1px);
}

    


        </style>
    </head>
    <body>
        <!-- Main Interface -->
        <div id="main-interface" class="container">
            <div class="mcp-badge">⚡ Powered by MCP Server</div>
            <h1>🤖 Youth Mental Wellness Portal</h1>
            <p style="color: #666; margin-bottom: 20px;">Connected to Mental Wellness MCP Server</p>
            <p style="color: #999; margin-bottom: 30px; font-size: 14px;">All interventions powered by Model Context Protocol tools</p>
            
            <button onclick="openSafetyNet()" style="
    background: linear-gradient(135deg, #dc3545, #c82333);
    color: white;
    padding: 18px 25px;
    border: none;
    border-radius: 15px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    width: 100%;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(220,53,69,0.3);
    transition: all 0.3s ease;
">
    🆘 Safety Net & Resources
</button>


            <button class="sos-button" onclick="triggerMCPSOS()">
                🚨 S.O.S. - I Need Help Right Now
            </button>
            <!-- VALUE COMPASS BUTTON -->
            <button class="values-compass-button" onclick="startValuesCompass()" style="background: linear-gradient(45deg, #4a90e2, #7b68ee); color: white; padding: 20px 40px; font-size: 20px; border: none; border-radius: 40px; cursor: pointer; width: 100%; margin: 15px 0; transition: all 0.3s ease;">
                🧭 Discover Your Values Compass
            </button>
            <!--EMPATHY MAP BUTTON-->
            <button class="empathy-map-button" onclick="startEmpathyMap()" style="background: linear-gradient(45deg, #28a745, #20c997); color: white; padding: 20px 40px; font-size: 20px; border: none; border-radius: 40px; cursor: pointer; width: 100%; margin: 15px 0; transition: all 0.3s ease;">
            🗺️ Build an Empathy Map
            </button>
            <button class="future-self-button" onclick="startFutureSelf()" style="background: linear-gradient(45deg, #6f42c1, #e83e8c); color: white; padding: 20px 40px; font-size: 20px; border: none; border-radius: 40px; cursor: pointer; width: 100%; margin: 15px 0; transition: all 0.3s ease;">
    ⏳ Simulate Your Future Self
</button><!--DIALOGUE GYM BUTTON-->
<!--DIALOGUE GYM BUTTON-->
<button onclick="showDialogueGymUI()" style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 20px 40px; font-size: 20px; border: none; border-radius: 40px; cursor: pointer; width: 100%; margin: 15px 0; transition: all 0.3s ease;">
    💬 Enter the Dialogue Gym
</button>


            <div>
                <textarea id="user-input" placeholder="How are you feeling today?"></textarea>
                <button class="send-button" onclick="analyzeCrisisWithMCP()">Analyze</button>
                <div id="response"></div>
            </div>
        </div>
        
        <!-- S.O.S. Triage Screen -->
        <div id="triage-screen" class="triage-screen">
            <button class="exit-button" onclick="exitSOS()">✕ Exit</button>
            <h2 style="color: #2d3748; margin-bottom: 10px; text-align: center; font-weight: 300;">MCP S.O.S. Triage</h2>
            <h3 id="triage-question" style="color: #2d3748; margin-bottom: 30px; text-align: center; font-weight: 400;"></h3>
            <div id="triage-options"></div>
        </div>
        
        <!-- Intervention Screen -->
        <div id="intervention-screen" class="intervention-screen">
            <button class="exit-button" onclick="exitSOS()">✕ Exit</button>
            <div id="intervention-content" style="text-align: center; max-width: 600px;"></div>
            <button class="intervention-button" onclick="exitSOS()" style="margin-top: 30px;">I'm Feeling Better</button>
        </div>

        <script>
            console.log('=== YOUTH PORTAL MCP CLIENT LOADED ===');
// =============================================================================
// FEATURE 1 JAVASCRIPT: CRISIS INTERVENTION FUNCTIONS
// =============================================================================

            async function triggerMCPSOS() {
                console.log('Triggering S.O.S. via MCP Server...');
                
                try {
                    // Call MCP sos_triage tool
                    const response = await fetch('/mcp/sos_triage');
                    const mcpResult = await response.json();
                    
                    console.log('MCP Triage Response:', mcpResult);
                    
                    // Display triage screen
                    document.getElementById('main-interface').style.display = 'none';
                    document.getElementById('triage-screen').style.display = 'flex';
                    
                    // Set triage question
                    document.getElementById('triage-question').textContent = mcpResult.question;
                    
                    // Generate option buttons
                    const optionsHtml = mcpResult.options.map(option => 
                        `<button class="triage-option" onclick="selectMCPIntervention('${option.recommended_tool}', '${option.id}')">${option.text}</button>`
                    ).join('');
                    
                    document.getElementById('triage-options').innerHTML = optionsHtml;
                    
                } catch (error) {
                    console.error('MCP S.O.S. error:', error);
                    alert('Connection to MCP server failed. Please ensure the MCP server is running.');
                }
            }
            
            async function selectMCPIntervention(toolName, symptomId) {
                console.log('Launching MCP intervention tool:', toolName, 'for symptom:', symptomId);
                
                try {
                    // Call the specific MCP intervention tool
                    const response = await fetch(`/mcp/${toolName}`);
                    const mcpResult = await response.json();
                    
                    console.log('MCP Intervention Response:', mcpResult);
                    
                    // Hide triage, show intervention
                    document.getElementById('triage-screen').style.display = 'none';
                    document.getElementById('intervention-screen').style.display = 'flex';
                    
                    // Display the intervention
                    displayMCPIntervention(mcpResult);
                    
                } catch (error) {
                    console.error('MCP intervention error:', error);
                    alert(`Failed to load MCP intervention: ${toolName}`);
                }
            }
            
            function displayMCPIntervention(mcpResult) {
                const content = document.getElementById('intervention-content');
                const intervention = mcpResult.intervention;
                
                let html = `
                    <div style="background: rgba(16, 185, 129, 0.1); padding: 10px 20px; border-radius: 10px; margin-bottom: 20px;">
                        <small style="color: #10b981;">🔗 MCP Tool: ${mcpResult.mcp_tool}</small>
                    </div>
                    <h2 style="margin-bottom: 20px;">${intervention.name}</h2>
                    <p style="font-size: 18px; margin-bottom: 30px; opacity: 0.9;">${intervention.description}</p>
                `;
                
                if (intervention.type === 'breathing_visual') {
                    html += `
                        <div class="breathing-circle" id="breathing-circle"></div>
                        <p id="breathing-text" style="font-size: 24px; margin-top: 20px;">Get ready to breathe with the circle...</p>
                        <p style="font-size: 16px; opacity: 0.7; margin-top: 10px;">Total cycles: ${intervention.total_cycles} | Duration: ${intervention.duration_seconds}s</p>
                    `;
                    content.innerHTML = html;
                    setTimeout(() => startMCPBreathing(intervention), 2000);
                    
                } else if (intervention.type === 'visual_meditation') {
                    html += `
                        <div class="visual-focus"></div>
                        <p style="font-size: 18px; margin-top: 20px; opacity: 0.9;">${intervention.instructions}</p>
                        <p style="font-size: 14px; opacity: 0.7; margin-top: 10px;">Animation: ${intervention.animation.type} | Speed: ${intervention.animation.speed}</p>
                    `;
                    content.innerHTML = html;
                    
                } else if (intervention.type === 'sensory_grounding') {
                    html += '<div id="mcp-grounding-steps"></div>';
                    content.innerHTML = html;
                    setTimeout(() => startMCPGrounding(intervention.steps, intervention.completion_message), 1000);

                } else if (intervention.type === 'physical_release') {
                    html += '<div id="mcp-muscle-steps"></div>';
                        content.innerHTML = html;
                        setTimeout(() => startMCPMuscleRelaxation(intervention.muscle_groups, intervention.completion_message), 1000);
    
                } else if (intervention.type === 'immersive_comfort') {
                    html += `
                        <div class="rain-animation"></div>
                        <h3 style="margin: 30px 0; color: #48bb78; font-weight: 300;">${intervention.primary_message}</h3>
                        <p style="font-size: 18px; opacity: 0.8;">${intervention.instructions}</p>
                        <p style="font-size: 14px; opacity: 0.6; margin-top: 15px;">Soundscape: ${intervention.soundscape.name}</p>
                    `;
                    content.innerHTML = html;

                    
                } else {
                    content.innerHTML = html + '<p>MCP intervention loaded successfully.</p>';
                }
            }
            
            function startMCPBreathing(intervention) {
                const circle = document.getElementById('breathing-circle');
                const text = document.getElementById('breathing-text');
                const pattern = intervention.breathing_pattern;
                let currentPhase = 0;
                let cycleCount = 0;
                
                function breathingPhase() {
                    const phase = pattern[currentPhase];
                    text.textContent = phase.instruction;
                    
                    if (phase.visual_cue === 'expand') {
                        circle.className = 'breathing-circle breathing-expanded';
                    } else if (phase.visual_cue === 'contract') {
                        circle.className = 'breathing-circle breathing-contracted';
                    } else {
                        circle.className = 'breathing-circle';
                    }
                    
                    currentPhase = (currentPhase + 1) % pattern.length;
                    if (currentPhase === 0) cycleCount++;
                    
                    if (cycleCount < intervention.total_cycles) {
                        setTimeout(breathingPhase, phase.duration * 1000);
                    } else {
                        text.textContent = 'Excellent work! Notice how much calmer you feel now.';
                        circle.className = 'breathing-circle';
                    }
                }
                
                breathingPhase();
            }
            
            function startMCPGrounding(steps, completionMessage) {
                let currentStep = 0;
                const container = document.getElementById('mcp-grounding-steps');
                
                function showGroundingStep() {
                    if (currentStep >= steps.length) {
                        container.innerHTML = `
                            <div class="grounding-step">
                                <h2 style="color: #48bb78; margin-bottom: 20px;">Perfect!</h2>
                                <h3 style="margin-bottom: 15px;">${completionMessage}</h3>
                                <p style="font-size: 14px; opacity: 0.7;">MCP grounding exercise completed successfully.</p>
                            </div>
                        `;
                        return;
                    }
                    
                    const step = steps[currentStep];
                    container.innerHTML = `
                        <div class="grounding-step">
                            <h3 style="margin-bottom: 20px;">Step ${step.step}: ${step.instruction}</h3>
                            <p style="margin: 15px 0; opacity: 0.8;">Examples: ${step.examples.join(', ')}</p>
                            <button class="intervention-button" onclick="nextMCPGroundingStep()">Found them - Next Step</button>
                        </div>
                    `;
                }
                
                window.nextMCPGroundingStep = function() {
                    currentStep++;
                    showGroundingStep();
                }
                
                showGroundingStep();
            }
            
            function startMCPMuscleRelaxation(muscleGroups, completionMessage) {
                let currentGroup = 0;
                const container = document.getElementById('mcp-muscle-steps');
    
                function showMuscleGroup() {
                    if (currentGroup >= muscleGroups.length) {
                        container.innerHTML = `
                            <div class="grounding-step">
                                <h2 style="color: #48bb78; margin-bottom: 20px;">Relaxation Complete</h2>
                                <h3 style="margin-bottom: 15px;">${completionMessage}</h3>
                            </div>
                        `;
                    return;
                }
        
        const group = muscleGroups[currentGroup];
        container.innerHTML = `
            <div class="grounding-step">
                <h3 style="margin-bottom: 20px;">${group.name.replace(/_/g, ' ').toUpperCase()}</h3>
                <p style="margin: 15px 0;"><strong>Tense:</strong> ${group.tension_instruction}</p>
                <p style="margin: 15px 0;"><strong>Release:</strong> ${group.release_instruction}</p>
                <p style="margin: 15px 0; font-size: 14px; opacity: 0.8;">${group.focus}</p>
                <button class="intervention-button" onclick="nextMCPMuscleGroup()">Done - Next Group</button>
            </div>
        `;
    }
    
    window.nextMCPMuscleGroup = function() {
        currentGroup++;
        showMuscleGroup();
    }
    
    showMuscleGroup();
}
// =============================================================================
// FEATURE 2 JAVASCRIPT: VALUES COMPASS FUNCTIONS  
// =============================================================================

// COMPLETE VALUES COMPASS FUNCTIONS
let valuesJourney = {
    stage: 'start',
    responses: [],
    selectedValues: [],
    scenarios: [
        {
            "id": 1, "domain": "career", "scenario": "You're offered two job opportunities:",
            "path_a": {"text": "A secure, well-paying job with a defined career ladder that your family would be proud of"},
            "path_b": {"text": "A lower-paying role at a startup with high risk, but complete creative freedom"}
        },
        {
            "id": 2, "domain": "social", "scenario": "Your friend group is planning something you don't agree with:",
            "path_a": {"text": "Go along to maintain harmony and avoid conflict"},
            "path_b": {"text": "Speak your truth, risking conflict but staying authentic to yourself"}
        },
        {
            "id": 3, "domain": "lifestyle", "scenario": "You have savings and two life paths to choose:",
            "path_a": {"text": "Buy a home in your familiar hometown, surrounded by support system"},
            "path_b": {"text": "Use savings to travel the world for a year, embracing uncertainty and new experiences"}
        },
        {
            "id": 4, "domain": "impact", "scenario": "You want to make a difference in the world:",
            "path_a": {"text": "Volunteer for local charity, making direct impact on a few individuals"},
            "path_b": {"text": "Work on large-scale policy, indirect impact that might affect thousands in years"}
        },
        {
            "id": 5, "domain": "relationships", "scenario": "In romantic relationships, you value:",
            "path_a": {"text": "Deep emotional intimacy and vulnerability, even if it's intense"},
            "path_b": {"text": "Healthy independence and personal space within the relationship"}
        },
        {
            "id": 6, "domain": "learning", "scenario": "When learning something new, you prefer:",
            "path_a": {"text": "Mastering one subject deeply, becoming an expert in that field"},
            "path_b": {"text": "Learning broadly across many subjects, staying curious about everything"}
        },
        {
            "id": 7, "domain": "success", "scenario": "Your definition of success is:",
            "path_a": {"text": "Being recognized and respected by others for your achievements"},
            "path_b": {"text": "Feeling fulfilled and proud of your personal growth, regardless of outside recognition"}
        }
    ]
};

async function startValuesCompass() {
    console.log('Starting Values Compass journey...');
    
    try {
        // Reset journey
        valuesJourney.responses = [];
        valuesJourney.selectedValues = [];
        
        // Hide main interface, show values interface
        document.getElementById('main-interface').style.display = 'none';
        showValuesInterface();
        
        // Start with first scenario
        displayValuesScenario({
            stage: 'scenario',
            current_scenario: valuesJourney.scenarios[0],
            progress: {current: 1, total: 7},
            intro_message: "Let's explore what truly drives you. There are no right or wrong answers, only what feels most authentic to you."
        });
        
    } catch (error) {
        console.error('Values Compass error:', error);
        alert('Failed to start Values Compass. Please try again.');
        document.getElementById('main-interface').style.display = 'block';
        if (document.getElementById('values-interface')) {
            document.getElementById('values-interface').style.display = 'none';
        }
    }
}

function showValuesInterface() {
    if (!document.getElementById('values-interface')) {
        const valuesHTML = `
            <div id="values-interface" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; z-index: 2000;">
                <button class="exit-button" onclick="exitValuesCompass()">✕ Exit</button>
                <div id="values-content" style="max-width: 700px; max-height: 80vh; background: white; padding: 40px; border-radius: 20px; text-align: center; overflow-y: auto; overflow-x: hidden;"></div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', valuesHTML);
    }
    
    document.getElementById('values-interface').style.display = 'flex';
}


function displayValuesScenario(mcpResult) {
    const content = document.getElementById('values-content');
    
    console.log('Displaying scenario:', mcpResult);
    
    if (mcpResult.stage === 'scenario' && mcpResult.current_scenario) {
        const scenario = mcpResult.current_scenario;
        content.innerHTML = `
            <div style="text-align: left;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #4a90e2; margin-bottom: 10px;">🧭 Values Discovery Expedition</h2>
                    <p style="color: #666;">${mcpResult.intro_message || 'Choose the path that feels most authentic to you.'}</p>
                    <div style="background: #f0f4f8; padding: 10px; border-radius: 10px; margin: 20px 0;">
                        <strong>Progress:</strong> ${mcpResult.progress.current} of ${mcpResult.progress.total}
                    </div>
                </div>
                
                <h3 style="margin-bottom: 20px; color: #333;">${scenario.scenario}</h3>
                
                <button onclick="chooseValuesPath('path_a', ${scenario.id})" style="display: block; width: 100%; padding: 20px; margin: 15px 0; background: #e8f4fd; border: 2px solid #4a90e2; border-radius: 10px; cursor: pointer; text-align: left; font-size: 16px;">
                    <strong>Path A:</strong> ${scenario.path_a.text}
                </button>
                
                <button onclick="chooseValuesPath('path_b', ${scenario.id})" style="display: block; width: 100%; padding: 20px; margin: 15px 0; background: #f3e8ff; border: 2px solid #7b68ee; border-radius: 10px; cursor: pointer; text-align: left; font-size: 16px;">
                    <strong>Path B:</strong> ${scenario.path_b.text}
                </button>
            </div>
        `;
    }
}

async function chooseValuesPath(choice, scenarioId) {
    console.log('Values choice:', choice, 'for scenario:', scenarioId);
    
    // Record the response
    valuesJourney.responses.push({
        scenario_id: scenarioId,
        choice: choice
    });
    
    // Check if more scenarios
    const nextScenarioId = scenarioId + 1;
    if (nextScenarioId <= valuesJourney.scenarios.length) {
        // Show next scenario
        const nextScenario = valuesJourney.scenarios[nextScenarioId - 1];
        displayValuesScenario({
            stage: 'scenario',
            current_scenario: nextScenario,
            progress: {current: nextScenarioId, total: 7}
        });
    } else {
        // All scenarios complete - move to synthesis
        startValuesSynthesis();
    }
}

async function startValuesSynthesis() {
    console.log('Starting values synthesis with responses:', valuesJourney.responses);
    
    const response = await fetch('/mcp/values_synthesis_analysis');
    const result = await response.json();
    displayValuesSynthesis(result);
}

function displayValuesSynthesis(mcpResult) {
    const content = document.getElementById('values-content');
    
    content.innerHTML = `
        <div style="text-align: left;">
            <h2 style="color: #4a90e2; text-align: center; margin-bottom: 20px;">🔍 Pattern Recognition</h2>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p style="font-style: italic; color: #2c5aa0;">"${mcpResult.ai_insight}"</p>
            </div>
            
            <h3 style="margin: 20px 0;">Select Your Core Values</h3>
            <p style="color: #666; margin-bottom: 20px;">${mcpResult.instruction}</p>
            
            <div id="values-selection">
                ${mcpResult.suggested_values.map(value => `
                    <label style="display: block; padding: 15px; margin: 10px 0; background: ${value.highlighted ? '#fff3cd' : '#f8f9fa'}; border: 2px solid ${value.highlighted ? '#ffc107' : '#e9ecef'}; border-radius: 10px; cursor: pointer;">
                        <input type="checkbox" name="core-values" value="${value.name}" style="margin-right: 10px;" ${value.highlighted ? 'checked' : ''}>
                        <strong>${value.name.charAt(0).toUpperCase() + value.name.slice(1)}</strong>
                        ${value.highlighted ? '<span style="color: #856404;"> ⭐ Strongly indicated</span>' : ''}
                        <br><small style="color: #666;">${value.definition}</small>
                    </label>
                `).join('')}
            </div>
            
            <button onclick="finalizeValuesSelection()" style="width: 100%; padding: 15px; margin-top: 20px; background: #4a90e2; color: white; border: none; border-radius: 10px; font-size: 18px; cursor: pointer;">
                Create My Values Compass
            </button>
        </div>
    `;
}

async function finalizeValuesSelection() {
    const checkedValues = Array.from(document.querySelectorAll('input[name="core-values"]:checked')).map(cb => cb.value);
    
    if (checkedValues.length < 3) {
        alert('Please select at least 3 values that feel most essential to you.');
        return;
    }
    
    if (checkedValues.length > 5) {
        alert('Please select no more than 5 core values to keep your compass focused.');
        return;
    }
    
    valuesJourney.selectedValues = checkedValues;
    
    // Create compass
    const response = await fetch('/mcp/values_compass_creation');
    const result = await response.json();
    displayValuesCompass(result);
}

function displayValuesCompass(mcpResult) {
    const content = document.getElementById('values-content');
    const compass = mcpResult.compass;
    
    content.innerHTML = `
        <div style="text-align: center;">
            <h2 style="color: #4a90e2; margin-bottom: 20px;">🧭 Your Personal Values Compass</h2>
            
            <div style="background: linear-gradient(135deg, #4a90e2, #7b68ee); color: white; padding: 30px; border-radius: 20px; margin: 20px 0;">
                <h3 style="margin-bottom: 20px; color: white;">True North Values</h3>
                ${compass.true_north_values.map(value => `
                    <div style="margin: 15px 0; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 10px;">
                        <strong style="font-size: 18px;">${value.charAt(0).toUpperCase() + value.slice(1)}</strong>
                        <p style="margin: 10px 0; font-size: 14px;">${compass.personalized_definitions[value] || 'Your personalized definition'}</p>
                    </div>
                `).join('')}
            </div>
            
            ${compass.supporting_values.length > 0 ? `
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h4>Supporting Values</h4>
                    <p>${compass.supporting_values.map(v => v.charAt(0).toUpperCase() + v.slice(1)).join(', ')}</p>
                </div>
            ` : ''}
            
            <div style="margin: 30px 0;">
                <p style="color: #48bb78; font-size: 18px; font-weight: bold;">${mcpResult.completion_message}</p>
            </div>
            
            <button onclick="exitValuesCompass()" style="background: #48bb78; color: white; padding: 15px 30px; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; margin: 10px;">
                Complete Journey
            </button>
            
            <button onclick="testCompassCheck()" style="background: #6c757d; color: white; padding: 15px 30px; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; margin: 10px;">
                Try Compass Check
            </button>
        </div>
    `;
}

async function testCompassCheck() {
    const content = document.getElementById('values-content');
    
    // Show input form first
    content.innerHTML = `
        <div style="text-align: left;">
            <h2 style="color: #4a90e2; text-align: center; margin-bottom: 20px;">🧭 Compass Check</h2>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">Use your values to navigate a real decision</p>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <strong>Your Core Values:</strong> ${valuesJourney.selectedValues.map(v => v.charAt(0).toUpperCase() + v.slice(1)).join(', ')}
            </div>
            
            <h3 style="margin-bottom: 15px;">What decision are you facing?</h3>
            <textarea id="dilemma-input" placeholder="E.g., Should I take a safe job or follow my passion? Should I move cities for an opportunity?" style="width: 100%; height: 80px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
            
            <button onclick="runCompassCheck()" style="width: 100%; padding: 15px; background: #4a90e2; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; margin-bottom: 15px;">
                🧭 Get Compass Guidance
            </button>
            
            <button onclick="displayValuesCompass({mcp_tool: 'values_compass_creation', compass: {true_north_values: valuesJourney.selectedValues, supporting_values: [], personalized_definitions: {}}, completion_message: 'Your Personal Values Compass is ready!'})" style="width: 100%; padding: 10px; background: #6c757d; color: white; border: none; border-radius: 10px; font-size: 14px; cursor: pointer;">
                ← Back to My Compass
            </button>
        </div>
    `;
}

async function runCompassCheck() {
    const dilemma = document.getElementById('dilemma-input').value.trim();
    
    if (!dilemma) {
        alert('Please describe your decision or dilemma first.');
        return;
    }
    
    // Show loading
    const content = document.getElementById('values-content');
    content.innerHTML = '<div style="text-align: center; padding: 40px;"><h3>🧭 Analyzing your dilemma...</h3><p>Applying your Values Compass...</p></div>';
    
    try {
        const response = await fetch('/mcp/values_compass_check');
        const result = await response.json();
        
        // Display beautiful results
        content.innerHTML = `
            <div style="text-align: left;">
                <h2 style="color: #4a90e2; text-align: center; margin-bottom: 20px;">🧭 Your Compass Guidance</h2>
                
                <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h4 style="margin-bottom: 10px; color: #2c5aa0;">Your Dilemma:</h4>
                    <p style="font-style: italic;">"${dilemma}"</p>
                </div>
                
                <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h4 style="margin-bottom: 15px; color: #155724;">💡 Compass Guidance:</h4>
                    <p style="line-height: 1.6;">${result.guidance}</p>
                </div>
                
                <h4 style="margin-bottom: 15px;">🎯 Decision Framework:</h4>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <div style="margin-bottom: 15px;">
                        <strong>1. ALIGNMENT:</strong><br>
                        <span style="color: #666;">${result.framework.alignment}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <strong>2. TENSION:</strong><br>
                        <span style="color: #666;">${result.framework.tension}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <strong>3. INTEGRATION:</strong><br>
                        <span style="color: #666;">${result.framework.integration}</span>
                    </div>
                </div>
                
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <button onclick="testCompassCheck()" style="flex: 1; padding: 12px; background: #4a90e2; color: white; border: none; border-radius: 10px; cursor: pointer;">
                        🔄 Try Another Decision
                    </button>
                    <button onclick="displayValuesCompass({mcp_tool: 'values_compass_creation', compass: {true_north_values: valuesJourney.selectedValues, supporting_values: [], personalized_definitions: {}}, completion_message: 'Your Personal Values Compass is ready!'})" style="flex: 1; padding: 12px; background: #28a745; color: white; border: none; border-radius: 10px; cursor: pointer;">
                        ← Back to Compass
                    </button>
                    <button onclick="exitValuesCompass()" style="flex: 1; padding: 12px; background: #6c757d; color: white; border: none; border-radius: 10px; cursor: pointer;">
                        Complete Journey
                    </button>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Compass check error:', error);
        content.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <h3 style="color: #dc3545;">⚠️ Error</h3>
                <p>Could not connect to MCP server. Please try again.</p>
                <button onclick="testCompassCheck()" style="padding: 15px 30px; background: #4a90e2; color: white; border: none; border-radius: 10px; cursor: pointer;">
                    Try Again
                </button>
            </div>
        `;
    }
}


function exitValuesCompass() {
    document.getElementById('values-interface').style.display = 'none';
    document.getElementById('main-interface').style.display = 'block';
    valuesJourney = {stage: 'start', responses: [], selectedValues: [], scenarios: valuesJourney.scenarios};
}

// =============================================================================
// FEATURE 3 JAVASCRIPT: EMPATHY MAP BUILDER FUNCTIONS (SIMPLIFIED)
// =============================================================================

let empathyJourney = {
    stage: 'setup',
    personData: {},
    responses: [],
    currentQuestion: 0,
    questions: [
        "What is their biggest dream for your future?",
        "What does a 'successful life' look like from their point of view?", 
        "What words do they often use when talking about the future?",
        "What is their absolute worst-case scenario regarding your situation?",
        "What past struggles or regrets in their own life might be influencing their perspective?",
        "What would they feel they have to sacrifice or lose if you follow your path?",
        "Whose opinions matter most to them? What would those people say?",
        "What cultural messages or media shape their worldview on this topic?"
    ],
    categories: [
        "HOPES & VALUES (What they want for you)",
        "HOPES & VALUES (What they want for you)",
        "HOPES & VALUES (What they want for you)", 
        "FEARS & ANXIETIES (What they are afraid of)",
        "FEARS & ANXIETIES (What they are afraid of)",
        "FEARS & ANXIETIES (What they are afraid of)",
        "EXTERNAL INFLUENCES (What shapes their thinking)",
        "EXTERNAL INFLUENCES (What shapes their thinking)"
    ]
};

async function startEmpathyMap() {
    console.log('Starting Empathy Map Builder...');
    
    // Reset everything
    empathyJourney.responses = [];
    empathyJourney.currentQuestion = 0;
    empathyJourney.personData = {};
    
    // Hide main interface, show empathy interface
    document.getElementById('main-interface').style.display = 'none';
    showEmpathyInterface();
    
    // Show setup form
    displayEmpathySetup();
}

function showEmpathyInterface() {
    if (!document.getElementById('empathy-interface')) {
        const empathyHTML = `
            <div id="empathy-interface" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; z-index: 2000;">
                <button class="exit-button" onclick="exitEmpathyMap()" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer;">✕ Exit</button>
                <div id="empathy-content" style="max-width: 700px; max-height: 80vh; background: white; padding: 40px; border-radius: 20px; text-align: center; overflow-y: auto;"></div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', empathyHTML);
    }
    
    document.getElementById('empathy-interface').style.display = 'flex';
}

function displayEmpathySetup() {
    const content = document.getElementById('empathy-content');
    
    content.innerHTML = `
        <div style="text-align: left;">
            <h2 style="color: #28a745; text-align: center; margin-bottom: 20px;">🗺️ Empathy Map Builder</h2>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">Build deep understanding before difficult conversations</p>
            
            <h3 style="margin-bottom: 15px;">Who are we building this map for?</h3>
            <input id="person-name" placeholder="e.g., My Dad, My Mom, My Partner" style="width: 100%; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px;">
            
            <h3 style="margin-bottom: 15px;">What's your conversation goal?</h3>
            <textarea id="conversation-goal" placeholder="e.g., Tell him I'm switching majors, Ask for their support with my decision" style="width: 100%; height: 80px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
            
            <button onclick="submitEmpathySetup()" style="width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">
                🗺️ Start Building the Map
            </button>
        </div>
    `;
}

function submitEmpathySetup() {
    const personName = document.getElementById('person-name').value.trim();
    const goal = document.getElementById('conversation-goal').value.trim();
    
    if (!personName || !goal) {
        alert('Please fill in both fields to continue.');
        return;
    }
    
    empathyJourney.personData = {
        person_name: personName,
        conversation_goal: goal
    };
    
    // Start with first question
    empathyJourney.currentQuestion = 0;
    displayCurrentQuestion();
}

function displayCurrentQuestion() {
    const content = document.getElementById('empathy-content');
    const questionIndex = empathyJourney.currentQuestion;
    const question = empathyJourney.questions[questionIndex];
    const category = empathyJourney.categories[questionIndex];
    const progress = questionIndex + 1;
    
    content.innerHTML = `
        <div style="text-align: left;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #28a745; margin-bottom: 10px;">🗺️ ${category}</h2>
                <div style="background: #f0f8f0; padding: 10px; border-radius: 10px; margin: 20px 0;">
                    <strong>Progress:</strong> ${progress} of 8
                </div>
            </div>
            
            <h3 style="margin-bottom: 20px; color: #333;">${question}</h3>
            <p style="color: #666; margin-bottom: 20px; font-style: italic;">Take your time to think deeply about their perspective...</p>
            
            <textarea id="empathy-answer" placeholder="Think deeply about their perspective..." style="width: 100%; height: 120px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
            
            <button onclick="submitCurrentAnswer()" style="width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">
                ${progress < 8 ? 'Continue to Next Question' : 'Create My Empathy Map'}
            </button>
        </div>
    `;
}

function submitCurrentAnswer() {
    const answer = document.getElementById('empathy-answer').value.trim();
    
    if (!answer) {
        alert('Please provide an answer before continuing.');
        return;
    }
    
    // Save the answer
    const questionIndex = empathyJourney.currentQuestion;
    empathyJourney.responses.push({
        question: empathyJourney.questions[questionIndex],
        category: empathyJourney.categories[questionIndex],
        answer: answer
    });
    
    console.log(`Question ${questionIndex + 1} answered:`, answer);
    
    // Move to next question or finish
    empathyJourney.currentQuestion++;
    
    if (empathyJourney.currentQuestion < 8) {
        // Show next question
        displayCurrentQuestion();
    } else {
        // All questions done - create the map
        createEmpathyMap();
    }
}

function createEmpathyMap() {
    const content = document.getElementById('empathy-content');
    
    // Show loading
    content.innerHTML = '<div style="text-align: center; padding: 40px;"><h3>🧠 Creating your empathy map...</h3><p>Analyzing all 8 responses...</p></div>';
    
    // Simulate processing time
    setTimeout(() => {
        displayEmpathyResults();
    }, 2000);
}

function displayEmpathyResults() {
    const content = document.getElementById('empathy-content');
    const person = empathyJourney.personData.person_name;
    const goal = empathyJourney.personData.conversation_goal;
    
    // Simple analysis based on responses
    const hopesAnswers = empathyJourney.responses.slice(0, 3).map(r => r.answer).join(' ');
    const fearsAnswers = empathyJourney.responses.slice(3, 6).map(r => r.answer).join(' ');
    const influenceAnswers = empathyJourney.responses.slice(6, 8).map(r => r.answer).join(' ');
    
    content.innerHTML = `
        <div style="text-align: left;">
            <h2 style="color: #28a745; text-align: center; margin-bottom: 20px;">🗺️ Empathy Map: ${person}</h2>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #495057; margin-bottom: 15px;">🎯 Your Conversation Goal:</h4>
                <p style="font-style: italic;">${goal}</p>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #155724; margin-bottom: 15px;">💚 HOPES & VALUES</h4>
                <p style="font-size: 14px; line-height: 1.5;">${hopesAnswers}</p>
            </div>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #856404; margin-bottom: 15px;">😰 FEARS & ANXIETIES</h4>
                <p style="font-size: 14px; line-height: 1.5;">${fearsAnswers}</p>
            </div>
            
            <div style="background: #cce5ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #004085; margin-bottom: 15px;">🌍 EXTERNAL INFLUENCES</h4>
                <p style="font-size: 14px; line-height: 1.5;">${influenceAnswers}</p>
            </div>
            
            <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #155724; margin-bottom: 15px;">💡 KEY INSIGHT:</h4>
                <p style="font-style: italic;">Understanding ${person}'s perspective will help you approach this conversation with empathy and find common ground.</p>
            </div>
            
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px;">
                <button onclick="showConversationTips()" style="flex: 1; padding: 12px; background: #28a745; color: white; border: none; border-radius: 10px; cursor: pointer;">
                    💬 Get Conversation Tips
                </button>
                <button onclick="exitEmpathyMap()" style="flex: 1; padding: 12px; background: #6c757d; color: white; border: none; border-radius: 10px; cursor: pointer;">
                    Complete Journey
                </button>
            </div>
        </div>
    `;
}

function showConversationTips() {
    const content = document.getElementById('empathy-content');
    const person = empathyJourney.personData.person_name;
    const goal = empathyJourney.personData.conversation_goal;
    
    // Analyze user's responses to create personalized tips
    const hopesText = empathyJourney.responses.slice(0, 3).map(r => r.answer).join(' ').toLowerCase();
    const fearsText = empathyJourney.responses.slice(3, 6).map(r => r.answer).join(' ').toLowerCase();
    const influenceText = empathyJourney.responses.slice(6, 8).map(r => r.answer).join(' ').toLowerCase();
    
    // Generate personalized empathy-first approach
    let empathyOpener = `"${person}, I know you want what's best for me, and I really value your concern about`;
    
    if (fearsText.includes('money') || fearsText.includes('financial') || fearsText.includes('stable') || fearsText.includes('secure')) {
        empathyOpener += ' my financial security and stability';
    } else if (fearsText.includes('future') || fearsText.includes('success') || fearsText.includes('career')) {
        empathyOpener += ' my future and career success';
    } else if (fearsText.includes('safe') || fearsText.includes('risk') || fearsText.includes('danger')) {
        empathyOpener += ' keeping me safe and secure';
    } else if (fearsText.includes('disappoint') || fearsText.includes('proud') || fearsText.includes('approval')) {
        empathyOpener += ' wanting me to make you proud';
    } else {
        empathyOpener += ' my wellbeing and future happiness';
    }
    empathyOpener += '..."';
    
    // Generate personalized talking points based on their fears
    let talkingPoints = [];
    
    if (fearsText.includes('money') || fearsText.includes('financial')) {
        talkingPoints.push('Show specific research on financial prospects and earning potential');
        talkingPoints.push('Present a detailed financial plan or budget');
    }
    
    if (fearsText.includes('waste') || fearsText.includes('talent') || fearsText.includes('potential')) {
        talkingPoints.push('Explain how this decision actually maximizes your potential');
        talkingPoints.push('Show how your talents align with this new direction');
    }
    
    if (fearsText.includes('family') || fearsText.includes('what people') || influenceText.includes('others')) {
        talkingPoints.push('Address concerns about what others will think');
        talkingPoints.push('Emphasize that this is about your authentic path');
    }
    
    if (fearsText.includes('struggle') || fearsText.includes('difficult') || fearsText.includes('hard')) {
        talkingPoints.push('Acknowledge the challenges while showing your preparation');
        talkingPoints.push('Share your backup plans and risk mitigation strategies');
    }
    
    // Default talking points if none specific were detected
    if (talkingPoints.length < 2) {
        talkingPoints = [
            'Address their main concerns with specific examples',
            'Show how your decision aligns with their core values',
            'Provide concrete evidence of your preparation',
            'Ask for their advice and input on your plan'
        ];
    }
    
    // Generate personalized bridge building based on hopes
    let bridgeText = 'Focus on what you both want: ';
    if (hopesText.includes('happy') || hopesText.includes('happiness')) {
        bridgeText += 'your genuine happiness and fulfillment';
    } else if (hopesText.includes('successful') || hopesText.includes('success')) {
        bridgeText += 'your success and achievement';
    } else if (hopesText.includes('secure') || hopesText.includes('stable')) {
        bridgeText += 'your security and stability';
    } else if (hopesText.includes('proud') || hopesText.includes('respect')) {
        bridgeText += 'something you can both be proud of';
    } else {
        bridgeText += 'your wellbeing and future success';
    }
    bridgeText += '. The conversation is about finding the best path forward together.';
    
    content.innerHTML = `
        <div style="text-align: left;">
            <h2 style="color: #28a745; text-align: center; margin-bottom: 20px;">💬 Your Personalized Conversation Strategy</h2>
            
            <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="color: #155724; margin-bottom: 15px;">🎯 Empathy-First Opening:</h4>
                <p style="line-height: 1.6; font-style: italic; font-size: 16px;">
                    ${empathyOpener}
                </p>
                <small style="color: #666;">This acknowledges their specific concerns from your empathy map.</small>
            </div>
            
            <div style="background: #e2e3e5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="margin-bottom: 15px;">📋 Your Key Talking Points:</h4>
                <ul style="line-height: 1.8;">
                    ${talkingPoints.map(point => `<li>${point}</li>`).join('')}
                </ul>
                <small style="color: #666;">Based on their specific fears and concerns you identified.</small>
            </div>
            
            <div style="background: #cce5ff; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="color: #004085; margin-bottom: 15px;">🤝 Bridge Building:</h4>
                <p style="line-height: 1.6;">
                    ${bridgeText}
                </p>
            </div>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h4 style="color: #856404; margin-bottom: 15px;">⚠️ Prepare For:</h4>
                <p style="line-height: 1.6;">
                    They may bring up <strong>${fearsText.includes('money') ? 'financial concerns' : fearsText.includes('future') ? 'future uncertainty' : fearsText.includes('family') ? 'family expectations' : 'their main worries'}</strong>. 
                    Respond by validating their concern first: <em>"I understand why that worries you..."</em> then present your thoughtful response.
                </p>
            </div>
            
            <button onclick="exitEmpathyMap()" style="width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">
                Ready for the Conversation with ${person}! 🗺️
            </button>
        </div>
    `;
}

function exitEmpathyMap() {
    document.getElementById('empathy-interface').style.display = 'none';
    document.getElementById('main-interface').style.display = 'block';
    
    // Reset everything
    empathyJourney = {
        stage: 'setup',
        personData: {},
        responses: [],
        currentQuestion: 0,
        questions: empathyJourney.questions,
        categories: empathyJourney.categories
    };
}

 // =============================================================================
// FEATURE 4: FUTURE SELF SIMULATOR
// =============================================================================


async function startFutureSelf() {
    console.log('Starting Future Self Simulator...');
    
    // Hide main interface, show future interface
    document.getElementById('main-interface').style.display = 'none';
    
    // Create and show future interface
    if (!document.getElementById('future-interface')) {
        const futureHTML = `
            <div id="future-interface" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; z-index: 2000;">
                <button onclick="exitFutureSelf()" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer;">✕ Exit</button>
                <div id="future-content" style="max-width: 700px; max-height: 80vh; background: white; padding: 40px; border-radius: 20px; text-align: center; overflow-y: auto;"></div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', futureHTML);
    }
    
    document.getElementById('future-interface').style.display = 'flex';
    
    // Show the demo content
    const content = document.getElementById('future-content');
    content.innerHTML = `
        <div style="text-align: center;">
            <h2 style="color: #6f42c1; margin-bottom: 20px;">⏳ Future Self Simulator</h2>
            
            <div style="background: linear-gradient(135deg, #6f42c1, #e83e8c); color: white; padding: 30px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: white; margin-bottom: 20px;">🌟 Experience Your Future Life</h3>
                <p style="line-height: 1.6;">Imagine waking up in your dream life, living as your ideal future self. This simulator creates a vivid, personalized "day in the life" experience to boost your motivation and clarity.</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: left;">
                <h4 style="margin-bottom: 20px; text-align: center;">🎬 Sample Future Day Experience:</h4>
                <p style="line-height: 1.8; font-style: italic;">
                    "The morning light streams into your dream workspace. As you prepare for another fulfilling day as a <strong>successful professional</strong>, you feel <strong>confident, purposeful, and excited</strong>. 
                    <br><br>
                    Your daily ritual of <strong>morning meditation</strong> grounds you before tackling meaningful work. The skill you've mastered - <strong>public speaking</strong> - now comes naturally as you prepare for today's important presentation.
                    <br><br>
                    This is the life you built through consistent, intentional choices. Every challenge you face now is one you <em>chose</em> to face, because it aligns with your authentic self and your vision."
                </p>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #155724;">🎯 How It Works:</h4>
                <ul style="text-align: left; line-height: 1.6;">
                    <li><strong>5 Guided Questions:</strong> About your future identity, environment, and goals</li>
                    <li><strong>AI Story Generation:</strong> Creates a personalized "day in your life" narrative</li>
                    <li><strong>Immersive Experience:</strong> Rich, sensory details make it feel real</li>
                    <li><strong>Action Bridge:</strong> Connects your vision to concrete next steps</li>
                </ul>
            </div>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #856404;">💡 Why This Works:</h4>
                <p style="text-align: left; line-height: 1.6;">
                    Your brain can't distinguish between a vividly imagined experience and reality. 
                    By "experiencing" your future success, you create powerful neural pathways that boost motivation and make your goals feel achievable.
                </p>
            </div>
            
            <button onclick="startFutureQuestions()" style="width: 100%; padding: 15px; background: linear-gradient(45deg, #6f42c1, #e83e8c); color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; margin-top: 20px;">
    🚀 Start My Future Simulation!
</button>

        </div>
    `;
}

function exitFutureSelf() {
    if (document.getElementById('future-interface')) {
        document.getElementById('future-interface').style.display = 'none';
    }
    document.getElementById('main-interface').style.display = 'block';
}

function startFutureQuestions() {
    const content = document.getElementById('future-content');
    
    content.innerHTML = `
        <div style="text-align: center;">
            <h2 style="color: #6f42c1; margin-bottom: 20px;">⏳ Future Self Builder</h2>
            <p style="color: #666; margin-bottom: 30px;">Answer 5 questions to create your personalized future day</p>
            
            <div id="question-container" style="background: #f8f9fa; padding: 30px; border-radius: 15px; margin: 20px 0; text-align: left;">
                <h3 style="margin-bottom: 15px;">Question 1 of 5:</h3>
                <p style="font-weight: bold; margin-bottom: 15px;">Let's start with the big picture. In one sentence, describe the future self you're working towards.</p>
                <textarea id="future-q1" placeholder="e.g., A successful freelance photographer living in Tokyo, specializing in street fashion" style="width: 100%; height: 100px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
                
                <button onclick="
                    const answer = document.getElementById('future-q1').value.trim();
                    if (!answer) { alert('Please provide an answer!'); return; }
                    window.futureAnswers = [answer];
                    document.getElementById('question-container').innerHTML = \`
                        <h3>Question 2 of 5:</h3>
                        <p style='font-weight: bold; margin-bottom: 15px;'>Where is this future you? Describe the vibe of your home or workspace.</p>
                        <textarea id='future-q2' placeholder='e.g., A small, minimalist apartment with large windows and organized equipment' style='width: 100%; height: 100px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;'></textarea>
                        <button onclick='nextToQ3()' style='width: 100%; padding: 15px; background: #6f42c1; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;'>Continue →</button>
                    \`;
                " style="width: 100%; padding: 15px; background: #6f42c1; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">
                    Continue →
                </button>
            </div>
        </div>
    `;
}

function nextToQ3() {
    const answer = document.getElementById('future-q2').value.trim();
    if (!answer) { alert('Please provide an answer!'); return; }
    window.futureAnswers.push(answer);
    
    document.getElementById('question-container').innerHTML = `
        <h3>Question 3 of 5:</h3>
        <p style="font-weight: bold; margin-bottom: 15px;">What three words best describe the feeling of your ideal day?</p>
        <textarea id="future-q3" placeholder="e.g., Creative, Independent, Inspired" style="width: 100%; height: 100px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
        <button onclick="nextToQ4()" style="width: 100%; padding: 15px; background: #6f42c1; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">Continue →</button>
    `;
}

function nextToQ4() {
    const answer = document.getElementById('future-q3').value.trim();
    if (!answer) { alert('Please provide an answer!'); return; }
    window.futureAnswers.push(answer);
    
    document.getElementById('question-container').innerHTML = `
        <h3>Question 4 of 5:</h3>
        <p style="font-weight: bold; margin-bottom: 15px;">Beyond work, what's a small, meaningful activity that's part of your daily routine?</p>
        <textarea id="future-q4" placeholder="e.g., Starting my day with a quiet hour at a local coffee shop" style="width: 100%; height: 100px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
        <button onclick="nextToQ5()" style="width: 100%; padding: 15px; background: #6f42c1; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">Continue →</button>
    `;
}

function nextToQ5() {
    const answer = document.getElementById('future-q4').value.trim();
    if (!answer) { alert('Please provide an answer!'); return; }
    window.futureAnswers.push(answer);
    
    document.getElementById('question-container').innerHTML = `
        <h3>Question 5 of 5:</h3>
        <p style="font-weight: bold; margin-bottom: 15px;">What is one skill you've mastered in this future that you're proud of?</p>
        <textarea id="future-q5" placeholder="e.g., I've become fluent in conversational Japanese" style="width: 100%; height: 100px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
        <button onclick="generateMyFuture()" style="width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">Generate My Future! ✨</button>
    `;
}

function generateMyFuture() {
    const answer = document.getElementById('future-q5').value.trim();
    if (!answer) { alert('Please provide an answer!'); return; }
    window.futureAnswers.push(answer);
    
    const [identity, environment, feelings, rituals, skill] = window.futureAnswers;
    
    // Create more sophisticated, personalized story
    const content = document.getElementById('future-content');
    content.innerHTML = `
        <div style="text-align: center;">
            <h2 style="color: #6f42c1; margin-bottom: 20px;">✨ A Day in Your Future Life</h2>
            <p style="color: #666; font-style: italic; margin-bottom: 30px; font-size: 18px;">${identity}</p>
            
            <div style="background: linear-gradient(135deg, #6f42c1, #e83e8c); color: white; padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: white; margin-bottom: 15px;">🎬 6:30 AM - Your Day Begins...</h3>
            </div>
            
            <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; margin: 20px 0; line-height: 1.8; text-align: left; font-size: 16px;">
                <p><strong>Morning:</strong> You wake up naturally in ${environment.toLowerCase()}. The first thing you notice is how <strong>${feelings.toLowerCase()}</strong> you feel - not the rushed anxiety of your old life, but a deep sense of alignment. You've built something real.</p>
                
                <p><strong>Your Ritual:</strong> ${rituals} has become more than routine - it's your anchor. During this time, you plan your day with intention rather than reacting to chaos. Today feels full of possibility.</p>
                
                <p><strong>Mid-Morning:</strong> As you prepare for work, you catch your reflection and smile. Remember when <strong>${skill.toLowerCase()}</strong> seemed impossible? Now it's second nature. That transformation didn't happen overnight - it was built through countless small choices.</p>
                
                <p><strong>Work Begins:</strong> Your work as <strong>${identity.toLowerCase()}</strong> doesn't feel like "work" anymore. There are challenges, yes, but they're the right challenges. You chose this struggle because it's aligned with who you really are.</p>
                
                <p><strong>Afternoon Reflection:</strong> Taking a brief break, you remember your younger self worrying about the future. If only they could see you now - not because everything is perfect, but because you're finally living authentically.</p>
                
                <p><strong>Evening Wind-Down:</strong> As the day ends, you feel that deep satisfaction that comes from living in alignment. Tomorrow will bring new challenges, but you'll face them as the person you've become - <strong>${feelings.toLowerCase()}</strong> and purposeful.</p>
                
                <p style="font-style: italic; margin-top: 20px; padding: 20px; background: rgba(111, 66, 193, 0.1); border-radius: 10px;"><strong>The Truth:</strong> This isn't a fantasy. Every element of this day is achievable. The person living this life made it real through consistent, intentional choices - exactly the kind you're capable of making starting today.</p>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #155724; margin-bottom: 15px;">🎯 Your Next Move</h4>
                <p>The gap between your current life and this future isn't a chasm - it's a series of small, intentional steps. What's one thing you could do this week to move 1% closer to this reality?</p>
            </div>
            
            <button onclick="showActionPlanning()" style="width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer; margin: 10px 0;">
                📋 Plan My First Step
            </button>
            
            <button onclick="exitFutureSelf()" style="width: 100%; padding: 12px; background: linear-gradient(45deg, #6f42c1, #e83e8c); color: white; border: none; border-radius: 10px; font-size: 14px; cursor: pointer;">
                🚀 I'm Ready to Build This Future!
            </button>
        </div>
    `;
}

function showActionPlanning() {
    const [identity, environment, feelings, rituals, skill] = window.futureAnswers;
    const content = document.getElementById('future-content');
    
    content.innerHTML = `
        <div style="text-align: left;">
            <h2 style="color: #6f42c1; text-align: center; margin-bottom: 20px;">📋 Your Action Plan</h2>
            
            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #856404; margin-bottom: 15px;">💡 Bridge the Gap</h4>
                <p style="line-height: 1.6;">
                    The future you just experienced isn't magic - it's the result of aligned actions. 
                    Let's identify your first concrete step toward becoming <strong>${identity.toLowerCase()}</strong>.
                </p>
            </div>
            
            <h3 style="margin-bottom: 15px;">What's one specific action you can take this week?</h3>
            <p style="color: #666; margin-bottom: 15px;">Make it concrete and measurable:</p>
            
            <textarea id="commitment-input" placeholder="Examples: 
• Research 3 companies where I'd want to work as ${identity.toLowerCase()}
• Practice ${skill.toLowerCase()} for 20 minutes daily
• Set up ${rituals.toLowerCase()} routine every morning this week
• Reach out to one person already doing what I want to do" style="width: 100%; height: 120px; padding: 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 16px; margin-bottom: 20px; resize: vertical;"></textarea>
            
            <button onclick="finalizeCommitment()" style="width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">
                ✅ Lock in My Commitment
            </button>
        </div>
    `;
}

function finalizeCommitment() {
    const commitment = document.getElementById('commitment-input').value.trim();
    
    if (!commitment) {
        alert('Please enter your specific first step!');
        return;
    }
    
    const [identity] = window.futureAnswers;
    const content = document.getElementById('future-content');
    
    content.innerHTML = `
        <div style="text-align: center;">
            <h2 style="color: #28a745; margin-bottom: 20px;">🎉 Your Future Journey Begins Now!</h2>
            
            <div style="background: #d4edda; padding: 30px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: #155724; margin-bottom: 15px;">✅ Your Week 1 Commitment:</h3>
                <p style="font-size: 18px; font-weight: bold; line-height: 1.6; font-style: italic;">
                    "${commitment}"
                </p>
            </div>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: left;">
                <h4 style="color: #155724; margin-bottom: 15px;">🔥 Success Strategy:</h4>
                <ul style="line-height: 1.8; padding-left: 20px;">
                    <li><strong>Start tomorrow</strong> - momentum beats perfection</li>
                    <li><strong>Track daily progress</strong> - small wins compound</li>
                    <li><strong>Revisit this vision</strong> when motivation dips</li>
                    <li><strong>Adjust, don't abandon</strong> - flexibility is strength</li>
                </ul>
            </div>
            
            <div style="background: #cce5ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p style="color: #004085; line-height: 1.6; font-size: 16px;">
                    <strong>Remember:</strong> The future you experienced isn't just possible - it's inevitable if you stay committed to growth. 
                    Every day you choose progress over comfort, you're choosing to become that person.
                </p>
            </div>
            
            <button onclick="exitFutureSelf()" style="width: 100%; padding: 15px; background: linear-gradient(45deg, #6f42c1, #e83e8c); color: white; border: none; border-radius: 10px; font-size: 16px; cursor: pointer;">
                ⏳ Ready to Build My Future!
            </button>
        </div>
    `;
}

// =============================================================================
// FEATURE 5 JAVASCRIPT: DIALOGUE GYM FUNCTIONS
// =============================================================================
function showDialogueGymUI() {
    console.log('Opening Dialogue Gym UI...');
    
    // Hide main interface
    document.getElementById('main-interface').style.display = 'none';
    
    // Create dialogue gym interface
    if (!document.getElementById('dialogue-gym-ui')) {
        const dialogueHTML = `
            <div id="dialogue-gym-ui" style="position: fixed; top: 0; left: 0; width: 100%; height: 100vh; background: linear-gradient(135deg, #17a2b8 0%, #007bff 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; z-index: 2000;">
                <button onclick="closeDialogueGym()" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer;">✕ Exit</button>
                
                <div id="dialogue-gym-content" style="max-width: 900px; max-height: 85vh; background: white; padding: 40px; border-radius: 20px; text-align: center; overflow-y: auto;">
                    <!-- Content will be loaded here -->
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', dialogueHTML);
    }
    
    document.getElementById('dialogue-gym-ui').style.display = 'flex';
    
    // Load the main zones view
    showMainZones();
}

function showMainZones() {
    const content = document.getElementById('dialogue-gym-content');
    
    content.innerHTML = `
        <h1 style="color: #17a2b8; margin-bottom: 10px;">💬 Dialogue Gym</h1>
        <p style="color: #666; margin-bottom: 30px; font-size: 18px;">Practice social conversations in a safe, judgment-free environment</p>
        
        <div style="background: linear-gradient(135deg, #17a2b8, #007bff); color: white; padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h2 style="color: white; margin-bottom: 15px;">🏋️ Choose Your Workout Zone</h2>
            <p style="line-height: 1.6; font-size: 16px;">Each zone focuses on specific social skills to build your confidence</p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0;">
            
            <div onclick="selectDialogueZone('assertiveness')" style="background: #f8f9fa; padding: 25px; border-radius: 15px; cursor: pointer; border: 3px solid transparent; transition: all 0.3s; text-align: left;" onmouseover="this.style.borderColor='#17a2b8'; this.style.background='#e8f4fd';" onmouseout="this.style.borderColor='transparent'; this.style.background='#f8f9fa';">
                <h3 style="color: #17a2b8; margin-bottom: 10px;">🛡️ Assertiveness Zone</h3>
                <p style="color: #666; line-height: 1.5; margin-bottom: 10px;">Learn to set boundaries and say "no" with confidence and kindness</p>
                <div style="color: #28a745; font-weight: bold;">2 Practice Scenarios</div>
                <small style="color: #6c757d;">• Declining money requests • Setting personal boundaries</small>
            </div>
            
            <div onclick="selectDialogueZone('reaching_out')" style="background: #f8f9fa; padding: 25px; border-radius: 15px; cursor: pointer; border: 3px solid transparent; transition: all 0.3s; text-align: left;" onmouseover="this.style.borderColor='#17a2b8'; this.style.background='#e8f4fd';" onmouseout="this.style.borderColor='transparent'; this.style.background='#f8f9fa';">
                <h3 style="color: #17a2b8; margin-bottom: 10px;">🤝 Reaching Out Zone</h3>
                <p style="color: #666; line-height: 1.5; margin-bottom: 10px;">Practice asking for help, support, and extensions professionally</p>
                <div style="color: #28a745; font-weight: bold;">3 Practice Scenarios</div>
                <small style="color: #6c757d;">• Email professors • Ask for mental health days • Request help from friends</small>
            </div>
            
            <div onclick="selectDialogueZone('social_connection')" style="background: #f8f9fa; padding: 25px; border-radius: 15px; cursor: pointer; border: 3px solid transparent; transition: all 0.3s; text-align: left;" onmouseover="this.style.borderColor='#17a2b8'; this.style.background='#e8f4fd';" onmouseout="this.style.borderColor='transparent'; this.style.background='#f8f9fa';">
                <h3 style="color: #17a2b8; margin-bottom: 10px;">👥 Social Connection Zone</h3>
                <p style="color: #666; line-height: 1.5; margin-bottom: 10px;">Build friendships through small talk and meaningful connections</p>
                <div style="color: #28a745; font-weight: bold;">4 Practice Scenarios</div>
                <small style="color: #6c757d;">• Classmate conversations • Party introductions • Following up with new friends</small>
            </div>
            
            <div onclick="selectDialogueZone('heart_to_heart')" style="background: #f8f9fa; padding: 25px; border-radius: 15px; cursor: pointer; border: 3px solid transparent; transition: all 0.3s; text-align: left;" onmouseover="this.style.borderColor='#17a2b8'; this.style.background='#e8f4fd';" onmouseout="this.style.borderColor='transparent'; this.style.background='#f8f9fa';">
                <h3 style="color: #17a2b8; margin-bottom: 10px;">💖 Heart-to-Heart Zone</h3>
                <p style="color: #666; line-height: 1.5; margin-bottom: 10px;">Practice vulnerable conversations and emotional disclosure</p>
                <div style="color: #28a745; font-weight: bold;">3 Practice Scenarios</div>
                <small style="color: #6c757d;">• Mental health disclosure • Meaningful apologies • Parent conversations</small>
            </div>
            
        </div>
        
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin: 25px 0; text-align: left;">
            <h3 style="color: #004085; margin-bottom: 15px;">💡 How The Dialogue Gym Works:</h3>
            <div style="color: #666; line-height: 1.7;">
                <p><strong>1. Choose Your Challenge:</strong> Pick a zone that matches your current social skill goals</p>
                <p><strong>2. Select a Scenario:</strong> Practice realistic situations you might actually encounter</p>
                <p><strong>3. Have Real Conversations:</strong> Chat with AI partners who stay in character</p>
                <p><strong>4. Get Live Coaching:</strong> Receive immediate feedback on your communication style</p>
                <p><strong>5. Build Confidence:</strong> Repeat scenarios until social interactions feel natural</p>
            </div>
        </div>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <p style="color: #856404; margin: 0;"><strong>🎯 Pro Tip:</strong> Start with easier scenarios and work your way up to build confidence gradually</p>
        </div>
    `;
}

function showDialogueZones() {
    // Go back to the main zones view
    showMainZones();
}

function selectDialogueZone(zone) {
    const zoneNames = {
        'assertiveness': '🛡️ Assertiveness Zone - Practice setting boundaries',
        'reaching_out': '🤝 Reaching Out Zone - Practice asking for help',
        'social_connection': '👥 Social Connection Zone - Practice building friendships', 
        'heart_to_heart': '💖 Heart-to-Heart Zone - Practice vulnerable conversations'
    };
    
    const scenarioCounts = {
        'assertiveness': '2 scenarios: Declining money requests, Setting personal boundaries',
        'reaching_out': '3 scenarios: Email professors, Ask for mental health days, Request help from friends',
        'social_connection': '4 scenarios: Classmate conversations, Party introductions, Following up with new friends, Making plans',
        'heart_to_heart': '3 scenarios: Mental health disclosure, Meaningful apologies, Parent conversations'
    };
    
    // Get scenario buttons based on zone
    const scenarioButtons = {
        'assertiveness': `
            <button onclick="startAssertiveness1Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                💰 <strong>Decline Money Request</strong><br>
                <small style="opacity: 0.9;">Practice saying no to a friend asking to borrow money</small>
            </button>
            <button onclick="startAssertiveness2Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                🚫 <strong>Set Personal Boundaries</strong><br>
                <small style="opacity: 0.9;">Practice responding to family criticism about your choices</small>
            </button>
        `,
        'reaching_out': `
            <button onclick="startProfessorChat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                📧 <strong>Email Professor for Extension</strong><br>
                <small style="opacity: 0.9;">Practice requesting academic deadline extensions professionally</small>
            </button>
            <button onclick="startManagerChat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                🧠 <strong>Request Mental Health Day</strong><br>
                <small style="opacity: 0.9;">Practice asking for mental health time off from work</small>
            </button>
            <button onclick="startFriendChat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                💬 <strong>Ask Friend for Emotional Support</strong><br>
                <small style="opacity: 0.9;">Practice reaching out to friends when you need support</small>
            </button>
        `,
        'social_connection': `
            <button onclick="startSocial1Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                👋 <strong>Small Talk with Classmate</strong><br>
                <small style="opacity: 0.9;">Practice casual conversation before class starts</small>
            </button>
            <button onclick="startSocial2Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                🎉 <strong>Join Party Conversation</strong><br>
                <small style="opacity: 0.9;">Practice approaching groups at social gatherings</small>
            </button>
            <button onclick="startSocial3Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                📱 <strong>Follow Up with New Friend</strong><br>
                <small style="opacity: 0.9;">Practice suggesting plans with someone you recently met</small>
            </button>
            <button onclick="startSocial4Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                🤝 <strong>Deepen Acquaintanceship</strong><br>
                <small style="opacity: 0.9;">Practice turning casual acquaintances into real friends</small>
            </button>
        `,
        'heart_to_heart': `
            <button onclick="startHeart1Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                🧠 <strong>Mental Health Disclosure</strong><br>
                <small style="opacity: 0.9;">Practice sharing your mental health struggles with a close friend</small>
            </button>
            <button onclick="startHeart2Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                🙏 <strong>Make a Meaningful Apology</strong><br>
                <small style="opacity: 0.9;">Practice taking responsibility and apologizing sincerely</small>
            </button>
            <button onclick="startHeart3Chat()" style="background: #17a2b8; color: white; padding: 15px 20px; border: none; border-radius: 8px; cursor: pointer; text-align: left; margin-bottom: 10px;">
                👨‍👩‍👧‍👦 <strong>Parent Life Decision Talk</strong><br>
                <small style="opacity: 0.9;">Practice discussing major life choices with your parents</small>
            </button>
        `
    };
    
    // Update content
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <h1 style="color: #17a2b8; margin-bottom: 10px;">${zoneNames[zone]}</h1>
        <p style="color: #666; margin-bottom: 20px; font-size: 16px;">${scenarioCounts[zone]}</p>
        
        <button onclick="showMainZones()" style="background: #6c757d; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 25px;">← Back to All Zones</button>
        
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #856404; margin-bottom: 15px;">📋 Available Scenarios:</h3>
            <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">${scenarioCounts[zone]}</p>
            
            <!-- SCENARIO BUTTONS -->
            <div style="display: flex; flex-direction: column;">
                ${scenarioButtons[zone] || '<p>Scenarios coming soon!</p>'}
            </div>
        </div>
        
        <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #004085; margin-bottom: 15px;">🎯 Coming Soon:</h3>
            <ul style="color: #666; line-height: 1.6; text-align: left;">
                <li>Interactive AI conversation partners</li>
                <li>Real-time coaching feedback</li>
                <li>Performance tracking and analysis</li>
                <li>Personalized difficulty progression</li>
            </ul>
        </div>
    `;
}


function closeDialogueGym() {
    if (document.getElementById('dialogue-gym-ui')) {
        document.getElementById('dialogue-gym-ui').style.display = 'none';
    }
    document.getElementById('main-interface').style.display = 'block';
}

// =============================================================================
// ASSERTIVENESS ZONE CHAT FUNCTIONS
// =============================================================================

let assertivenessStep = 0;

function startAssertiveness1Chat() {
    assertivenessStep = 0;
    showAssertiveness1UI();
}

function startAssertiveness2Chat() {
    assertivenessStep = 0;
    showAssertiveness2UI();
}

function showAssertiveness1UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">💰 Decline Money Request</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice saying no to a friend asking to borrow money</p>
            </div>
            <div id="assertiveness1Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Your Friend</div>
                        <div style="color: #495057;">Hey! I'm in a really tight spot right now. Could you possibly lend me $200? I promise I'll pay you back next month.</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="assertiveness1Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToAssertiveness1()">
                <button onclick="sendToAssertiveness1()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitAssertiveness1Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToAssertiveness1() {
    const input = document.getElementById('assertiveness1Input');
    const message = input.value.trim();
    if (!message) return;
    
    addAssertiveness1Message(message, 'user');
    
    setTimeout(() => {
        const response = getAssertiveness1Response(assertivenessStep);
        addAssertiveness1Message(response, 'ai');
        assertivenessStep++;
    }, 1000);
    
    input.value = '';
}

function addAssertiveness1Message(message, sender) {
    const messagesDiv = document.getElementById('assertiveness1Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Your Friend';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getAssertiveness1Response(step) {
    const responses = [
        "I understand that you're stressed, but is there any way? Even just $100?",
        "Come on, we're friends! I really wouldn't ask if it wasn't important.",
        "Okay, I get it. Thanks for being honest with me.",
        "I appreciate you being upfront. No hard feelings!"
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitAssertiveness1Chat() {
    showChatComplete('💰 Money Request Chat', 'You set boundaries kindly while preserving the friendship!');
}

function showAssertiveness2UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">🚫 Set Personal Boundaries</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice responding to family criticism about your choices</p>
            </div>
            <div id="assertiveness2Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Family Member</div>
                        <div style="color: #495057;">I just don't understand why you're wasting your potential on this path. You could be doing so much better.</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="assertiveness2Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToAssertiveness2()">
                <button onclick="sendToAssertiveness2()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitAssertiveness2Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToAssertiveness2() {
    const input = document.getElementById('assertiveness2Input');
    const message = input.value.trim();
    if (!message) return;
    
    addAssertiveness2Message(message, 'user');
    
    setTimeout(() => {
        const response = getAssertiveness2Response(assertivenessStep);
        addAssertiveness2Message(response, 'ai');
        assertivenessStep++;
    }, 1000);
    
    input.value = '';
}

function addAssertiveness2Message(message, sender) {
    const messagesDiv = document.getElementById('assertiveness2Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Family Member';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getAssertiveness2Response(step) {
    const responses = [
        "I'm just trying to look out for you. This path seems risky.",
        "I understand your point, but I still think you're making a mistake.",
        "Well, I hope you know what you're doing.",
        "I respect your decision, even if I don't fully understand it."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitAssertiveness2Chat() {
    showChatComplete('🚫 Boundary Setting Chat', 'You stood your ground respectfully while maintaining family relationships!');
}

// =============================================================================
// SOCIAL CONNECTION ZONE CHAT FUNCTIONS  
// =============================================================================

let socialStep = 0;

function startSocial1Chat() {
    socialStep = 0;
    showSocial1UI();
}

function startSocial2Chat() {
    socialStep = 0;
    showSocial2UI();
}

function startSocial3Chat() {
    socialStep = 0;
    showSocial3UI();
}

function startSocial4Chat() {
    socialStep = 0;
    showSocial4UI();
}

function showSocial1UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">👋 Small Talk with Classmate</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice casual conversation before class starts</p>
            </div>
            <div id="social1Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Jamie</div>
                        <div style="color: #495057;">Oh hey, you're in my statistics class too, right? How are you finding it so far?</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="social1Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToSocial1()">
                <button onclick="sendToSocial1()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitSocial1Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToSocial1() {
    const input = document.getElementById('social1Input');
    const message = input.value.trim();
    if (!message) return;
    
    addSocial1Message(message, 'user');
    
    setTimeout(() => {
        const response = getSocial1Response(socialStep);
        addSocial1Message(response, 'ai');
        socialStep++;
    }, 1000);
    
    input.value = '';
}

function addSocial1Message(message, sender) {
    const messagesDiv = document.getElementById('social1Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Jamie';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getSocial1Response(step) {
    const responses = [
        "Yeah, I know what you mean! The homework can be pretty intense. Are you finding the professor helpful?",
        "That's great that you're keeping up! I sometimes struggle with the concepts. Do you have any study tips?",
        "Nice! Maybe we could study together sometime? I think it would help both of us.",
        "Awesome! Here's my number - let me know when you want to meet up!"
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitSocial1Chat() {
    showChatComplete('👋 Classmate Chat', 'You built rapport and created a potential study partnership!');
}

// =============================================================================
// HEART-TO-HEART ZONE CHAT FUNCTIONS
// =============================================================================

let heartStep = 0;

function startHeart1Chat() {
    heartStep = 0;
    showHeart1UI();
}

function startHeart2Chat() {
    heartStep = 0;
    showHeart2UI();
}

function startHeart3Chat() {
    heartStep = 0;
    showHeart3UI();
}

function showHeart1UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">🧠 Mental Health Disclosure</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice sharing your mental health struggles with a close friend</p>
            </div>
            <div id="heart1Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Sam</div>
                        <div style="color: #495057;">You seem to have something on your mind lately. Is everything okay?</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="heart1Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToHeart1()">
                <button onclick="sendToHeart1()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitHeart1Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToHeart1() {
    const input = document.getElementById('heart1Input');
    const message = input.value.trim();
    if (!message) return;
    
    addHeart1Message(message, 'user');
    
    setTimeout(() => {
        const response = getHeart1Response(heartStep);
        addHeart1Message(response, 'ai');
        heartStep++;
    }, 1000);
    
    input.value = '';
}

function addHeart1Message(message, sender) {
    const messagesDiv = document.getElementById('heart1Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Sam';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getHeart1Response(step) {
    const responses = [
        "Thank you for trusting me with this. That sounds really tough to deal with.",
        "I'm here for you. How long have you been feeling this way?",
        "You're really brave for sharing this with me. What kind of support would help most?",
        "I care about you and I'm glad you told me. Let's figure out how I can best support you."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitHeart1Chat() {
    showChatComplete('🧠 Mental Health Chat', 'You shared vulnerably and deepened your friendship through trust!');
}

// =============================================================================
// SOCIAL CONNECTION - SCENARIO 2: JOIN PARTY CONVERSATION
// =============================================================================

function showSocial2UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">🎉 Join Party Conversation</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice approaching groups at social gatherings</p>
            </div>
            <div id="social2Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Casey</div>
                        <div style="color: #495057;">...and then the professor said that was the wrong formula entirely! Can you believe it? Oh hey, come join us!</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="social2Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToSocial2()">
                <button onclick="sendToSocial2()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitSocial2Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToSocial2() {
    const input = document.getElementById('social2Input');
    const message = input.value.trim();
    if (!message) return;
    
    addSocial2Message(message, 'user');
    
    setTimeout(() => {
        const response = getSocial2Response(socialStep);
        addSocial2Message(response, 'ai');
        socialStep++;
    }, 1000);
    
    input.value = '';
}

function addSocial2Message(message, sender) {
    const messagesDiv = document.getElementById('social2Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Casey';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getSocial2Response(step) {
    const responses = [
        "Oh wow, that sounds frustrating! Which class was this? I think I know that professor.",
        "Right? Some professors can be so confusing with their explanations. Are you taking other classes this semester?",
        "Nice! We should all hang out sometime. Do you ever go to the campus events?",
        "That sounds fun! Let's exchange numbers and plan something soon!"
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitSocial2Chat() {
    showChatComplete('🎉 Party Chat', 'You smoothly joined the conversation and made new connections!');
}

// =============================================================================
// SOCIAL CONNECTION - SCENARIO 3: FOLLOW UP WITH NEW FRIEND
// =============================================================================

function showSocial3UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">📱 Follow Up with New Friend</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice suggesting plans with someone you recently met</p>
            </div>
            <div id="social3Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Morgan</div>
                        <div style="color: #495057;">Hey! Great meeting you at the coffee shop yesterday. How did your presentation go?</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="social3Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToSocial3()">
                <button onclick="sendToSocial3()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitSocial3Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToSocial3() {
    const input = document.getElementById('social3Input');
    const message = input.value.trim();
    if (!message) return;
    
    addSocial3Message(message, 'user');
    
    setTimeout(() => {
        const response = getSocial3Response(socialStep);
        addSocial3Message(response, 'ai');
        socialStep++;
    }, 1000);
    
    input.value = '';
}

function addSocial3Message(message, sender) {
    const messagesDiv = document.getElementById('social3Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Morgan';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getSocial3Response(step) {
    const responses = [
        "That's awesome! I'm so glad it went well. You seemed a bit nervous about it yesterday.",
        "You totally deserved that! You clearly put a lot of work into it. What's next for you?",
        "That sounds really interesting! I'd love to hear more about it. Want to grab lunch sometime this week?",
        "Perfect! How about Thursday around noon? I know a great place near campus."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitSocial3Chat() {
    showChatComplete('📱 Follow-up Chat', 'You successfully turned a new acquaintance into plans for deeper friendship!');
}

// =============================================================================
// SOCIAL CONNECTION - SCENARIO 4: DEEPEN ACQUAINTANCESHIP
// =============================================================================

function showSocial4UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">🤝 Deepen Acquaintanceship</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice turning casual acquaintances into real friends</p>
            </div>
            <div id="social4Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Riley</div>
                        <div style="color: #495057;">Hey! I keep running into you everywhere. How's your week going?</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="social4Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToSocial4()">
                <button onclick="sendToSocial4()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitSocial4Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToSocial4() {
    const input = document.getElementById('social4Input');
    const message = input.value.trim();
    if (!message) return;
    
    addSocial4Message(message, 'user');
    
    setTimeout(() => {
        const response = getSocial4Response(socialStep);
        addSocial4Message(response, 'ai');
        socialStep++;
    }, 1000);
    
    input.value = '';
}

function addSocial4Message(message, sender) {
    const messagesDiv = document.getElementById('social4Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Riley';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getSocial4Response(step) {
    const responses = [
        "I know, right? It's like we're on the same schedule! That sounds really cool, what kind of hobbies are you into?",
        "Oh wow, that's awesome! I've always wanted to try that. Do you think a beginner could join you sometime?",
        "That sounds amazing! I'd love to learn. When do you usually do that?",
        "Count me in! This sounds like the start of a great friendship!"
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitSocial4Chat() {
    showChatComplete('🤝 Friendship Building Chat', 'You deepened the relationship by sharing interests and making plans!');
}

// =============================================================================
// HEART-TO-HEART ZONE - SCENARIOS 2 & 3
// =============================================================================

// SCENARIO 2: MEANINGFUL APOLOGY
function showHeart2UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">🙏 Make a Meaningful Apology</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice taking responsibility and apologizing sincerely</p>
            </div>
            <div id="heart2Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Jordan</div>
                        <div style="color: #495057;">I got your message saying you wanted to talk. I have to say, I'm still pretty hurt about what happened.</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="heart2Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToHeart2()">
                <button onclick="sendToHeart2()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitHeart2Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToHeart2() {
    const input = document.getElementById('heart2Input');
    const message = input.value.trim();
    if (!message) return;
    
    addHeart2Message(message, 'user');
    
    setTimeout(() => {
        const response = getHeart2Response(heartStep);
        addHeart2Message(response, 'ai');
        heartStep++;
    }, 1000);
    
    input.value = '';
}

function addHeart2Message(message, sender) {
    const messagesDiv = document.getElementById('heart2Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Jordan';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getHeart2Response(step) {
    const responses = [
        "I appreciate that you're acknowledging it. It really did hurt when you said that in front of everyone.",
        "That means a lot to hear. I was starting to think you didn't even realize how it affected me.",
        "Thank you for saying that. It takes courage to admit when you're wrong. I accept your apology.",
        "I'm glad we could talk about this. It means a lot that our friendship matters to you too."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitHeart2Chat() {
    showChatComplete('🙏 Apology Chat', 'You took responsibility sincerely and repaired the relationship with authenticity!');
}

// SCENARIO 3: PARENT LIFE DECISION TALK
function showHeart3UI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">👨‍👩‍👧‍👦 Parent Life Decision Talk</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice discussing major life choices with your parents</p>
            </div>
            <div id="heart3Messages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Parent</div>
                        <div style="color: #495057;">You said you wanted to talk about something important. We're listening, honey.</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="heart3Input" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToHeart3()">
                <button onclick="sendToHeart3()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitHeart3Chat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToHeart3() {
    const input = document.getElementById('heart3Input');
    const message = input.value.trim();
    if (!message) return;
    
    addHeart3Message(message, 'user');
    
    setTimeout(() => {
        const response = getHeart3Response(heartStep);
        addHeart3Message(response, 'ai');
        heartStep++;
    }, 1000);
    
    input.value = '';
}

function addHeart3Message(message, sender) {
    const messagesDiv = document.getElementById('heart3Messages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Parent';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getHeart3Response(step) {
    const responses = [
        "That's a big decision, sweetheart. Can you help us understand what's drawing you to this path?",
        "We can see you've thought about this seriously. What are your concerns about the practical aspects?",
        "We appreciate you sharing your reasoning with us. Our main worry is just wanting you to be secure and happy.",
        "We may not fully understand it, but we trust you and we'll support you. We love you."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitHeart3Chat() {
    showChatComplete('👨‍👩‍👧‍👦 Parent Chat', 'You communicated your decision with maturity while honoring your family relationship!');
}

// =============================================================================
// MISSING FUNCTION FOR END BUTTONS - ADD THIS ONLY
// =============================================================================

function showChatComplete(chatTitle, feedbackMessage) {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="text-align: center; padding: 40px;">
            <h2 style="color: #28a745; margin-bottom: 20px;">🎉 ${chatTitle} Complete!</h2>
            
            <div style="background: #d4edda; padding: 25px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: #155724; margin-bottom: 15px;">✅ Great Practice!</h3>
                <p style="color: #666; line-height: 1.6;">${feedbackMessage}</p>
            </div>
            
            <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h4 style="color: #004085; margin-bottom: 10px;">🎯 What You Accomplished:</h4>
                <p style="color: #666;">You practiced real conversation skills in a safe environment and built confidence for similar real-world situations!</p>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <p style="color: #856404; margin: 0; font-size: 14px;"><strong>💡 Pro Tip:</strong> Practice makes perfect! The more you use these skills, the more natural they become.</p>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                <button onclick="showMainZones()" style="padding: 15px 25px; background: #17a2b8; color: white; border: none; border-radius: 10px; cursor: pointer;">🏋️ Choose Another Zone</button>
                <button onclick="showMainZones()" style="padding: 15px 25px; background: #28a745; color: white; border: none; border-radius: 10px; cursor: pointer;">🎯 Practice More!</button>
            </div>
            
            <div style="margin-top: 20px;">
                <button onclick="closeDialogueGym()" style="padding: 12px 20px; background: #6c757d; color: white; border: none; border-radius: 8px; cursor: pointer;">← Back to Main Portal</button>
            </div>
        </div>
    `;
}

// =============================================================================
// REACHING OUT ZONE CHAT FUNCTIONS
// =============================================================================

let reachingStep = 0;

function startProfessorChat() {
    reachingStep = 0;
    showProfessorChatUI();
}

function startManagerChat() {
    reachingStep = 0;
    showManagerChatUI();
}

function startFriendChat() {
    reachingStep = 0;
    showFriendChatUI();
}

// =============================================================================
// PROFESSOR EXTENSION CHAT
// =============================================================================

function showProfessorChatUI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">📧 Email Professor for Extension</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice requesting academic deadline extensions professionally</p>
            </div>
            <div id="professorMessages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Professor Johnson</div>
                        <div style="color: #495057;">Hello! I received your email about needing an extension. Can you tell me more about your situation and when you think you can submit the work?</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="professorInput" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToProfessor()">
                <button onclick="sendToProfessor()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitProfessorChat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToProfessor() {
    const input = document.getElementById('professorInput');
    const message = input.value.trim();
    if (!message) return;
    
    addProfessorMessage(message, 'user');
    
    setTimeout(() => {
        const response = getProfessorResponse(reachingStep);
        addProfessorMessage(response, 'ai');
        reachingStep++;
    }, 1000);
    
    input.value = '';
}

function addProfessorMessage(message, sender) {
    const messagesDiv = document.getElementById('professorMessages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Professor Johnson';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getProfessorResponse(step) {
    const responses = [
        "I appreciate you reaching out. Can you be more specific about what's preventing you from meeting the deadline?",
        "That sounds challenging. When do you realistically think you can submit the work?", 
        "I understand. Let's set a new deadline that works for both of us. How about Friday?",
        "Thank you for being upfront about this. I'll make a note of the extension in my records."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitProfessorChat() {
    showChatComplete('📧 Professor Chat', 'You communicated professionally and successfully requested your extension!');
}

// =============================================================================
// MANAGER MENTAL HEALTH DAY CHAT
// =============================================================================

function showManagerChatUI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">🧠 Request Mental Health Day</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice asking for mental health time off professionally</p>
            </div>
            <div id="managerMessages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Your Manager</div>
                        <div style="color: #495057;">Hi! I got your message about needing some time off. Let's talk about what you need and how we can make it work.</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="managerInput" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToManager()">
                <button onclick="sendToManager()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitManagerChat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToManager() {
    const input = document.getElementById('managerInput');
    const message = input.value.trim();
    if (!message) return;
    
    addManagerMessage(message, 'user');
    
    setTimeout(() => {
        const response = getManagerResponse(reachingStep);
        addManagerMessage(response, 'ai');
        reachingStep++;
    }, 1000);
    
    input.value = '';
}

function addManagerMessage(message, sender) {
    const messagesDiv = document.getElementById('managerMessages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Your Manager';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getManagerResponse(step) {
    const responses = [
        "I appreciate your honesty about needing time for your wellbeing. How much time do you think you need?",
        "Of course, your mental health is important. Let's make sure your work is covered while you're out.",
        "That sounds reasonable. Take the time you need to recharge.",
        "I'm glad you felt comfortable coming to me about this. Your wellbeing matters to our team."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitManagerChat() {
    showChatComplete('🧠 Manager Chat', 'You successfully advocated for your mental health needs professionally!');
}

// =============================================================================
// FRIEND EMOTIONAL SUPPORT CHAT
// =============================================================================

function showFriendChatUI() {
    const content = document.getElementById('dialogue-gym-content');
    content.innerHTML = `
        <div style="height: 600px; display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 10px;">
            <div style="background: linear-gradient(45deg, #17a2b8, #007bff); color: white; padding: 15px; text-align: center;">
                <h3 style="margin: 0;">💬 Ask Friend for Emotional Support</h3>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Practice reaching out to friends when you need support</p>
            </div>
            <div id="friendSupportMessages" style="flex: 1; background: #f8f9fa; padding: 20px; overflow-y: auto;">
                <div style="margin-bottom: 15px;">
                    <div style="background: #e9ecef; padding: 12px 15px; border-radius: 15px 15px 15px 5px; display: inline-block; max-width: 80%;">
                        <div style="font-weight: bold; color: #495057; font-size: 12px; margin-bottom: 5px;">Your Friend Alex</div>
                        <div style="color: #495057;">Hey! What's up? You seemed a bit off in your message. Is everything okay?</div>
                    </div>
                </div>
            </div>
            <div style="background: white; padding: 15px; border-top: 1px solid #ddd; display: flex; gap: 10px;">
                <input type="text" id="friendSupportInput" placeholder="Type your response..." style="flex: 1; padding: 10px; border: 2px solid #e9ecef; border-radius: 5px;" onkeypress="if(event.key==='Enter') sendToFriendSupport()">
                <button onclick="sendToFriendSupport()" style="padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 5px; cursor: pointer;">Send</button>
                <button onclick="exitFriendSupportChat()" style="padding: 10px 15px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">End</button>
            </div>
        </div>
    `;
}

function sendToFriendSupport() {
    const input = document.getElementById('friendSupportInput');
    const message = input.value.trim();
    if (!message) return;
    
    addFriendSupportMessage(message, 'user');
    
    setTimeout(() => {
        const response = getFriendSupportResponse(reachingStep);
        addFriendSupportMessage(response, 'ai');
        reachingStep++;
    }, 1000);
    
    input.value = '';
}

function addFriendSupportMessage(message, sender) {
    const messagesDiv = document.getElementById('friendSupportMessages');
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `margin-bottom: 15px; ${sender === 'user' ? 'text-align: right;' : 'text-align: left;'}`;
    const senderName = sender === 'user' ? 'You' : 'Alex';
    
    messageDiv.innerHTML = `
        <div style="background: ${sender === 'user' ? '#17a2b8' : '#e9ecef'}; color: ${sender === 'user' ? 'white' : '#495057'}; padding: 12px 15px; border-radius: ${sender === 'user' ? '15px 15px 5px 15px' : '15px 15px 15px 5px'}; display: inline-block; max-width: 80%;">
            <div style="font-weight: bold; color: ${sender === 'user' ? '#e9ecef' : '#495057'}; font-size: 12px; margin-bottom: 5px;">${senderName}</div>
            <div>${message}</div>
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getFriendSupportResponse(step) {
    const responses = [
        "I can tell something's bothering you. Want to talk about what's going on?",
        "That sounds really tough. I'm here to listen if you want to share more.",
        "Thanks for trusting me with this. How can I best support you right now?",
        "You don't have to go through this alone. I'm here for you, always."
    ];
    return responses[Math.min(step, responses.length - 1)];
}

function exitFriendSupportChat() {
    showChatComplete('💬 Friend Support Chat', 'You courageously reached out for support and strengthened your friendship!');
}


 // =============================================================================
// SHARED CRISIS ANALYSIS FUNCTION
// =============================================================================

async function analyzeCrisisWithMCP() {
    const input = document.getElementById('user-input').value.trim();
    
    if (!input) {
        alert('Please share how you\\'re feeling first.');
        return;
    }
    
    console.log('Analyzing input:', input);
    
    const response_div = document.getElementById('response');
    
    // 1. CHECK FOR EMPATHY MAP NEEDS FIRST (most specific)
    const empathyTriggers = [
        'talk to my', 'tell my parents', 'difficult conversation', 'family conflict',
        'convince someone', 'they dont understand', 'communicate with', 'relationship problem',
        'tell my mom', 'tell my dad', 'family pressure'
    ];
    
    const needsEmpathyMap = empathyTriggers.some(trigger => 
        input.toLowerCase().includes(trigger)
    );
    
    if (needsEmpathyMap) {
        // Launch Empathy Map Builder
        response_div.innerHTML = `
            <div style="background: #d4edda; padding: 20px; border-radius: 10px; border-left: 4px solid #28a745;">
                <strong>🗺️ Communication Challenge Detected - Launching Empathy Map Builder...</strong><br><br>
                <div style="text-align: center; margin: 20px 0;">
                    <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #28a745; border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                </div>
                <small style="color: #666;">Building understanding for better conversations...</small>
            </div>
        `;
        response_div.className = 'mcp-info';
        response_div.style.display = 'block';
        
        setTimeout(() => { startEmpathyMap(); }, 1500);
        return;
    }

    //FUTURE CHECK

    // Add after empathy check, before values check:
const futureTriggers = [
    'no motivation', 'lost motivation', 'dont see the point', 'whats the point',
    'future feels hopeless', 'cant see myself', 'no direction', 'stuck in life',
    'dreams feel impossible', 'goals seem unrealistic', 'losing hope', 'giving up',
    'dont know where im going', 'future looks bleak', 'no purpose'
];

const needsFutureVision = futureTriggers.some(trigger => 
    input.toLowerCase().includes(trigger)
);

if (needsFutureVision) {
    // Launch Future Self Simulator
    response_div.innerHTML = `
        <div style="background: #e8d5ff; padding: 20px; border-radius: 10px; border-left: 4px solid #6f42c1;">
            <strong>⏳ Motivation Challenge Detected - Launching Future Self Simulator...</strong><br><br>
            <div style="text-align: center; margin: 20px 0;">
                <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #6f42c1; border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            </div>
            <small style="color: #666;">Creating a powerful vision of your future to reignite your motivation...</small>
        </div>
    `;
    response_div.className = 'mcp-info';
    response_div.style.display = 'block';
    
    setTimeout(() => { startFutureSelf(); }, 1500);
    return;
}

// Add after future triggers, before empathy check:
const dialogueTriggers = [
    'social anxiety', 'cant talk to people', 'awkward conversations', 'dont know what to say',
    'scared to ask', 'afraid to speak up', 'conversation skills', 'social skills',
    'trouble communicating', 'hard to talk', 'social situations', 'shy around people',
    'cant say no', 'bad at boundaries', 'people please', 'avoid conflict'
];

const needsDialogueSkills = dialogueTriggers.some(trigger => 
    input.toLowerCase().includes(trigger)
);

if (needsDialogueSkills) {
    // Launch Dialogue Gym
    response_div.innerHTML = `
        <div style="background: #cce5ff; padding: 20px; border-radius: 10px; border-left: 4px solid #17a2b8;">
            <strong>💬 Communication Challenge Detected - Launching Dialogue Gym...</strong><br><br>
            <div style="text-align: center; margin: 20px 0;">
                <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #17a2b8; border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            </div>
            <small style="color: #666;">Building your social confidence through practice...</small>
        </div>
    `;
    response_div.className = 'mcp-info';
    response_div.style.display = 'block';
    
    setTimeout(() => { startDialogueGym(); }, 1500);
    return;
}


    // 2. CHECK FOR VALUES QUESTIONS (general decision-making)
    const valuesQuestions = [
        'should i', 'is it okay to', 'is it right to', 'what should i do',
        'pick a safe job', 'pick a risky job', 'follow my passion', 'choose',
        'which path', 'what career', 'life decision', 'big decision',
        'family expects', 'pressure to', 'supposed to', 'right thing to do',
        'stay safe or', 'secure or risky', 'stable or', 'follow dreams',
        'leave a job', 'quit my job', 'change career'
    ];
    
    const isValuesQuestion = valuesQuestions.some(trigger => 
        input.toLowerCase().includes(trigger)
    );
    
    if (isValuesQuestion) {
        // Launch Values Compass
        response_div.innerHTML = `
            <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; border-left: 4px solid #4a90e2;">
                <strong>🧭 Decision Question Detected - Launching Values Compass...</strong><br><br>
                <div style="text-align: center; margin: 20px 0;">
                    <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #4a90e2; border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                </div>
                <small style="color: #666;">Preparing your personalized values discovery journey...</small>
            </div>
        `;
        response_div.className = 'mcp-info';
        response_div.style.display = 'block';
        
        setTimeout(() => { startValuesCompass(); }, 1500);
        return;
    }
    
    // 3. CHECK FOR MENTAL HEALTH CRISIS (urgent)
    const crisisKeywords = [
        'kill myself', 'hurt myself', 'suicide', 'end my life', 'cant breathe',
        'heart racing', 'panic attack', 'want to die', 'hopeless', 'cant take it',
        'overwhelming', 'breaking down', 'falling apart', 'cant cope'
    ];
    
    const isCrisis = crisisKeywords.some(keyword => 
        input.toLowerCase().includes(keyword)
    );
    
    if (isCrisis) {
        // Launch S.O.S. System
        response_div.innerHTML = `
            <div style="background: #f8d7da; padding: 20px; border-radius: 10px; border-left: 4px solid #dc3545;">
                <strong>🚨 Crisis Detected - Launching S.O.S. System...</strong><br><br>
                <div style="text-align: center; margin: 20px 0;">
                    <div style="display: inline-block; width: 40px; height: 40px; border: 4px solid #dc3545; border-top: 4px solid transparent; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                </div>
                <small style="color: #666;">Getting you immediate support tools...</small>
            </div>
        `;
        response_div.className = 'error';
        response_div.style.display = 'block';
        
        setTimeout(() => { triggerMCPSOS(); }, 1500);
        return;
    }
    
    // 4. DEFAULT: Regular analysis for everything else
    continueWithCrisisAnalysis(input);
}

async function continueWithCrisisAnalysis(input) {
    const response_div = document.getElementById('response');
    
    try {
        // Show loading
        response_div.innerHTML = '<strong>🔄 Analyzing with MCP Server...</strong>';
        response_div.className = 'mcp-info';
        response_div.style.display = 'block';
        
        // Call MCP crisis detection
        const response = await fetch('/mcp/crisis_detection', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_text: input})
        });
        
        const mcpResult = await response.json();
        console.log('MCP Crisis Analysis Result:', mcpResult);
        
        const analysis = mcpResult.analysis;
        
        response_div.innerHTML = `
            <div style="text-align: left;">
                <strong>🤖 MCP Analysis Complete</strong><br>
                <strong>Crisis Detected:</strong> ${analysis.is_crisis ? 'Yes' : 'No'}<br>
                <strong>Primary Symptom:</strong> ${analysis.symptom_type}<br>
                <strong>Confidence:</strong> ${analysis.confidence}%<br>
                <strong>Recommended Tool:</strong> ${analysis.suggested_tool}<br>
                <small style="opacity: 0.7;">Analyzed by: ${mcpResult.mcp_tool} | ${mcpResult.timestamp}</small>
            </div>
        `;
        
        if (analysis.is_crisis) {
            response_div.innerHTML += '<br><strong>🚨 Crisis detected - launching S.O.S. mode in 2 seconds...</strong>';
            setTimeout(triggerMCPSOS, 2000);
        }
        
    } catch (error) {
        console.error('MCP analysis error:', error);
        response_div.innerHTML = 
            '<strong>⚠️ MCP Server connection failed.</strong><br>Please ensure the MCP server is running, then try the S.O.S. button for immediate help.';
    }
}

// =============================================================================
// SAFETY NET & RESOURCE HUB - UNIQUE FUNCTION NAMES
// =============================================================================

function openSafetyNet() {
    console.log('Opening Safety Net Hub');
    
    // Use existing content div or create temporary one
    let contentDiv = document.getElementById('dialogue-gym-content');
    if (!contentDiv) {
        contentDiv = document.getElementById('app-content') || document.body;
    }
    
    contentDiv.innerHTML = `
        <div style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #dc3545, #c82333); color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
                <h1 style="margin: 0 0 10px 0; font-size: 28px;">🆘 Safety Net & Resource Hub</h1>
                <p style="margin: 0; font-size: 16px; opacity: 0.9;">Vetted mental health resources for Pune, India</p>
                <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.8;">Confidential • Professional • Available 24/7</p>
            </div>

            <!-- CRISIS SUPPORT -->
            <div style="background: #f8d7da; padding: 25px; border-radius: 15px; border-left: 5px solid #dc3545; margin-bottom: 20px;">
                <h2 style="color: #721c24; margin: 0 0 15px 0; font-size: 22px;">🚨 Need Help Right Now?</h2>
                <p style="color: #721c24; margin-bottom: 20px;">If you're in crisis, please reach out immediately:</p>
                
                <!-- Aasra Hotline -->
                <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div style="flex: 1; min-width: 250px;">
                            <h3 style="color: #dc3545; margin: 0 0 8px 0;">Aasra Suicide Prevention</h3>
                            <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">24/7 crisis helpline • Trained volunteers • Confidential</p>
                            <div style="background: #e3f2fd; padding: 8px; border-radius: 6px; font-size: 12px; color: #1565c0;">
                                <strong>What to expect:</strong> Anonymous support, no judgment, trained listeners
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 18px; font-weight: bold; color: #dc3545; margin-bottom: 10px;">+91 9820466726</div>
                            <a href="tel:+919820466726" style="background: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; display: inline-block; font-size: 14px;">📞 Call Now</a>
                        </div>
                    </div>
                </div>

                <!-- iCALL -->
                <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div style="flex: 1; min-width: 250px;">
                            <h3 style="color: #dc3545; margin: 0 0 8px 0;">iCALL Listening Service</h3>
                            <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">TISS psychosocial helpline • Mon-Sat 10am-6pm</p>
                            <div style="background: #e3f2fd; padding: 8px; border-radius: 6px; font-size: 12px; color: #1565c0;">
                                <strong>What to expect:</strong> Professional counselors, emotional support, complete privacy
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 18px; font-weight: bold; color: #dc3545; margin-bottom: 10px;">022-25521111</div>
                            <a href="tel:02225521111" style="background: #dc3545; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; display: inline-block; font-size: 14px;">📞 Call Now</a>
                        </div>
                    </div>
                </div>

                <!-- WhatsApp Support -->
                <div style="background: white; padding: 20px; border-radius: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div style="flex: 1; min-width: 250px;">
                            <h3 style="color: #dc3545; margin: 0 0 8px 0;">WhatsApp Crisis Support</h3>
                            <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">Text-based crisis support when calling feels difficult</p>
                            <div style="background: #e3f2fd; padding: 8px; border-radius: 6px; font-size: 12px; color: #1565c0;">
                                <strong>What to expect:</strong> Text with trained volunteers, respond when you can
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 18px; font-weight: bold; color: #dc3545; margin-bottom: 10px;">+91 9152987821</div>
                            <a href="https://wa.me/919152987821" target="_blank" style="background: #25d366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; display: inline-block; font-size: 14px;">💬 WhatsApp</a>
                        </div>
                    </div>
                </div>
            </div>

            <!-- FIND PROFESSIONAL HELP -->
            <div style="background: #d1ecf1; padding: 25px; border-radius: 15px; border-left: 5px solid #17a2b8; margin-bottom: 20px;">
                <h2 style="color: #0c5460; margin: 0 0 15px 0; font-size: 22px;">🏥 Find Professional Help</h2>
                <p style="color: #0c5460; margin-bottom: 20px;">Connect with qualified mental health professionals:</p>
                
                <div style="display: grid; gap: 15px;">
                    <!-- Local Therapists -->
                    <div style="background: white; padding: 20px; border-radius: 10px;">
                        <h3 style="color: #17a2b8; margin: 0 0 10px 0;">🏢 In-Person Therapy (Pune)</h3>
                        <p style="margin: 0 0 15px 0; color: #666;">Find registered therapists and psychiatrists in Pune:</p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px;">
                            <a href="https://www.practo.com/pune/therapist" target="_blank" style="background: #17a2b8; color: white; padding: 8px 15px; text-decoration: none; border-radius: 6px; font-size: 14px;">🔍 Practo Directory</a>
                            <a href="https://www.nimhans.ac.in/" target="_blank" style="background: #17a2b8; color: white; padding: 8px 15px; text-decoration: none; border-radius: 6px; font-size: 14px;">🏥 NIMHANS</a>
                        </div>
                        <div style="background: #e3f2fd; padding: 8px; border-radius: 6px; font-size: 12px; color: #1565c0;">
                            <strong>What to expect:</strong> Browse profiles, check credentials, book appointments, insurance accepted
                        </div>
                    </div>

                    <!-- Online Therapy -->
                    <div style="background: white; padding: 20px; border-radius: 10px;">
                        <h3 style="color: #17a2b8; margin: 0 0 10px 0;">💻 Online Therapy</h3>
                        <p style="margin: 0 0 15px 0; color: #666;">Professional online therapy platforms:</p>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px;">
                            <a href="https://www.betterlyf.com/" target="_blank" style="background: #17a2b8; color: white; padding: 8px 15px; text-decoration: none; border-radius: 6px; font-size: 14px;">💙 BetterLYF</a>
                            <a href="https://yourdost.com/" target="_blank" style="background: #17a2b8; color: white; padding: 8px 15px; text-decoration: none; border-radius: 6px; font-size: 14px;">🗨️ YourDOST</a>
                        </div>
                        <div style="background: #e3f2fd; padding: 8px; border-radius: 6px; font-size: 12px; color: #1565c0;">
                            <strong>What to expect:</strong> Video/chat sessions, flexible scheduling, often more affordable
                        </div>
                    </div>
                </div>
            </div>

            <!-- SELF-HELP RESOURCES -->
            <div style="background: #d4edda; padding: 25px; border-radius: 15px; border-left: 5px solid #28a745; margin-bottom: 20px;">
                <h2 style="color: #155724; margin: 0 0 15px 0; font-size: 22px;">📖 Self-Help Resources</h2>
                <p style="color: #155724; margin-bottom: 20px;">Evidence-based resources from trusted organizations:</p>
                
                <div style="display: grid; gap: 10px;">
                    <div onclick="alertResourceInfo('anxiety')" style="background: white; padding: 15px; border-radius: 8px; cursor: pointer; border-left: 4px solid #28a745;">
                        <h4 style="color: #28a745; margin: 0 0 5px 0;">😰 Managing Anxiety</h4>
                        <p style="margin: 0; color: #666; font-size: 13px;">WHO, NIMHANS, and Live Love Laugh Foundation resources</p>
                    </div>
                    
                    <div onclick="alertResourceInfo('depression')" style="background: white; padding: 15px; border-radius: 8px; cursor: pointer; border-left: 4px solid #28a745;">
                        <h4 style="color: #28a745; margin: 0 0 5px 0;">😔 Understanding Depression</h4>
                        <p style="margin: 0; color: #666; font-size: 13px;">Evidence-based coping strategies and information</p>
                    </div>
                    
                    <div onclick="alertResourceInfo('relationships')" style="background: white; padding: 15px; border-radius: 8px; cursor: pointer; border-left: 4px solid #28a745;">
                        <h4 style="color: #28a745; margin: 0 0 5px 0;">💕 Healthy Relationships</h4>
                        <p style="margin: 0; color: #666; font-size: 13px;">Communication, boundaries, and relationship wellness</p>
                    </div>
                    
                    <div onclick="alertResourceInfo('mindfulness')" style="background: white; padding: 15px; border-radius: 8px; cursor: pointer; border-left: 4px solid #28a745;">
                        <h4 style="color: #28a745; margin: 0 0 5px 0;">🧘 Mindfulness & Meditation</h4>
                        <p style="margin: 0; color: #666; font-size: 13px;">Guided practices and meditation techniques</p>
                    </div>
                </div>
            </div>

            <!-- BACK BUTTON -->
            <div style="text-align: center; margin-top: 30px;">
                <button onclick="closeSafetyNet()" style="background: #6c757d; color: white; padding: 15px 30px; border: none; border-radius: 10px; cursor: pointer; font-size: 16px;">← Back to Main</button>
            </div>
        </div>
    `;
}

function alertResourceInfo(category) {
    const info = {
        'anxiety': 'Anxiety Resources:\\n\\n• WHO Anxiety Disorders Guide\\n• NIMHANS Self-Help Toolkit\\n• Breathing exercises & relaxation\\n• Understanding panic attacks\\n• Live Love Laugh Foundation materials',
        'depression': 'Depression Resources:\\n\\n• WHO Depression Information\\n• NIMHANS Clinical Guidelines\\n• Daily routine builders\\n• Self-care strategies\\n• Support group connections',
        'relationships': 'Relationship Resources:\\n\\n• Communication techniques\\n• Setting healthy boundaries\\n• Conflict resolution skills\\n• Building self-esteem\\n• Resources for abuse survivors',
        'mindfulness': 'Mindfulness Resources:\\n\\n• Headspace & Calm apps\\n• Art of Living centers (Pune)\\n• Guided meditation practices\\n• Mindful eating guides\\n• Scientific research on benefits'
    };
    
    alert(info[category]);
}

function closeSafetyNet() {
    // Go back to main - you can customize this
    location.reload();
}



//EXIT SOS FUNCTION DONT TOUCH
            function exitSOS() {
                console.log('Exiting MCP S.O.S. mode');
                document.getElementById('triage-screen').style.display = 'none';
                document.getElementById('intervention-screen').style.display = 'none';
                document.getElementById('main-interface').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

@app.get("/mcp/{tool_name}")
async def call_mcp_tool_get(tool_name: str):
    """Call MCP tool via GET request"""
    result = await mcp_client.call_mcp_tool(tool_name)
    return result

@app.post("/mcp/{tool_name}")
async def call_mcp_tool_post(tool_name: str, request: Request):
    """Call MCP tool via POST request"""
    try:
        data = await request.json()
        result = await mcp_client.call_mcp_tool(tool_name, data)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/mcp/status")
async def mcp_status():
    """Check MCP server connection status"""
    return {
        "status": "connected",
        "server": "youth-wellness-mcp",
        "version": "1.0.0",
        "available_tools": [
            "crisis_detection", "sos_triage", "box_breathing", 
            "visual_focus", "grounding_543", "muscle_relaxation", 
            "emergency_soundscape"
        ]
    }

if __name__ == "__main__":
    logger.info("Starting Youth Portal MCP Client...")
    uvicorn.run(app, host="127.0.0.1", port=8003)
