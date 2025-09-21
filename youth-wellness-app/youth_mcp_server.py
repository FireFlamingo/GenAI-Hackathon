#!/usr/bin/env python3
"""
Youth Mental Wellness MCP Server - FIXED VERSION
Proper Model Context Protocol implementation
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime

import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import storage

# MCP imports
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("youth-wellness-mcp")

# Global server instance
server = Server("youth-wellness-mcp")

# Global wellness components
model = None
storage_client = None
bucket_name = "youth-crisis-data-bucket"

def initialize_services():
    """Initialize AI and storage services"""
    global model, storage_client
    try:
        # Initialize Vertex AI
        vertexai.init(project="youth-wellness-mcp", location="us-central1")
        model = GenerativeModel("gemini-2.0-flash-exp")
        
        # Initialize Cloud Storage
        storage_client = storage.Client(project="youth-wellness-mcp")
        
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all available mental wellness tools"""
    return [
        types.Tool(
            name="crisis_detection",
            description="Analyze user text for mental health crisis signs and classify symptoms",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_text": {
                        "type": "string",
                        "description": "User's text input to analyze for crisis indicators"
                    }
                },
                "required": ["user_text"]
            },
        ),
        types.Tool(
            name="sos_triage",
            description="Get S.O.S. triage options for immediate crisis intervention",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="box_breathing",
            description="Interactive box breathing exercise for physical panic symptoms",
            inputSchema={
                "type": "object",
                "properties": {
                    "duration_seconds": {
                        "type": "integer",
                        "description": "Duration of the breathing exercise in seconds",
                        "default": 120
                    }
                }
            },
        ),
        types.Tool(
            name="visual_focus",
            description="Calming visual meditation for racing thoughts",
            inputSchema={
                "type": "object",
                "properties": {
                    "animation_speed": {
                        "type": "string",
                        "description": "Speed of animation: slow, medium, or fast",
                        "enum": ["slow", "medium", "fast"],
                        "default": "slow"
                    }
                }
            },
        ),
        types.Tool(
            name="grounding_543",
            description="5-4-3-2-1 sensory grounding exercise for dissociation",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="muscle_relaxation",
            description="Guided progressive muscle relaxation for physical tension",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        types.Tool(
            name="emergency_soundscape",
            description="Immersive comforting soundscape for emotional distress",
            inputSchema={
                "type": "object",
                "properties": {
                    "soundscape_type": {
                        "type": "string",
                        "description": "Type of soundscape",
                        "enum": ["rain", "forest", "ocean", "fireplace"],
                        "default": "rain"
                    }
                }
            },
        ),
        types.Tool(
            name="save_session_data",
            description="Save anonymized session data for analytics",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_type": {
                        "type": "string",
                        "description": "Type of session (crisis, wellness_check, intervention)"
                    },
                    "outcome": {
                        "type": "string",
                        "description": "Session outcome (resolved, escalated, ongoing)"
                    },
                    "duration_seconds": {
                        "type": "integer",
                        "description": "Duration of session in seconds"
                    },
                    "intervention_used": {
                        "type": "string",
                        "description": "Which intervention tool was used"
                    }
                },
                "required": ["session_type", "outcome"]
            },
        ),
        types.Tool(
            name="get_analytics",
            description="Retrieve aggregated wellness analytics and insights",
            inputSchema={
                "type": "object",
                "properties": {}
            },
        ),
        # VALUE TOOLS:

        types.Tool(
            name="values_discovery_expedition",
            description="Stage 1: Interactive scenarios to discover core values through branching choices",
            inputSchema={
                "type": "object",
                "properties": {
                    "stage": {
                        "type": "string",
                        "description": "Current stage: start, scenario_response",
                        "enum": ["start", "scenario_response"]
                    },
                    "scenario_id": {
                        "type": "integer",
                        "description": "ID of current scenario (1-15)"
                    },
                    "choice": {
                        "type": "string", 
                        "description": "User's choice: path_a or path_b"
                    },
                    "user_responses": {
                        "type": "array",
                        "description": "Array of previous responses"
                    }
                },
                "required": ["stage"]
            }
        ),

        types.Tool(
            name="values_synthesis_analysis",
            description="Stage 2: AI analysis of user choices to identify value patterns",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_responses": {
                        "type": "array",
                        "description": "Complete array of user scenario responses"
                    }
                },
                "required": ["user_responses"]
            }
        ),

        types.Tool(
            name="values_compass_creation",
            description="Stage 3: Create personalized Values Compass with visual representation",
            inputSchema={
                "type": "object", 
                "properties": {
                    "selected_values": {
                        "type": "array",
                        "description": "User's final selected core values (3-5)"
                    },
                    "scenario_context": {
                        "type": "array",
                        "description": "Original scenario responses for personalization"
                    }
                },
                "required": ["selected_values"]
            }
        ),

        types.Tool(
            name="values_compass_check",
            description="Stage 4: Use Values Compass to evaluate decisions and resolve conflicts", 
            inputSchema={
                "type": "object",
                "properties": {
                    "user_dilemma": {
                        "type": "string",
                        "description": "Current decision or conflict user is facing"
                    },
                    "user_values": {
                        "type": "array", 
                        "description": "User's established core values"
                    },
                    "decision_options": {
                        "type": "array",
                        "description": "Options user is considering"
                    }
                },
                "required": ["user_dilemma", "user_values"]
            }
        ),
        # =============================================================================
# FEATURE 3: EMPATHY MAP BUILDER - Understanding Others for Better Communication
# =============================================================================

        types.Tool(
            name="empathy_map_setup",
            description="Stage 1: Setup the conversation context and define the person to map",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_name": {"type": "string", "description": "Who the map is for"},
                    "conversation_goal": {"type": "string", "description": "Key message or outcome desired"},
                    "relationship": {"type": "string", "description": "Relationship to the person"}
                },
                "required": ["person_name", "conversation_goal"]
            }
        ),

        types.Tool(
            name="empathy_map_inquiry",
            description="Stage 2: Guided perspective-taking through probing questions",
            inputSchema={
                "type": "object",
                "properties": {
                    "stage": {"type": "string", "enum": ["start", "answer"]},
                    "category": {"type": "string", "enum": ["hopes", "fears", "influences", "complete"]},
                    "answer": {"type": "string", "description": "User's answer to current question"},
                    "responses": {"type": "array", "description": "Previous responses"}
                },
                "required": ["stage"]
            }
        ),

        types.Tool(
            name="empathy_map_synthesis",
            description="Stage 3: AI creates the visual empathy map from responses",
            inputSchema={
                "type": "object",
                "properties": {
                    "person_data": {"type": "object", "description": "Setup information"},
                    "inquiry_responses": {"type": "array", "description": "All inquiry responses"}
                },
                "required": ["person_data", "inquiry_responses"]
            }
        ),

        types.Tool(
            name="empathy_map_strategy",
            description="Stage 4: Strategic briefing - turning insights into conversational action",
            inputSchema={
                "type": "object",
                "properties": {
                    "empathy_map": {"type": "object", "description": "Generated empathy map"},
                    "conversation_goal": {"type": "string", "description": "Original conversation goal"}
                },
                "required": ["empathy_map", "conversation_goal"]
            }
        ),
# =============================================================================
# FEATURE 4: FUTURE SELF SIMULATOR - Visualizing Motivation Through Time
# =============================================================================

        types.Tool(
            name="future_self_input",
            description="Stage 1: Collect user inputs for future self simulation",
            inputSchema={
                "type": "object",
                "properties": {
                    "stage": {"type": "string", "enum": ["start", "answer"]},
                    "question_id": {"type": "integer", "description": "Current question number"},
                    "answer": {"type": "string", "description": "User's answer to current question"},
                    "responses": {"type": "array", "description": "Previous responses"}
                },
                "required": ["stage"]
            }
        ),

        types.Tool(
            name="future_self_generation",
            description="Stage 2: AI generates narrative and visual prompts",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_inputs": {"type": "array", "description": "All user responses"},
                    "simulation_preferences": {"type": "object", "description": "User preferences"}
                },
                "required": ["user_inputs"]
            }
        ),

        types.Tool(
            name="future_self_experience",
            description="Stage 3: Present immersive simulation to user",
            inputSchema={
                "type": "object",
                "properties": {
                    "generated_content": {"type": "object", "description": "Generated story and image"},
                    "user_profile": {"type": "object", "description": "User context"}
                },
                "required": ["generated_content"]
            }
        ),

        types.Tool(
            name="future_self_integration",
            description="Stage 4: Connect future vision to present actions",
            inputSchema={
                "type": "object",
                "properties": {
                    "future_vision": {"type": "object", "description": "Complete simulation"},
                    "commitment": {"type": "string", "description": "User's action commitment"}
                },
                "required": ["future_vision"]
            }
        ),
# =============================================================================
# FEATURE 5: DIALOGUE GYM - Interactive Social Skills Training
# =============================================================================

        types.Tool(
            name="dialogue_gym_scenarios",
            description="Get available workout zones and scenarios for dialogue practice",
            inputSchema={
                "type": "object",
                "properties": {
                    "zone": {"type": "string", "enum": ["assertiveness", "reaching_out", "social_connection", "heart_to_heart"]},
                    "action": {"type": "string", "enum": ["list_zones", "get_scenarios"]}
                },
                "required": ["action"]
            }
        ),

        types.Tool(
            name="dialogue_gym_persona",
            description="AI persona agent for role-playing in dialogue scenarios",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario_id": {"type": "string", "description": "ID of the scenario being practiced"},
                    "conversation_history": {"type": "array", "description": "Previous messages in conversation"},
                    "user_message": {"type": "string", "description": "User's latest message"},
                    "turn_number": {"type": "integer", "description": "Current conversation turn"}
                },
                "required": ["scenario_id", "user_message"]
            }
        ),

        types.Tool(
            name="dialogue_gym_coach",
            description="AI coach agent providing real-time feedback on communication",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario_goal": {"type": "string", "description": "Goal of the current scenario"},
                    "user_message": {"type": "string", "description": "User's message to analyze"},
                    "persona_message": {"type": "string", "description": "Persona's previous message"},
                    "conversation_context": {"type": "array", "description": "Conversation history"}
                },
                "required": ["scenario_goal", "user_message"]
            }
        ),

        types.Tool(
            name="dialogue_gym_analysis",
            description="Post-workout performance analysis and feedback",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario_data": {"type": "object", "description": "Scenario information"},
                    "conversation_history": {"type": "array", "description": "Complete conversation transcript"},
                    "coach_feedback": {"type": "array", "description": "All coach feedback given"}
                },
                "required": ["scenario_data", "conversation_history"]
            }
        )





    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool execution"""
    global model, storage_client, bucket_name
    
    try:
        if name == "crisis_detection":
            result = await crisis_detection_tool(arguments.get("user_text", ""))
        elif name == "sos_triage":
            result = sos_triage_tool()
        elif name == "box_breathing":
            result = box_breathing_tool(arguments.get("duration_seconds", 120))
        elif name == "visual_focus":
            result = visual_focus_tool(arguments.get("animation_speed", "slow"))
        elif name == "grounding_543":
            result = grounding_543_tool()
        elif name == "muscle_relaxation":
            result = muscle_relaxation_tool()
        elif name == "emergency_soundscape":
            result = emergency_soundscape_tool(arguments.get("soundscape_type", "rain"))
        elif name == "save_session_data":
            result = await save_session_data_tool(arguments)
        elif name == "get_analytics":
            result = await get_analytics_tool()
        elif name == "values_discovery_expedition":
            result = await values_discovery_expedition_tool(arguments)
        elif name == "values_synthesis_analysis":  
            result = await values_synthesis_analysis_tool(arguments)
        elif name == "values_compass_creation":
            result = await values_compass_creation_tool(arguments)
        elif name == "values_compass_check":
            result = await values_compass_check_tool(arguments)

        else:
            raise ValueError(f"Unknown tool: {name}")
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        error_result = {
            "error": str(e),
            "tool": name,
            "status": "failed"
        }
        return [types.TextContent(type="text", text=json.dumps(error_result, indent=2))]

async def crisis_detection_tool(user_text: str) -> dict:
    """Crisis detection and symptom classification"""
    global model
    
    prompt = f"""
    Analyze this text for mental health crisis signs: "{user_text}"
    
    Classify the PRIMARY symptom type:
    - racing_thoughts: Racing thoughts, can't stop thinking, mental overwhelm
    - physical_panic: Heart pounding, can't breathe, physical panic symptoms  
    - dissociation: Feeling unreal, foggy, detached from reality
    - sadness: Sudden heavy sadness, emptiness, depression wave
    - tension: Body tense, restless, want to escape, agitation
    - numbness: Feeling numb, frozen, shut down, disconnected
    
    Respond ONLY with valid JSON:
    {{"is_crisis": true, "symptom_type": "racing_thoughts", "confidence": 85, "suggested_tool": "visual_focus"}}
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean JSON from response
        if '{' in response_text and '}' in response_text:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_text = response_text[start:end]
        else:
            json_text = response_text
        
        result = json.loads(json_text)
        
        # Save crisis event
        await save_crisis_event(user_text, result)
        
        return {
            "mcp_tool": "crisis_detection",
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Crisis detection error: {e}")
        return {
            "mcp_tool": "crisis_detection",
            "analysis": {
                "is_crisis": True, 
                "symptom_type": "physical_panic", 
                "confidence": 50, 
                "suggested_tool": "box_breathing"
            },
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def sos_triage_tool() -> dict:
    """S.O.S. triage options"""
    return {
        "mcp_tool": "sos_triage",
        "question": "Right now, in this moment, what do you feel the most?",
        "options": [
            {
                "id": "racing_thoughts",
                "text": "💭 My thoughts are racing and I can't stop them.",
                "recommended_tool": "visual_focus"
            },
            {
                "id": "physical_panic", 
                "text": "💓 My heart is pounding and I can't breathe.",
                "recommended_tool": "box_breathing"
            },
            {
                "id": "dissociation",
                "text": "🌫️ Everything feels unreal, like I'm in a fog.",
                "recommended_tool": "grounding_543"
            },
            {
                "id": "sadness",
                "text": "😔 I feel a sudden, heavy wave of sadness or emptiness.",
                "recommended_tool": "emergency_soundscape"
            },
            {
                "id": "tension",
                "text": "⚡ My body is tense, restless, and wants to escape.",
                "recommended_tool": "muscle_relaxation"
            },
            {
                "id": "numbness",
                "text": "🧊 I just feel numb and frozen.",
                "recommended_tool": "emergency_soundscape"
            }
        ],
        "timestamp": datetime.now().isoformat()
    }

def box_breathing_tool(duration_seconds: int) -> dict:
    """Box breathing intervention"""
    cycles = max(1, duration_seconds // 16)  # 16 seconds per cycle
    
    return {
        "mcp_tool": "box_breathing",
        "intervention": {
            "name": "Interactive Box Breathing",
            "type": "breathing_visual",
            "description": "Visual guide to regulate nervous system and reduce heart rate",
            "duration_seconds": duration_seconds,
            "total_cycles": cycles,
            "instructions": "Follow the expanding circle as it guides your breathing",
            "breathing_pattern": [
                {"phase": "inhale", "duration": 4, "instruction": "Breathe in slowly", "visual_cue": "expand"},
                {"phase": "hold_in", "duration": 4, "instruction": "Hold your breath", "visual_cue": "pause_expanded"},
                {"phase": "exhale", "duration": 4, "instruction": "Breathe out slowly", "visual_cue": "contract"},
                {"phase": "hold_out", "duration": 4, "instruction": "Hold empty", "visual_cue": "pause_contracted"}
            ],
            "completion_message": "Excellent work! Notice how much calmer you feel now."
        },
        "timestamp": datetime.now().isoformat()
    }

def visual_focus_tool(animation_speed: str) -> dict:
    """Visual focus meditation"""
    speed_settings = {
        "slow": {"duration": 30, "description": "Very slow, hypnotic movement"},
        "medium": {"duration": 20, "description": "Moderate, steady rhythm"},
        "fast": {"duration": 10, "description": "Dynamic, engaging motion"}
    }
    
    setting = speed_settings.get(animation_speed, speed_settings["slow"])
    
    return {
        "mcp_tool": "visual_focus",
        "intervention": {
            "name": "Calming Visual Focus",
            "type": "visual_meditation",
            "description": "Mesmerizing animation to interrupt racing thoughts",
            "duration_seconds": 120,
            "animation": {
                "type": "spiral_particles",
                "speed": animation_speed,
                "rotation_duration": setting["duration"],
                "color_scheme": "calming_gradient",
                "description": setting["description"]
            },
            "instructions": "Focus on the center of the animation. Let your thoughts follow the gentle movement.",
            "guidance": [
                "Don't try to stop your thoughts",
                "Just watch the movement",
                "Let your mind become curious about the patterns",
                "Breathe naturally as you watch"
            ]
        },
        "timestamp": datetime.now().isoformat()
    }

def grounding_543_tool() -> dict:
    """5-4-3-2-1 grounding exercise"""
    return {
        "mcp_tool": "grounding_543",
        "intervention": {
            "name": "5-4-3-2-1 Grounding Exercise",
            "type": "sensory_grounding",
            "description": "Reconnect with your physical environment through your senses",
            "estimated_duration": 300,
            "steps": [
                {
                    "step": 1,
                    "sense": "sight",
                    "count": 5,
                    "instruction": "Look around and name 5 things you can see",
                    "examples": ["the wall color", "your hands", "a door", "the ceiling", "shadows"],
                    "guidance": "Take your time. Really notice the details."
                },
                {
                    "step": 2,
                    "sense": "touch",
                    "count": 4,
                    "instruction": "Find and touch 4 different textures",
                    "examples": ["your clothing", "a smooth surface", "your hair", "something rough"],
                    "guidance": "Notice the temperature, texture, and weight."
                },
                {
                    "step": 3,
                    "sense": "hearing",
                    "count": 3,
                    "instruction": "Listen carefully for 3 distinct sounds",
                    "examples": ["your breathing", "distant traffic", "air conditioning", "footsteps"],
                    "guidance": "Close your eyes if it helps you focus on sounds."
                },
                {
                    "step": 4,
                    "sense": "smell",
                    "count": 2,
                    "instruction": "Notice 2 different scents in your environment",
                    "examples": ["the air", "soap", "food", "cleaning products", "your clothes"],
                    "guidance": "Take gentle breaths in through your nose."
                },
                {
                    "step": 5,
                    "sense": "taste",
                    "count": 1,
                    "instruction": "Focus on 1 taste you can detect",
                    "examples": ["your mouth", "toothpaste", "coffee", "gum", "neutral saliva"],
                    "guidance": "This might be subtle - that's completely normal."
                }
            ],
            "completion_message": "Perfect! You are here, in this moment, in this place. You are present and safe.",
            "follow_up": "Take a moment to notice how you feel compared to when you started."
        },
        "timestamp": datetime.now().isoformat()
    }

def muscle_relaxation_tool() -> dict:
    """Progressive muscle relaxation"""
    return {
        "mcp_tool": "muscle_relaxation",
        "intervention": {
            "name": "Guided Progressive Muscle Relaxation",
            "type": "physical_release",
            "description": "Release physical tension through systematic muscle tension and release",
            "estimated_duration": 240,
            "instructions": "Tense each muscle group for 5 seconds, then completely release and notice the relaxation",
            "muscle_groups": [
                {
                    "name": "hands_and_forearms",
                    "tension_instruction": "Make tight fists and tense your forearms",
                    "release_instruction": "Open your hands and let your arms fall completely loose",
                    "focus": "Notice the contrast between tension and relaxation"
                },
                {
                    "name": "upper_arms_and_shoulders",
                    "tension_instruction": "Pull your arms tight against your body and lift your shoulders to your ears",
                    "release_instruction": "Let your arms drop heavy and your shoulders fall down",
                    "focus": "Feel the weight of your arms as they relax"
                },
                {
                    "name": "face_and_head",
                    "tension_instruction": "Scrunch your face tight - close eyes, clench jaw, furrow brow",
                    "release_instruction": "Let your entire face go soft and smooth",
                    "focus": "Allow your jaw to drop slightly open"
                },
                {
                    "name": "neck_and_throat",
                    "tension_instruction": "Gently tense your neck muscles",
                    "release_instruction": "Let your neck relax completely",
                    "focus": "Feel your head settle comfortably"
                },
                {
                    "name": "chest_and_back",
                    "tension_instruction": "Arch your back slightly and expand your chest",
                    "release_instruction": "Let your chest fall and your back settle naturally",
                    "focus": "Notice your breathing becoming deeper"
                },
                {
                    "name": "legs_and_feet",
                    "tension_instruction": "Straighten your legs, point your toes, tense your thighs",
                    "release_instruction": "Let your legs become completely heavy and loose",
                    "focus": "Feel your legs sinking into relaxation"
                }
            ],
            "completion_message": "Excellent work. Your body has released significant tension. Take a moment to appreciate how much calmer you feel.",
            "final_instruction": "Sit quietly for another minute and enjoy this relaxed state."
        },
        "timestamp": datetime.now().isoformat()
    }

def emergency_soundscape_tool(soundscape_type: str) -> dict:
    """Emergency comforting soundscape"""
    soundscapes = {
        "rain": {
            "name": "Gentle Rain",
            "description": "Soft rain on a window with occasional thunder in the distance",
            "visual_theme": "water_droplets_on_glass",
            "mood": "peaceful_and_cleansing"
        },
        "forest": {
            "name": "Peaceful Forest",
            "description": "Gentle wind through trees with distant bird songs",
            "visual_theme": "swaying_green_trees",
            "mood": "grounded_and_natural"
        },
        "ocean": {
            "name": "Calm Ocean Waves",
            "description": "Gentle waves washing onto a peaceful shore",
            "visual_theme": "rhythmic_blue_waves",
            "mood": "vast_and_soothing"
        },
        "fireplace": {
            "name": "Cozy Fireplace",
            "description": "Gentle crackling fire with warm, dancing flames",
            "visual_theme": "warm_orange_flames",
            "mood": "safe_and_comforting"
        }
    }
    
    selected = soundscapes.get(soundscape_type, soundscapes["rain"])
    
    return {
        "mcp_tool": "emergency_soundscape",
        "intervention": {
            "name": f"Emergency Comfort: {selected['name']}",
            "type": "immersive_comfort",
            "description": "A safe, comforting sensory experience that requires no effort from you",
            "duration_seconds": 300,
            "soundscape": selected,
            "visual_component": {
                "type": selected["visual_theme"],
                "description": f"Gentle visual that matches the {soundscape_type} sounds",
                "auto_dim": True
            },
            "binaural_audio": {
                "frequency": "40hz_gamma_wave",
                "description": "Subtle background frequency to promote calm alertness"
            },
            "primary_message": "You are safe. This feeling will pass. You are not alone.",
            "secondary_messages": [
                "You don't need to do anything right now except breathe",
                "It's okay to just exist in this moment",
                "You have survived difficult moments before",
                "This is a safe space for you to simply be"
            ],
            "instructions": "Just breathe and let the sounds wash over you. There's nothing you need to fix or figure out right now."
        },
        "timestamp": datetime.now().isoformat()
    }

async def save_crisis_event(user_input: str, crisis_result: dict):
    """Save crisis event to cloud storage"""
    global storage_client, bucket_name
    
    try:
        bucket = storage_client.bucket(bucket_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"mcp_crisis_events/{timestamp}_crisis_event.json"
        
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "mcp_version": "1.0.0",
            "crisis_detected": crisis_result.get("is_crisis", False),
            "symptom_type": crisis_result.get("symptom_type", "unknown"),
            "confidence": crisis_result.get("confidence", 0),
            "suggested_tool": crisis_result.get("suggested_tool", "none"),
            "input_metadata": {
                "length": len(user_input),
                "word_count": len(user_input.split()),
                "contains_keywords": any(word in user_input.lower() for word in ["help", "panic", "scared", "overwhelmed", "crisis"])
            },
            "session_id": f"mcp_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(event_data, indent=2))
        logger.info(f"MCP crisis event saved: {filename}")
        
    except Exception as e:
        logger.error(f"Failed to save MCP crisis event: {e}")

async def save_session_data_tool(data: dict) -> dict:
    """Save session data"""
    global storage_client, bucket_name
    
    try:
        bucket = storage_client.bucket(bucket_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"mcp_sessions/{timestamp}_session.json"
        
        session_data = {
            "timestamp": datetime.now().isoformat(),
            "mcp_version": "1.0.0",
            "session_data": data
        }
        
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(session_data, indent=2))
        
        return {
            "mcp_tool": "save_session_data",
            "status": "success",
            "filename": filename,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "mcp_tool": "save_session_data",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

async def get_analytics_tool() -> dict:
    """Get wellness analytics"""
    global storage_client, bucket_name
    
    try:
        bucket = storage_client.bucket(bucket_name)
        
        # Analyze MCP crisis events
        crisis_blobs = bucket.list_blobs(prefix="mcp_crisis_events/")
        crisis_count = 0
        total_events = 0
        symptom_distribution = {}
        tool_usage = {}
        
        for blob in crisis_blobs:
            try:
                content = blob.download_as_text()
                event = json.loads(content)
                total_events += 1
                
                if event.get("crisis_detected"):
                    crisis_count += 1
                    symptom = event.get("symptom_type", "unknown")
                    symptom_distribution[symptom] = symptom_distribution.get(symptom, 0) + 1
                    
                    tool = event.get("suggested_tool", "none")
                    tool_usage[tool] = tool_usage.get(tool, 0) + 1
                    
            except Exception as e:
                logger.error(f"Error processing analytics event: {e}")
                continue
        
        return {
            "mcp_tool": "get_analytics",
            "analytics": {
                "overview": {
                    "total_events": total_events,
                    "crisis_events": crisis_count,
                    "crisis_rate_percent": round((crisis_count / total_events * 100) if total_events > 0 else 0, 1)
                },
                "symptom_distribution": symptom_distribution,
                "tool_usage": tool_usage,
                "most_common_symptom": max(symptom_distribution.items(), key=lambda x: x[1])[0] if symptom_distribution else "none",
                "most_used_tool": max(tool_usage.items(), key=lambda x: x[1])[0] if tool_usage else "none"
            },
            "generated_at": datetime.now().isoformat(),
            "data_period": f"All time through {datetime.now().strftime('%Y-%m-%d')}"
        }
        
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return {
            "mcp_tool": "get_analytics",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# VALUES COMPASS TOOL IMPLEMENTATIONS

DISCOVERY_SCENARIOS = [
    {
        "id": 1,
        "domain": "career",
        "scenario": "You're offered two job opportunities:",
        "path_a": {"text": "A secure, well-paying job with a defined career ladder that your family would be proud of", "values": ["security", "family_approval", "structure"]},
        "path_b": {"text": "A lower-paying role at a startup with high risk, but complete creative freedom to build something from scratch", "values": ["creativity", "autonomy", "innovation"]}
    },
    {
        "id": 2, 
        "domain": "social",
        "scenario": "Your friend group is planning something you don't agree with:",
        "path_a": {"text": "Go along to maintain harmony and avoid conflict", "values": ["harmony", "belonging", "peace"]},
        "path_b": {"text": "Speak your truth, risking conflict but staying authentic to yourself", "values": ["authenticity", "integrity", "courage"]}
    },
    {
        "id": 3,
        "domain": "lifestyle", 
        "scenario": "You have savings and two life paths to choose:",
        "path_a": {"text": "Buy a home in your familiar hometown, surrounded by support system", "values": ["security", "community", "stability"]},
        "path_b": {"text": "Use savings to travel the world for a year, embracing uncertainty and new experiences", "values": ["adventure", "growth", "freedom"]}
    },
    {
        "id": 4,
        "domain": "impact",
        "scenario": "You want to make a difference in the world:",
        "path_a": {"text": "Volunteer for local charity, making direct impact on a few individuals", "values": ["compassion", "direct_impact", "community"]},
        "path_b": {"text": "Work on large-scale policy, indirect impact that might affect thousands in years", "values": ["justice", "systemic_change", "patience"]}
    },
    {
        "id": 5,
        "domain": "relationships",
        "scenario": "In romantic relationships, you value:",
        "path_a": {"text": "Deep emotional intimacy and vulnerability, even if it's intense", "values": ["intimacy", "authenticity", "depth"]},
        "path_b": {"text": "Healthy independence and personal space within the relationship", "values": ["autonomy", "balance", "respect"]}
    },
    {
        "id": 6,
        "domain": "learning",
        "scenario": "When learning something new, you prefer:",
        "path_a": {"text": "Mastering one subject deeply, becoming an expert in that field", "values": ["mastery", "depth", "expertise"]}, 
        "path_b": {"text": "Learning broadly across many subjects, staying curious about everything", "values": ["curiosity", "breadth", "exploration"]}
    },
    {
        "id": 7,
        "domain": "success",
        "scenario": "Your definition of success is:",
        "path_a": {"text": "Being recognized and respected by others for your achievements", "values": ["recognition", "achievement", "status"]},
        "path_b": {"text": "Feeling fulfilled and proud of your personal growth, regardless of outside recognition", "values": ["fulfillment", "growth", "self_worth"]}
    }
]

CORE_VALUES_LIBRARY = {
    "autonomy": "The freedom to make your own choices and live life on your terms",
    "creativity": "The drive to express yourself and create something new and original", 
    "security": "The need for stability, predictability, and safety in your life",
    "adventure": "The desire for new experiences, excitement, and exploration",
    "authenticity": "Being true to yourself and living according to your genuine nature",
    "compassion": "Deep care for others' wellbeing and desire to alleviate suffering",
    "justice": "The drive to ensure fairness and fight against inequality",
    "growth": "Continuous learning, improvement, and personal development",
    "community": "Strong connection and belonging with others who share your values",
    "integrity": "Living in alignment with your moral principles and being honest",
    "excellence": "The pursuit of high quality and doing your best in everything",
    "balance": "Harmony between different aspects of life and avoiding extremes",
    "courage": "The strength to face challenges and stand up for what's right",
    "wisdom": "The pursuit of deep understanding and sound judgment",
    "impact": "Making a meaningful difference in the world around you"
}

async def values_discovery_expedition_tool(arguments: dict) -> dict:
    """Stage 1: Interactive scenarios for values discovery"""
    try:
        stage = arguments.get("stage")
        user_responses = arguments.get("user_responses", [])
        
        if stage == "start":
            # Return first scenario
            return {
                "mcp_tool": "values_discovery_expedition",
                "stage": "scenario",
                "current_scenario": DISCOVERY_SCENARIOS[0],
                "progress": {"current": 1, "total": len(DISCOVERY_SCENARIOS)},
                "intro_message": "Let's explore what truly drives you. There are no right or wrong answers, only what feels most authentic to you.",
                "timestamp": datetime.now().isoformat()
            }
            
        elif stage == "scenario_response":
            scenario_id = arguments.get("scenario_id", 1)
            choice = arguments.get("choice")  # "path_a" or "path_b"
            
            # Record the response
            new_response = {
                "scenario_id": scenario_id,
                "choice": choice,
                "values_indicated": DISCOVERY_SCENARIOS[scenario_id-1][choice]["values"]
            }
            user_responses.append(new_response)
            
            # Check if more scenarios
            next_scenario_id = scenario_id + 1
            if next_scenario_id <= len(DISCOVERY_SCENARIOS):
                return {
                    "mcp_tool": "values_discovery_expedition", 
                    "stage": "scenario",
                    "current_scenario": DISCOVERY_SCENARIOS[next_scenario_id-1],
                    "progress": {"current": next_scenario_id, "total": len(DISCOVERY_SCENARIOS)},
                    "user_responses": user_responses,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Expedition complete
                return {
                    "mcp_tool": "values_discovery_expedition",
                    "stage": "complete", 
                    "user_responses": user_responses,
                    "message": "Expedition complete! Ready for synthesis.",
                    "timestamp": datetime.now().isoformat()
                }
                
        # Save expedition data
        await save_values_data("expedition", user_responses)
        
    except Exception as e:
        logger.error(f"Values discovery error: {e}")
        return {"mcp_tool": "values_discovery_expedition", "error": str(e)}

async def values_synthesis_analysis_tool(arguments: dict) -> dict:
    """Stage 2: AI analysis of patterns in user responses"""
    try:
        user_responses = arguments.get("user_responses", [])
        
        # Analyze value patterns
        value_counts = {}
        for response in user_responses:
            for value in response["values_indicated"]:
                value_counts[value] = value_counts.get(value, 0) + 1
        
        # Get top values
        sorted_values = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
        top_values = sorted_values[:7]  # Top 7 for selection
        
        # Generate AI insight using the model
        pattern_prompt = f"""
        Analyze this user's values expedition results: {user_responses}
        
        The user's choices show these value patterns: {dict(top_values)}
        
        Write a warm, insightful 2-3 sentence analysis that:
        1. Highlights the strongest pattern you notice
        2. Connects it to their authentic self
        3. Feels personal and validating
        
        Start with: "I've noticed a pattern in your expedition..."
        """
        
        ai_response = model.generate_content(pattern_prompt)
        ai_insight = ai_response.text.strip()
        
        return {
            "mcp_tool": "values_synthesis_analysis",
            "ai_insight": ai_insight,
            "suggested_values": [
                {
                    "name": value,
                    "count": count,
                    "definition": CORE_VALUES_LIBRARY.get(value, "Core personal value"),
                    "highlighted": count >= 3  # Strongly indicated
                }
                for value, count in top_values
            ],
            "instruction": "Do these resonate? Please select the 3-5 that feel like your 'True North'—the values that are most essentially you.",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Values synthesis error: {e}")
        return {"mcp_tool": "values_synthesis_analysis", "error": str(e)}

async def values_compass_creation_tool(arguments: dict) -> dict:
    """Stage 3: Create personalized Values Compass"""
    try:
        selected_values = arguments.get("selected_values", [])
        scenario_context = arguments.get("scenario_context", [])
        
        # Generate personalized definitions
        personalized_definitions = {}
        for value in selected_values[:3]:  # Top 3 as "True North"
            
            personalization_prompt = f"""
            Based on this user's expedition choices: {scenario_context}
            
            They selected "{value}" as a core value. The generic definition is: "{CORE_VALUES_LIBRARY.get(value, '')}"
            
            Write a personalized definition that:
            1. Reflects how THEY specifically live this value based on their choices
            2. Is warm and affirming 
            3. Starts with "For you, {value.title()} means..."
            4. Is 1-2 sentences maximum
            """
            
            ai_response = model.generate_content(personalization_prompt)
            personalized_definitions[value] = ai_response.text.strip()
        
        # Create compass structure
        compass = {
            "true_north_values": selected_values[:3],
            "supporting_values": selected_values[3:] if len(selected_values) > 3 else [],
            "personalized_definitions": personalized_definitions,
            "created_date": datetime.now().isoformat()
        }
        
        # Save compass
        await save_values_data("compass", compass)
        
        return {
            "mcp_tool": "values_compass_creation",
            "compass": compass,
            "visual_config": {
                "primary_color": "#4a90e2",
                "accent_color": "#7b68ee", 
                "layout": "circular_compass"
            },
            "completion_message": "Your Personal Values Compass is ready! This is your guide for authentic decision-making.",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Compass creation error: {e}")
        return {"mcp_tool": "values_compass_creation", "error": str(e)}

async def values_compass_check_tool(arguments: dict) -> dict:
    """Stage 4: Use compass for decision guidance"""
    try:
        user_dilemma = arguments.get("user_dilemma")
        user_values = arguments.get("user_values", [])
        decision_options = arguments.get("decision_options", [])
        
        # Generate compass check guidance
        compass_prompt = f"""
        A user with these core values: {user_values}
        
        Is facing this dilemma: "{user_dilemma}"
        
        Decision options: {decision_options if decision_options else "Not specified"}
        
        Provide guidance using the Compass Check Framework:
        1. ALIGNMENT: Which option aligns most with their core values?
        2. TENSION: Does any choice create tension with their values?  
        3. INTEGRATION: Is there a creative third path honoring multiple values?
        
        Be supportive, specific, and actionable. Reference their specific values.
        """
        
        ai_response = model.generate_content(compass_prompt)
        guidance = ai_response.text.strip()
        
        return {
            "mcp_tool": "values_compass_check",
            "guidance": guidance,
            "framework": {
                "alignment": "Which option aligns most closely with your 'True North' values?",
                "tension": "Does this choice create significant tension with any of your core values?", 
                "integration": "Is there a third path—a creative compromise that could honor multiple values at once?"
            },
            "user_values": user_values,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Compass check error: {e}")
        return {"mcp_tool": "values_compass_check", "error": str(e)}

async def save_values_data(data_type: str, data: dict):
    """Save values-related data to cloud storage"""
    try:
        bucket = storage_client.bucket(bucket_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"values_compass/{timestamp}_{data_type}.json"
        
        values_data = {
            "timestamp": datetime.now().isoformat(),
            "mcp_version": "1.0.0", 
            "data_type": data_type,
            "data": data
        }
        
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(values_data, indent=2))
        logger.info(f"Values data saved: {filename}")
        
    except Exception as e:
        logger.error(f"Failed to save values data: {e}")

EMPATHY_QUESTIONS = {
    "hopes": [
        "What is their biggest dream for your future?",
        "What does a 'successful life' look like from their point of view?",
        "What words do they often use when talking about the future?"
    ],
    "fears": [
        "What is their absolute worst-case scenario regarding your situation?",
        "What past struggles or regrets in their own life might be influencing their perspective?",
        "What would they feel they have to sacrifice or lose if you follow your path?"
    ],
    "influences": [
        "Whose opinions matter most to them? What would those people say?",
        "What cultural messages or media shape their worldview on this topic?"
    ]
}

async def empathy_map_setup_tool(arguments: dict) -> dict:
    """Stage 1: Setup the empathy mapping session"""
    try:
        person_name = arguments.get("person_name")
        goal = arguments.get("conversation_goal")
        relationship = arguments.get("relationship", "someone important")
        
        setup_data = {
            "person_name": person_name,
            "conversation_goal": goal,
            "relationship": relationship,
            "created_at": datetime.now().isoformat()
        }
        
        # Save setup data
        await save_empathy_data("setup", setup_data)
        
        return {
            "mcp_tool": "empathy_map_setup",
            "setup_complete": True,
            "person_name": person_name,
            "goal": goal,
            "message": f"Perfect! We're building an empathy map for {person_name}. Remember, the goal isn't to win an argument, but to build a bridge of understanding so your message can be truly heard.",
            "next_step": "inquiry",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Empathy setup error: {e}")
        return {"mcp_tool": "empathy_map_setup", "error": str(e)}

async def empathy_map_inquiry_tool(arguments: dict) -> dict:
    """Stage 2: Guided perspective-taking questions"""
    try:
        stage = arguments.get("stage")
        responses = arguments.get("responses", [])
        
        if stage == "start":
            # Start with hopes & values
            return {
                "mcp_tool": "empathy_map_inquiry",
                "stage": "question",
                "category": "hopes",
                "question_number": 1,
                "question": EMPATHY_QUESTIONS["hopes"][0],
                "category_title": "HOPES & VALUES (What they want for you)",
                "instruction": "Take your time to really think about their perspective. There are no wrong answers.",
                "progress": {"current": 1, "total": 8}
            }
            
        elif stage == "answer":
            category = arguments.get("category")
            answer = arguments.get("answer")
            
            # Record the response
            new_response = {
                "category": category,
                "question": arguments.get("current_question", ""),
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            }
            responses.append(new_response)
            
            # Determine next question
            current_progress = len(responses)
            
            if current_progress < 3:  # Continue with hopes
                return {
                    "mcp_tool": "empathy_map_inquiry",
                    "stage": "question",
                    "category": "hopes",
                    "question_number": current_progress + 1,
                    "question": EMPATHY_QUESTIONS["hopes"][current_progress],
                    "category_title": "HOPES & VALUES (What they want for you)",
                    "progress": {"current": current_progress + 1, "total": 8},
                    "responses": responses
                }
            elif current_progress < 6:  # Move to fears
                fear_index = current_progress - 3
                return {
                    "mcp_tool": "empathy_map_inquiry",
                    "stage": "question",
                    "category": "fears",
                    "question_number": fear_index + 1,
                    "question": EMPATHY_QUESTIONS["fears"][fear_index],
                    "category_title": "FEARS & ANXIETIES (What they are afraid of)",
                    "progress": {"current": current_progress + 1, "total": 8},
                    "responses": responses
                }
            elif current_progress < 8:  # Move to influences
                influence_index = current_progress - 6
                return {
                    "mcp_tool": "empathy_map_inquiry",
                    "stage": "question",
                    "category": "influences", 
                    "question_number": influence_index + 1,
                    "question": EMPATHY_QUESTIONS["influences"][influence_index],
                    "category_title": "EXTERNAL INFLUENCES (What shapes their thinking)",
                    "progress": {"current": current_progress + 1, "total": 8},
                    "responses": responses
                }
            else:  # Complete
                await save_empathy_data("inquiry", responses)
                return {
                    "mcp_tool": "empathy_map_inquiry",
                    "stage": "complete",
                    "responses": responses,
                    "message": "Excellent work! You've completed the inquiry phase. Ready to create your empathy map.",
                    "timestamp": datetime.now().isoformat()
                }
        
    except Exception as e:
        logger.error(f"Empathy inquiry error: {e}")
        return {"mcp_tool": "empathy_map_inquiry", "error": str(e)}

async def empathy_map_synthesis_tool(arguments: dict) -> dict:
    """Stage 3: Create the visual empathy map"""
    try:
        person_data = arguments.get("person_data", {})
        responses = arguments.get("inquiry_responses", [])
        
        # Analyze responses using AI
        analysis_prompt = f"""
        Analyze these empathy mapping responses about {person_data.get('person_name', 'this person')}:
        
        {json.dumps(responses, indent=2)}
        
        Create an empathy map with these 4 quadrants:
        1. HOPES & VALUES: What they want/value most
        2. FEARS & ANXIETIES: What they're afraid of
        3. EXTERNAL INFLUENCES: What shapes their thinking
        4. THE UNSPOKEN CORE: The central driving emotion behind everything
        
        Format as structured data with bullet points for each quadrant.
        Also provide a one-sentence "AI Insight" about their primary motivation.
        """
        
        ai_response = model.generate_content(analysis_prompt)
        ai_analysis = ai_response.text.strip()
        
        # Create structured empathy map
        empathy_map = {
            "person_name": person_data.get("person_name"),
            "conversation_goal": person_data.get("conversation_goal"),
            "quadrants": {
                "hopes_values": [],
                "fears_anxieties": [],
                "external_influences": [],
                "unspoken_core": ""
            },
            "ai_insight": "",
            "raw_analysis": ai_analysis,
            "created_at": datetime.now().isoformat()
        }
        
        # Save empathy map
        await save_empathy_data("empathy_map", empathy_map)
        
        return {
            "mcp_tool": "empathy_map_synthesis",
            "empathy_map": empathy_map,
            "visual_ready": True,
            "message": "Your empathy map has been created! This reveals the deeper motivations and fears driving their perspective.",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Empathy synthesis error: {e}")
        return {"mcp_tool": "empathy_map_synthesis", "error": str(e)}

async def empathy_map_strategy_tool(arguments: dict) -> dict:
    """Stage 4: Convert insights into conversational strategy"""
    try:
        empathy_map = arguments.get("empathy_map", {})
        goal = arguments.get("conversation_goal")
        person_name = empathy_map.get("person_name", "them")
        
        strategy_prompt = f"""
        Based on this empathy map for {person_name} and the goal: "{goal}"
        
        Empathy Map: {json.dumps(empathy_map, indent=2)}
        
        Provide strategic conversation guidance:
        1. BRIDGE: What common ground do you share?
        2. EMPATHY-FIRST OPENING: A suggested conversation starter that acknowledges their core fears
        3. OBJECTION PREPARATION: Likely counter-arguments and thoughtful responses
        4. KEY TALKING POINTS: 3-4 main points that align with their values
        
        Be specific and actionable. Focus on building understanding, not winning arguments.
        """
        
        ai_response = model.generate_content(strategy_prompt)
        strategy_guidance = ai_response.text.strip()
        
        strategy = {
            "empathy_map_id": empathy_map.get("created_at"),
            "conversation_goal": goal,
            "strategy_guidance": strategy_guidance,
            "created_at": datetime.now().isoformat()
        }
        
        # Save strategy
        await save_empathy_data("strategy", strategy)
        
        return {
            "mcp_tool": "empathy_map_strategy",
            "strategy": strategy,
            "guidance": strategy_guidance,
            "ready_for_conversation": True,
            "message": "Your strategic conversation plan is ready! You now have the insights and approach to have a meaningful, empathetic dialogue.",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Empathy strategy error: {e}")
        return {"mcp_tool": "empathy_map_strategy", "error": str(e)}

async def save_empathy_data(data_type: str, data: dict):
    """Save empathy mapping data to cloud storage"""
    try:
        bucket = storage_client.bucket(bucket_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"empathy_maps/{timestamp}_{data_type}.json"
        
        empathy_data = {
            "timestamp": datetime.now().isoformat(),
            "mcp_version": "1.0.0",
            "data_type": data_type,
            "data": data
        }
        
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(empathy_data, indent=2))
        logger.info(f"Empathy data saved: {filename}")
        
    except Exception as e:
        logger.error(f"Failed to save empathy data: {e}")


FUTURE_SELF_QUESTIONS = [
    {
        "id": 1,
        "question": "Let's start with the big picture. In one sentence, describe the future self you're working towards.",
        "placeholder": "e.g., A successful freelance photographer living in Tokyo, specializing in street fashion",
        "category": "identity"
    },
    {
        "id": 2,
        "question": "Where is this future you? Describe the vibe of your home or workspace.",
        "placeholder": "e.g., A small, minimalist apartment with large windows and organized equipment",
        "category": "environment"
    },
    {
        "id": 3,
        "question": "What three words best describe the feeling of your ideal day?",
        "placeholder": "e.g., Creative, Independent, Inspired",
        "category": "feeling"
    },
    {
        "id": 4,
        "question": "Beyond work, what's a small, meaningful activity that's part of your daily routine?",
        "placeholder": "e.g., Starting my day with a quiet hour at a local coffee shop",
        "category": "rituals"
    },
    {
        "id": 5,
        "question": "What is one skill you've mastered in this future that you're proud of?",
        "placeholder": "e.g., I've become fluent in conversational Japanese",
        "category": "accomplishment"
    }
]

async def future_self_input_tool(arguments: dict) -> dict:
    """Stage 1: Collect structured inputs for future self simulation"""
    try:
        stage = arguments.get("stage")
        responses = arguments.get("responses", [])
        
        if stage == "start":
            # Return first question
            return {
                "mcp_tool": "future_self_input",
                "stage": "question",
                "current_question": FUTURE_SELF_QUESTIONS[0],
                "progress": {"current": 1, "total": len(FUTURE_SELF_QUESTIONS)},
                "intro_message": "Let's build a vivid simulation of your future self. The more detailed you are, the more powerful the experience will be.",
                "timestamp": datetime.now().isoformat()
            }
            
        elif stage == "answer":
            question_id = arguments.get("question_id", 1)
            answer = arguments.get("answer")
            
            # Record the response
            new_response = {
                "question_id": question_id,
                "question": FUTURE_SELF_QUESTIONS[question_id-1]["question"],
                "category": FUTURE_SELF_QUESTIONS[question_id-1]["category"],
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            }
            responses.append(new_response)
            
            # Check if more questions
            next_question_id = question_id + 1
            if next_question_id <= len(FUTURE_SELF_QUESTIONS):
                return {
                    "mcp_tool": "future_self_input",
                    "stage": "question",
                    "current_question": FUTURE_SELF_QUESTIONS[next_question_id-1],
                    "progress": {"current": next_question_id, "total": len(FUTURE_SELF_QUESTIONS)},
                    "responses": responses,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # All questions complete
                await save_future_data("input", responses)
                return {
                    "mcp_tool": "future_self_input",
                    "stage": "complete",
                    "responses": responses,
                    "message": "Perfect! Ready to generate your future self simulation.",
                    "timestamp": datetime.now().isoformat()
                }
        
    except Exception as e:
        logger.error(f"Future self input error: {e}")
        return {"mcp_tool": "future_self_input", "error": str(e)}

async def future_self_generation_tool(arguments: dict) -> dict:
    """Stage 2: Generate narrative and visual content"""
    try:
        user_inputs = arguments.get("user_inputs", [])
        
        # Extract key elements from inputs
        identity = next((r["answer"] for r in user_inputs if r["category"] == "identity"), "")
        environment = next((r["answer"] for r in user_inputs if r["category"] == "environment"), "")
        feelings = next((r["answer"] for r in user_inputs if r["category"] == "feeling"), "")
        rituals = next((r["answer"] for r in user_inputs if r["category"] == "rituals"), "")
        skill = next((r["answer"] for r in user_inputs if r["category"] == "accomplishment"), "")
        
        # Generate image prompt
        image_prompt = f"cinematic photo, {environment}. The mood is {feelings}. High detail, photorealistic, inspiring atmosphere, natural lighting."
        
        # Generate narrative using AI
        narrative_prompt = f"""
        You are an inspiring storyteller. Write a vivid, first-person "Day in the Life" story (250-300 words) for someone who is: {identity}
        
        Environment: {environment}
        Daily ritual: {rituals}
        Key skill: {skill}
        Mood/feeling: {feelings}
        
        Requirements:
        - Use rich, sensory details
        - Write in first person present tense
        - Include the daily ritual and mention the skill naturally
        - Capture the feeling words throughout
        - End with a sense of fulfillment and purpose
        - Make it feel achievable yet inspiring
        - Bold key phrases that connect to their inputs
        """
        
        ai_response = model.generate_content(narrative_prompt)
        generated_story = ai_response.text.strip()
        
        # Create simulation package
        simulation = {
            "identity": identity,
            "environment": environment,
            "feelings": feelings,
            "rituals": rituals,
            "skill": skill,
            "generated_story": generated_story,
            "image_prompt": image_prompt,
            "user_inputs": user_inputs,
            "created_at": datetime.now().isoformat()
        }
        
        await save_future_data("simulation", simulation)
        
        return {
            "mcp_tool": "future_self_generation",
            "simulation": simulation,
            "ready_for_experience": True,
            "message": "Your future self simulation has been created! Ready to experience your day in the life.",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Future self generation error: {e}")
        return {"mcp_tool": "future_self_generation", "error": str(e)}

async def future_self_experience_tool(arguments: dict) -> dict:
    """Stage 3: Present the immersive simulation"""
    try:
        generated_content = arguments.get("generated_content", {})
        
        # Create experience package
        experience = {
            "simulation_id": generated_content.get("created_at"),
            "immersive_story": generated_content.get("generated_story"),
            "visual_description": generated_content.get("image_prompt"),
            "identity_summary": generated_content.get("identity"),
            "experience_ready": True,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "mcp_tool": "future_self_experience",
            "experience": experience,
            "message": "Welcome to your future. Take your time experiencing this day in your life.",
            "next_step": "integration",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Future self experience error: {e}")
        return {"mcp_tool": "future_self_experience", "error": str(e)}

async def future_self_integration_tool(arguments: dict) -> dict:
    """Stage 4: Connect future vision to present actions"""
    try:
        future_vision = arguments.get("future_vision", {})
        commitment = arguments.get("commitment", "")
        
        # Generate personalized action guidance
        action_prompt = f"""
        Based on this future vision: {future_vision.get('identity_summary', '')}
        
        The user committed to: "{commitment}"
        
        Provide encouraging, specific guidance for their first step. Include:
        1. Why this commitment is perfect for moving toward their future
        2. How to make it a sustainable habit
        3. What to focus on this week
        
        Keep it motivating and actionable (2-3 sentences).
        """
        
        ai_response = model.generate_content(action_prompt)
        action_guidance = ai_response.text.strip()
        
        # Create integration package
        integration = {
            "future_vision": future_vision,
            "user_commitment": commitment,
            "ai_guidance": action_guidance,
            "created_at": datetime.now().isoformat()
        }
        
        await save_future_data("integration", integration)
        
        return {
            "mcp_tool": "future_self_integration",
            "integration": integration,
            "guidance": action_guidance,
            "message": "Your future self simulation is complete! You now have a clear vision and your first step forward.",
            "simulation_saved": True,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Future self integration error: {e}")
        return {"mcp_tool": "future_self_integration", "error": str(e)}

async def save_future_data(data_type: str, data: dict):
    """Save future self simulation data to cloud storage"""
    try:
        bucket = storage_client.bucket(bucket_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"future_simulations/{timestamp}_{data_type}.json"
        
        future_data = {
            "timestamp": datetime.now().isoformat(),
            "mcp_version": "1.0.0",
            "data_type": data_type,
            "data": data
        }
        
        blob = bucket.blob(filename)
        blob.upload_from_string(json.dumps(future_data, indent=2))
        logger.info(f"Future simulation data saved: {filename}")
        
    except Exception as e:
        logger.error(f"Failed to save future simulation data: {e}")

# Dialogue Gym scenario library
DIALOGUE_SCENARIOS = {
    "assertiveness": {
        "zone_name": "Assertiveness Zone",
        "description": "Practice setting boundaries and saying 'no' confidently",
        "scenarios": [
            {
                "id": "assert_1",
                "title": "Friend Wants to Borrow Money",
                "situation": "Your friend asks to borrow $200 that you're not comfortable lending",
                "goal": "Decline the request firmly but kindly, preserving the friendship",
                "difficulty": "Medium",
                "persona_prompt": "You are Alex, a close friend who is stressed about finances. You need $200 urgently and hope your friend will help. Be friendly but persistent. Express disappointment if they refuse, but don't get angry.",
                "opening_line": "Hey! I'm in a really tight spot right now. Could you possibly lend me $200? I promise I'll pay you back next month."
            },
            {
                "id": "assert_2", 
                "title": "Family Member's Critical Comment",
                "situation": "Your family member makes a critical comment about your life choices",
                "goal": "Address the criticism while maintaining respect and setting a boundary",
                "difficulty": "Hard",
                "persona_prompt": "You are a concerned family member who thinks the user is making poor life choices. You care about them but tend to be critical. Defend your position if challenged.",
                "opening_line": "I just don't understand why you're wasting your potential on this path. You could be doing so much better."
            }
        ]
    },
    "reaching_out": {
        "zone_name": "Reaching Out Zone", 
        "description": "Practice asking for help and support",
        "scenarios": [
            {
                "id": "reach_1",
                "title": "Ask Professor for Extension",
                "situation": "You need to email your professor for a deadline extension due to personal reasons",
                "goal": "Request extension professionally while providing appropriate context",
                "difficulty": "Medium",
                "persona_prompt": "You are Professor Johnson, a understanding but busy academic. You want to help students but need clear, concise requests. You appreciate honesty and professionalism.",
                "opening_line": "Hello, I received your email about needing an extension. Can you tell me more about your situation?"
            }
        ]
    },
    "social_connection": {
        "zone_name": "Social Connection Zone",
        "description": "Practice building friendships and social skills", 
        "scenarios": [
            {
                "id": "social_1",
                "title": "Small Talk with Classmate",
                "situation": "Making conversation with a new classmate before lecture begins",
                "goal": "Create a friendly connection and find common ground",
                "difficulty": "Easy",
                "persona_prompt": "You are Jamie, a friendly classmate who is open to chatting but not overly talkative. Respond naturally to conversation attempts.",
                "opening_line": "Oh hey, you're in my statistics class too, right? How are you finding it so far?"
            }
        ]
    },
    "heart_to_heart": {
        "zone_name": "Heart-to-Heart Zone",
        "description": "Practice vulnerable and significant conversations",
        "scenarios": [
            {
                "id": "heart_1", 
                "title": "Mental Health Disclosure",
                "situation": "Telling a close friend about your mental health struggles",
                "goal": "Share vulnerably while asking for appropriate support",
                "difficulty": "Hard",
                "persona_prompt": "You are Sam, a caring friend who wants to be supportive but isn't sure how to respond to mental health topics. Be empathetic but realistic.",
                "opening_line": "You seem to have something on your mind lately. Is everything okay?"
            }
        ]
    }
}

async def dialogue_gym_scenarios_tool(arguments: dict) -> dict:
    """Get workout zones and scenarios for dialogue practice"""
    try:
        action = arguments.get("action")
        zone = arguments.get("zone")
        
        if action == "list_zones":
            zones = []
            for zone_id, zone_data in DIALOGUE_SCENARIOS.items():
                zones.append({
                    "id": zone_id,
                    "name": zone_data["zone_name"],
                    "description": zone_data["description"],
                    "scenario_count": len(zone_data["scenarios"])
                })
            
            return {
                "mcp_tool": "dialogue_gym_scenarios",
                "action": "list_zones",
                "zones": zones,
                "timestamp": datetime.now().isoformat()
            }
            
        elif action == "get_scenarios" and zone:
            if zone in DIALOGUE_SCENARIOS:
                zone_data = DIALOGUE_SCENARIOS[zone]
                return {
                    "mcp_tool": "dialogue_gym_scenarios", 
                    "action": "get_scenarios",
                    "zone": zone,
                    "zone_name": zone_data["zone_name"],
                    "scenarios": zone_data["scenarios"],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {"mcp_tool": "dialogue_gym_scenarios", "error": "Zone not found"}
        
    except Exception as e:
        logger.error(f"Dialogue gym scenarios error: {e}")
        return {"mcp_tool": "dialogue_gym_scenarios", "error": str(e)}

async def dialogue_gym_persona_tool(arguments: dict) -> dict:
    """AI persona agent for role-playing"""
    try:
        scenario_id = arguments.get("scenario_id")
        user_message = arguments.get("user_message")
        conversation_history = arguments.get("conversation_history", [])
        turn_number = arguments.get("turn_number", 1)
        
        # Find scenario data
        scenario_data = None
        for zone_data in DIALOGUE_SCENARIOS.values():
            for scenario in zone_data["scenarios"]:
                if scenario["id"] == scenario_id:
                    scenario_data = scenario
                    break
        
        if not scenario_data:
            return {"mcp_tool": "dialogue_gym_persona", "error": "Scenario not found"}
        
        # Build persona prompt with conversation context
        context_prompt = f"""
        {scenario_data['persona_prompt']}
        
        Scenario: {scenario_data['situation']}
        
        Conversation so far: {conversation_history[-3:] if conversation_history else 'This is the start'}
        
        The user just said: "{user_message}"
        
        Respond as your character would, keeping the conversation realistic and engaging. 
        Don't break character. Keep responses to 1-2 sentences.
        """
        
        # Generate persona response
        ai_response = model.generate_content(context_prompt)
        persona_reply = ai_response.text.strip()
        
        return {
            "mcp_tool": "dialogue_gym_persona",
            "scenario_id": scenario_id,
            "persona_response": persona_reply,
            "turn_number": turn_number,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Dialogue gym persona error: {e}")
        return {"mcp_tool": "dialogue_gym_persona", "error": str(e)}

async def dialogue_gym_coach_tool(arguments: dict) -> dict:
    """AI coach providing real-time feedback"""
    try:
        scenario_goal = arguments.get("scenario_goal")
        user_message = arguments.get("user_message") 
        persona_message = arguments.get("persona_message", "")
        
        coach_prompt = f"""
        You are an expert communication coach. Analyze this response:
        
        GOAL: {scenario_goal}
        CONTEXT: The other person said: "{persona_message}"
        USER RESPONSE: "{user_message}"
        
        Provide ONE sentence of concise, actionable feedback. Focus on:
        - How well they're meeting the goal
        - Specific communication techniques (I-statements, empathy, clarity)
        - What to improve or what they did well
        
        Start with "Good!" or "Try:" and keep it under 20 words.
        """
        
        ai_response = model.generate_content(coach_prompt)
        coach_feedback = ai_response.text.strip()
        
        return {
            "mcp_tool": "dialogue_gym_coach",
            "feedback": coach_feedback,
            "user_message": user_message,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Dialogue gym coach error: {e}")
        return {"mcp_tool": "dialogue_gym_coach", "error": str(e)}

async def dialogue_gym_analysis_tool(arguments: dict) -> dict:
    """Post-workout performance analysis"""
    try:
        scenario_data = arguments.get("scenario_data", {})
        conversation_history = arguments.get("conversation_history", [])
        coach_feedback = arguments.get("coach_feedback", [])
        
        analysis_prompt = f"""
        Analyze this dialogue practice session:
        
        SCENARIO: {scenario_data.get('title', '')} - {scenario_data.get('goal', '')}
        CONVERSATION: {conversation_history}
        COACH FEEDBACK: {coach_feedback}
        
        Provide:
        1. Performance ratings (1-5 stars) for: Clarity, Empathy, Goal Achievement
        2. Key strengths (what they did well)
        3. Growth areas (what to improve) 
        4. One specific alternative phrase they could have used
        
        Keep it encouraging and actionable.
        """
        
        ai_response = model.generate_content(analysis_prompt)
        analysis = ai_response.text.strip()
        
        return {
            "mcp_tool": "dialogue_gym_analysis",
            "scenario": scenario_data,
            "performance_analysis": analysis,
            "conversation_length": len(conversation_history),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Dialogue gym analysis error: {e}")
        return {"mcp_tool": "dialogue_gym_analysis", "error": str(e)}


async def main():
    """Run the MCP server"""
    # Initialize services
    initialize_services()
    
    # Create server options
    options = InitializationOptions(
        server_name="youth-wellness-mcp",
        server_version="1.0.0",
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={}
        )
    )
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Youth Mental Wellness MCP Server starting...")
        await server.run(
            read_stream,
            write_stream,
            options
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
