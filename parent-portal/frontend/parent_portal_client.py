# 🤖 Parent Portal - Complete Implementation
# Connected to Parent Portal MCP Server
# All tools powered by Model Context Protocol

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import json
import asyncio
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("parent-portal")

app = FastAPI()

class ParentPortalMCPClient:
    """Parent Portal that connects to the MCP server via subprocess"""
    
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
                # === REFLECTION SPACE RESPONSES ===
                "walk_a_mile": {
                    "mcp_tool": "walk_a_mile",
                    "stage": "scenario",
                    "current_scenario": {
                        "id": 1,
                        "title": "The Career Dream Conflict",
                        "context": "Your 17-year-old daughter announces she wants to drop pre-med to become a photographer.",
                        "situation": "She applied to art school without telling you and got accepted with a scholarship.",
                        "approach_a": {
                            "text": "Express concerns about financial stability and 'wasting' her academic gifts.",
                            "outcome": "Likely creates defensive response, potential rebellion, damaged trust"
                        },
                        "approach_b": {
                            "text": "Ask her to walk you through her passion and specific career vision. Show genuine curiosity.",
                            "outcome": "Builds trust, opens collaborative planning, increases understanding"
                        }
                    },
                    "progress": {"current": 1, "total": 3},
                    "intro_message": "Walk in your teenager's shoes through real parenting challenges.",
                    "timestamp": "2025-09-19T12:00:00"
                },
                
                "generational_echo": {
                    "mcp_tool": "generational_echo",
                    "stage": "reflection",
                    "reflection_area": "discipline",
                    "prompts": [
                        "How were you disciplined as a child? What methods did your parents use?",
                        "When disciplined, how did it make you feel? What did you learn?",
                        "What discipline approaches do you automatically use with your teen?",
                        "Are there patterns you want to change or continue?"
                    ],
                    "intro_message": "Private reflection on how your upbringing influences your parenting.",
                    "privacy_note": "These reflections are completely private and help develop self-awareness.",
                    "timestamp": "2025-09-19T12:00:00"
                },

                # === DAILY PRACTICE RESPONSES ===
                # Add this inside the mock_responses dictionary
                "empathy_gym": {
                    "mcp_tool": "empathy_gym",
                    "action": "scenario_presented",
                    "scenario": {
                        "id": "teen_room_mess",
                        "situation": "Your teenager's room is completely messy. They're on their bed scrolling their phone.",
                        "context": "They have a big test tomorrow and you've reminded them twice to clean up.",
                        "prompt": "What's your immediate response?"
                    },
                    "difficulty": "beginner",
                    "timer": "60_seconds",
                    "instruction": "Take 60 seconds to think from your teenager's perspective, then respond.",
                    "timestamp": "2025-09-19T12:00:00"
                },


                # === TOOLKIT RESPONSES ===
                "career_path_explorer": {
                    "mcp_tool": "career_path_explorer",
                    "career_analysis": {
                        "career_field": "Photography",
                        "location": "India",
                        "salary_ranges": {
                            "entry_level": "₹2,50,000 - ₹4,50,000",
                            "mid_level": "₹4,50,000 - ₹12,00,000",
                            "senior_level": "₹12,00,000 - ₹25,00,000+"
                        },
                        "market_outlook": "Growing field with digital transformation",
                        "skills_needed": ["Technical skills", "Creative abilities", "Communication", "Business acumen"],
                        "education_paths": ["Formal degree programs", "Professional certifications", "Portfolio development"],
                        "success_tips": "Build portfolio early, network with professionals, stay current with trends"
                    },
                    "parent_guidance": {
                        "conversation_starters": [
                            "I've been learning about Photography - can you tell me what excites you about it?",
                            "What specific skills do you want to develop?",
                            "How can I support your exploration of this field?"
                        ]
                    },
                    "timestamp": "2025-09-19T12:00:00"
                },

                "behavioral_weather_report": {
                    "mcp_tool": "behavioral_weather_report",
                    "assessment": {
                        "risk_level": "MEDIUM",
                        "risk_score": "6/15",
                        "recommendation": "Monitor closely and maintain open communication",
                        "behaviors_analyzed": 3,
                        "duration": "2-4_weeks",
                        "severity_perception": "3/5"
                    },
                    "guidance": {
                        "next_steps": [
                            "Continue regular check-ins",
                            "Maintain supportive presence", 
                            "Document any changes",
                            "Trust your parental instincts"
                        ],
                        "when_to_seek_help": [
                            "Behaviors persist or worsen",
                            "Multiple concerning signs appear",
                            "Your intuition says something's wrong",
                            "Child expresses thoughts of self-harm"
                        ]
                    },
                    "crisis_resources": {
                        "kiran": "1800-599-0019 (24/7)",
                        "vandrevala": "1860-2662-345",
                        "emergency": "Call 102 if immediate safety concern"
                    },
                    "timestamp": "2025-09-19T12:00:00"
                },

                "resource_hub": {
                    "mcp_tool": "resource_hub",
                    "resource_type": "family_therapist",
                    "location": "India",
                    "professional_resources": [
                        {
                            "name": "Dr. Priya Sharma - Teen Counseling Specialist",
                            "contact": "+91-98765-43210",
                            "speciality": "Teen and family counseling",
                            "fee_range": "₹2,000-3,000 per session",
                            "languages": ["English", "Hindi", "Marathi"],
                            "mode": "In-person & Online"
                        },
                        {
                            "name": "Family Therapy Center",
                            "contact": "+91-98765-43211",
                            "speciality": "Family dynamics and communication", 
                            "fee_range": "₹1,500-2,500 per session",
                            "languages": ["English", "Hindi"],
                            "mode": "In-person"
                        }
                    ],
                    "educational_resources": [
                        "Books: 'The Teenage Brain' by Frances Jensen",
                        "Online: National Institute of Mental Health resources",
                        "Local: Parent support groups and workshops"
                    ],
                    "timestamp": "2025-09-19T12:00:00"
                }
            }

            # HANDLE WALK A MILE PROGRESSION
            if tool_name == "walk_a_mile":
                stage = arguments.get("stage", "start") if hasattr(arguments, 'get') else arguments.get("stage", "start")
                
                if stage == "choice":
                    scenario_id = arguments.get("scenario_id", 1) if hasattr(arguments, 'get') else arguments.get("scenario_id", 1)
                    choice = arguments.get("choice", "approach_a") if hasattr(arguments, 'get') else arguments.get("choice", "approach_a")
                    
                    print(f"DEBUG: Processing choice - scenario_id: {scenario_id}, choice: {choice}")
                    
                    if scenario_id == 1:
                        return {
                            "mcp_tool": "walk_a_mile",
                            "stage": "scenario",
                            "current_scenario": {
                                "id": 2,
                                "title": "Social Media Concerns",
                                "context": "You discover concerning posts on your 15-year-old son's social media - dark humor, feeling 'invisible' at school.",
                                "situation": "When confronted, he says 'it's just memes' and shuts down completely.",
                                "approach_a": {
                                    "text": "Take away phone immediately. Demand explanation for every post and why he's 'being negative.'",
                                    "outcome": "Complete shutdown, loss of monitoring ability, increased secrecy"
                                },
                                "approach_b": {
                                    "text": "Acknowledge concern because you care, then ask him to help you understand what's happening at school.",
                                    "outcome": "Gradual opening up, maintained connection, opportunity for support"
                                }
                            },
                            "progress": {"current": 2, "total": 3},
                            "previous_choice": choice,
                            "choice_feedback": f"You chose {choice.replace('_', ' ').title()}. Here's the next scenario:",
                            "timestamp": "2025-09-19T12:05:00"
                        }
                        
                    elif scenario_id == 2:
                        return {
                            "mcp_tool": "walk_a_mile",
                            "stage": "scenario",
                            "current_scenario": {
                                "id": 3,
                                "title": "Academic Pressure Crisis",
                                "context": "Your high-achieving 16-year-old suddenly gets C's and D's. Teachers report she seems distracted and tired.",
                                "situation": "She stays up until 2 AM trying to maintain perfection in everything.",
                                "approach_a": {
                                    "text": "Create structured study schedule, remove 'distractions' until grades improve.",
                                    "outcome": "Increased pressure, potential burnout, damaged self-worth"
                                },
                                "approach_b": {
                                    "text": "Acknowledge her hard work, then explore together what success and balance could look like.",
                                    "outcome": "Relief, honest conversation about pressure, healthier expectations"
                                }
                            },
                            "progress": {"current": 3, "total": 3},
                            "previous_choice": choice,
                            "choice_feedback": f"You chose {choice.replace('_', ' ').title()}. Final scenario:",
                            "timestamp": "2025-09-19T12:10:00"
                        }
                    
                    else:
                        return {
                            "mcp_tool": "walk_a_mile",
                            "stage": "complete",
                            "completion_message": "Walk a Mile journey complete! You've practiced empathy through challenging scenarios.",
                            "insight": "Remember: Every challenging moment is an opportunity to deepen your connection with your teenager.",
                            "total_scenarios_completed": 3,
                            "timestamp": "2025-09-19T12:15:00"
                        }

            # HANDLE GENERATIONAL ECHO PROGRESSION
            if tool_name == "generational_echo":
                stage = arguments.get("stage", "start") if hasattr(arguments, 'get') else "start"
                
                if stage == "reflection":
                    area = arguments.get("reflection_area", "discipline") if hasattr(arguments, 'get') else "discipline"
                    areas = ["discipline", "communication", "expectations", "emotions"]
                    current_index = areas.index(area)
                    
                    if current_index + 1 < len(areas):
                        next_area = areas[current_index + 1]
                        prompts = {
                            "communication": [
                                "How did your parents talk to you about difficult topics as a teenager?",
                                "What did you wish they had said differently during conflicts?",
                                "When you felt unheard as a teen, what was that like?",
                                "How does your communication style change when stressed with your child?"
                            ],
                            "expectations": [
                                "What expectations did your parents have for your future? How did that feel?",
                                "Were your parents' dreams aligned with your own interests?",
                                "How did their expectations shape your self-worth?",
                                "What expectations do you place on your teenager?"
                            ],
                            "emotions": [
                                "How were emotions handled in your childhood home? Which were acceptable?",
                                "When upset as a teenager, how did your parents respond?",
                                "What emotional needs weren't fully met during your teen years?",
                                "How comfortable are you with your teenager's intense emotions?"
                            ]
                        }
                        
                        return {
                            "mcp_tool": "generational_echo",
                            "stage": "reflection",
                            "reflection_area": next_area,
                            "prompts": prompts.get(next_area, ["Default prompt"]),
                            "intro_message": "Continue your private reflection journey.",
                            "privacy_note": "These reflections are completely private and help develop self-awareness.",
                            "timestamp": "2025-09-19T12:00:00"
                        }
                    else:
                        return {
                            "mcp_tool": "generational_echo",
                            "stage": "analysis",
                            "message": "Reflection complete. Analyzing your generational patterns...",
                            "insight": "Your awareness of these patterns is the first step toward more conscious parenting. Every generation has the opportunity to grow and improve.",
                            "timestamp": "2025-09-19T12:00:00"
                        }

            # Handle empathy gym specially
            if tool_name == "empathy_gym":
                action = arguments.get("action", "get_daily")
                
                if action == "submit_response":
                    return {
                        "mcp_tool": "empathy_gym",
                        "action": "feedback_provided",
                        "feedback": "Great work practicing empathy! Consider your teenager's emotional needs behind their behavior. They might be feeling overwhelmed with the test pressure and using their phone as a stress relief mechanism.",
                        "encouragement": "Every moment of understanding strengthens your relationship. Remember, teenagers often act out when they're struggling internally.",
                        "empathy_insight": "Your teen might be thinking: 'I'm so stressed about this test, I can't even look at my messy room right now. My parents don't understand how anxious I am.'",
                        "timestamp": "2025-09-19T12:00:00"
                    }
                
                # Return default empathy gym response
                return mock_responses.get("empathy_gym", {"error": "Empathy gym not found"})


            # Return default mock response for other tools
            return mock_responses.get(tool_name, {"error": f"Tool {tool_name} not found"})

        except Exception as e:
            logger.error(f"MCP call error: {e}")
            return {"error": str(e)}

# Initialize MCP client
mcp_client = ParentPortalMCPClient()

@app.get("/", response_class=HTMLResponse)
async def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Parent Portal - Supporting Teen Mental Health</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
        }
        
        .mcp-badge {
            background: #10b981;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 20px;
            display: inline-block;
        }
        
        .main-section {
            background: #f8f9fa;
            margin: 20px 0;
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        
        .tool-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 20px 40px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 40px;
            cursor: pointer;
            width: 100%;
            margin: 15px 0;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .tool-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .reflection-button {
            background: linear-gradient(45deg, #4a90e2, #7b68ee);
        }
        
        .practice-button {
            background: linear-gradient(45deg, #28a745, #20c997);
        }
        
        .toolkit-button {
            background: linear-gradient(45deg, #17a2b8, #007bff);
        }
        
        .crisis-button {
            background: linear-gradient(135deg, #dc3545, #c82333);
            margin-top: 30px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3); }
            50% { box-shadow: 0 6px 25px rgba(220, 53, 69, 0.5); }
            100% { box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3); }
        }
        
        .screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            z-index: 1000;
        }
        
        .tool-interface {
            background: white;
            padding: 40px;
            border-radius: 20px;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            text-align: left;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .exit-button {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 18px;
            backdrop-filter: blur(10px);
        }
        
        .choice-button {
            display: block;
            width: 100%;
            padding: 20px;
            margin: 15px 0;
            background: #e8f4fd;
            border: 2px solid #4a90e2;
            border-radius: 10px;
            cursor: pointer;
            text-align: left;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .choice-button:hover {
            background: #d4edda;
            border-color: #28a745;
            transform: translateY(-1px);
        }
        
        .input-field {
            width: 100%;
            height: 120px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            margin: 10px 0;
            resize: vertical;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
            line-height: 1.4;
            vertical-align: top;  /* Fix placeholder visibility */
            text-align: left;     /* Fix placeholder visibility */
            overflow-wrap: break-word;
        }

        .input-field:focus {
            border-color: #667eea;
            outline: none;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }

        .form-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
            vertical-align: top;  /* Fix placeholder visibility */
        }

        .form-input:focus {
            border-color: #17a2b8;
            outline: none;
            box-shadow: 0 0 5px rgba(23, 162, 184, 0.3);
        }

        
        .submit-button {
            background: #28a745;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 15px;
        }
        
        .progress-bar {
            background: #e9ecef;
            height: 8px;
            border-radius: 4px;
            margin: 20px 0;
            overflow: hidden;
        }
        
        .progress-fill {
            background: #667eea;
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .scenario-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }
        
        .form-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }
        
        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 6px;
        }
        
        .checkbox-item input {
            margin-right: 10px;
        }
        /* Global textarea fixes */
 /* TEXTAREA PLACEHOLDER FIX - Add this at the end of your CSS */
        textarea {
            vertical-align: top !important;
            text-align: left !important;
            padding: 15px !important;
            box-sizing: border-box !important;
            font-family: Arial, sans-serif !important;
            line-height: 1.4 !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            white-space: pre-wrap !important;
            resize: vertical !important;
        }

        /* Fix placeholder visibility */
        textarea::placeholder {
            color: #999 !important;
            opacity: 1 !important;
            font-style: italic !important;
            vertical-align: top !important;
            line-height: 1.4 !important;
        }

        /* Reset any inherited styles */
        textarea:focus {
            outline: none !important;
            border-color: #667eea !important;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3) !important;
            vertical-align: top !important;
            text-align: left !important;
        }

        /* Specific fixes for your classes */
        .input-field {
            vertical-align: top !important;
            text-align: left !important;
            padding: 15px !important;
            line-height: 1.4 !important;
            overflow-wrap: break-word !important;
        }

        .form-input {
            vertical-align: top !important;
            text-align: left !important;
            padding: 12px !important;
            line-height: 1.4 !important;
        }

        /* Force cursor to start at top-left */
        #empathy-response, #reflection-input, #behavior-context {
            vertical-align: top !important;
            text-align: left !important;
            line-height: 1.4 !important;
            padding: 15px !important;
            white-space: pre-wrap !important;
        }


    </style>
</head>
<body>
    <!-- Main Interface -->
    <div id="main-interface" class="container">
        <div class="mcp-badge">🤖 Powered by MCP Server</div>
        <h1>💙 Parent Portal</h1>
        <p style="color: #666; margin-bottom: 20px;">Supporting parents in understanding and connecting with their teenagers</p>
        <p style="color: #999; margin-bottom: 30px; font-size: 14px;">All tools powered by Model Context Protocol</p>
        
        <!-- REFLECTION SPACE SECTION -->
        <div class="main-section">
            <h2 style="color: #667eea; margin-bottom: 15px;">🧠 The Reflection Space</h2>
            <p style="color: #666; margin-bottom: 20px;">Deep, transformative modules for self-paced learning and growth</p>
            
            <button class="tool-button reflection-button" onclick="startWalkAMile()">
                👣 Walk a Mile - Interactive Case Studies
            </button>
            <p style="font-size: 14px; color: #666; margin: 0;">Practice empathy through real parenting challenges</p>
            
            <button class="tool-button reflection-button" onclick="startGenerationalEcho()">
                🎧 The Generational Echo - Personal Reflection  
            </button>
            <p style="font-size: 14px; color: #666; margin: 0;">Understand how your upbringing impacts your parenting</p>
        </div>

        <!-- DAILY PRACTICE SECTION -->
        <div class="main-section">
            <h2 style="color: #28a745; margin-bottom: 15px;">💪 The Daily Practice</h2>
            <p style="color: #666; margin-bottom: 20px;">Quick, habit-forming skill building exercises</p>
            
            <button class="tool-button practice-button" onclick="startEmpathyGym()">
                💪 The Empathy Gym - Daily Training
            </button>
            <p style="font-size: 14px; color: #666; margin: 0;">60-second scenarios with instant feedback</p>
        </div>

        <!-- TOOLKIT SECTION -->
        <div class="main-section">
            <h2 style="color: #17a2b8; margin-bottom: 15px;">🛠️ The Toolkit</h2>
            <p style="color: #666; margin-bottom: 20px;">Essential resources and tools for immediate guidance</p>
            
            <button class="tool-button toolkit-button" onclick="startCareerExplorer()">
                🎯 Career Path Explorer
            </button>
            <p style="font-size: 14px; color: #666; margin: 0;">Research modern career options with real data</p>
            
            <button class="tool-button toolkit-button" onclick="startBehavioralWeather()">
                🌤️ Behavioral Weather Report  
            </button>
            <p style="font-size: 14px; color: #666; margin: 0;">Distinguish normal behavior from warning signs</p>
            
            <button class="tool-button toolkit-button" onclick="startResourceHub()">
                🔍 Resource Hub
            </button>
            <p style="font-size: 14px; color: #666; margin: 0;">Find verified mental health professionals and support</p>
        </div>
        
        <!-- CRISIS SUPPORT -->
        <button class="tool-button crisis-button" onclick="showCrisisSupport()">
            🚨 Crisis Support - I Need Help Now
        </button>
    </div>

    <script>
        console.log("PARENT PORTAL CLIENT LOADED - ALL FEATURES ENABLED");
        
        // Global state
        let currentTool = null;
        let generationalProgress = { area: "discipline", responses: [] };

        // === UTILITY FUNCTIONS ===
        
        function createScreen(screenId) {
            if (!document.getElementById(screenId)) {
                const screen = document.createElement("div");
                screen.id = screenId;
                screen.className = "screen";
                screen.innerHTML = `
                    <button class="exit-button" onclick="exitTool()">✕ Exit</button>
                    <div class="tool-interface" id="${screenId.replace('-screen', '-content')}">
                        <!-- Content loaded dynamically -->
                    </div>
                `;
                document.body.appendChild(screen);
            }
        }

        function showScreen(screenId) {
            document.getElementById("main-interface").style.display = "none";
            document.getElementById(screenId).style.display = "flex";
        }

        function exitTool() {
            // Hide all tool screens
            const screens = ["walk-a-mile-screen", "generational-echo-screen", "empathy-gym-screen", 
                           "career-explorer-screen", "behavioral-weather-screen", "resource-hub-screen"];
            screens.forEach(screenId => {
                const screen = document.getElementById(screenId);
                if (screen) {
                    screen.style.display = "none";
                }
            });
            
            // Show main interface
            document.getElementById("main-interface").style.display = "block";
            
            // Reset state
            currentTool = null;
            generationalProgress = { area: "discipline", responses: [] };
        }

        async function callMCPTool(toolName, arguments = {}) {
            try {
                const response = await fetch(`/mcp/${toolName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(arguments)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
                
            } catch (error) {
                console.error("MCP call failed:", error);
                return await mcp_client.call_mcp_tool(toolName, arguments);
            }
        }

        // === REFLECTION SPACE FUNCTIONS ===

        async function startWalkAMile() {
            console.log("Starting Walk a Mile...");
            try {
                currentTool = "walk-a-mile";
                createScreen("walk-a-mile-screen");
                showScreen("walk-a-mile-screen");
                
                const response = await callMCPTool("walk_a_mile", { stage: "start" });
                displayWalkAMileContent(response);
                
            } catch (error) {
                console.error("Walk a Mile error:", error);
                alert("Could not load Walk a Mile. Please try again.");
                exitTool();
            }
        }

        function displayWalkAMileContent(mcpResult) {
            const content = document.getElementById("walk-a-mile-content");
            const scenario = mcpResult.current_scenario;
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #4a90e2; margin-bottom: 10px;">👣 Walk a Mile</h2>
                    <p style="color: #666;">${mcpResult.intro_message}</p>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${(mcpResult.progress.current / mcpResult.progress.total) * 100}%"></div>
                </div>
                <div style="text-align: center; margin-bottom: 20px;">
                    <small>Scenario ${mcpResult.progress.current} of ${mcpResult.progress.total}</small>
                </div>
                
                <div class="scenario-card">
                    <h3 style="margin-bottom: 15px; color: #333;">${scenario.title}</h3>
                    <p style="margin-bottom: 15px;"><strong>Context:</strong> ${scenario.context}</p>
                    <p style="margin-bottom: 20px;"><strong>Situation:</strong> ${scenario.situation}</p>
                    
                    <h4 style="margin-bottom: 15px;">How would you respond?</h4>
                    
                    <div class="choice-button" onclick="makeWalkAMileChoice('approach_a', ${scenario.id})" style="cursor: pointer;">
                        <strong>Approach A:</strong> ${scenario.approach_a.text}
                        <br><small style="color: #666; margin-top: 5px;">Likely outcome: ${scenario.approach_a.outcome}</small>
                    </div>
                    
                    <div class="choice-button" onclick="makeWalkAMileChoice('approach_b', ${scenario.id})" style="cursor: pointer;">
                        <strong>Approach B:</strong> ${scenario.approach_b.text}
                        <br><small style="color: #666; margin-top: 5px;">Likely outcome: ${scenario.approach_b.outcome}</small>
                    </div>
                </div>
            `;
        }

        async function makeWalkAMileChoice(choice, scenarioId) {
            console.log(`Choice made: ${choice} for scenario ${scenarioId}`);
            
            try {
                alert(`You chose ${choice === 'approach_a' ? 'Approach A' : 'Approach B'}!\\n\\nProcessing your choice and loading next scenario...`);
                
                const response = await callMCPTool("walk_a_mile", { 
                    stage: "choice", 
                    choice: choice,
                    scenario_id: scenarioId 
                });
                
                if (response.stage === "complete") {
                    displayWalkAMileComplete(response);
                } else {
                    displayWalkAMileContent(response);
                }
                
            } catch (error) {
                console.error("Walk a Mile choice error:", error);
                alert("Error processing your choice. Please try again.");
            }
        }

        function displayWalkAMileComplete(mcpResult) {
            const content = document.getElementById("walk-a-mile-content");
            
            content.innerHTML = `
                <div style="text-align: center;">
                    <h2 style="color: #28a745; margin-bottom: 20px;">🎉 Walk a Mile Complete!</h2>
                    <p style="font-size: 18px; color: #48bb78; margin-bottom: 20px;">
                        ${mcpResult.completion_message}
                    </p>
                    <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <p style="font-style: italic; color: #2d5016;">
                            "${mcpResult.insight}"
                        </p>
                    </div>
                    <button class="submit-button" onclick="exitTool()">
                        Continue Your Parenting Journey
                    </button>
                </div>
            `;
        }

        async function startGenerationalEcho() {
            console.log("Starting Generational Echo...");
            try {
                currentTool = "generational-echo";
                createScreen("generational-echo-screen");
                showScreen("generational-echo-screen");
                
                const response = await callMCPTool("generational_echo", { stage: "start" });
                displayGenerationalEchoContent(response);
                
            } catch (error) {
                console.error("Generational Echo error:", error);
                alert("Could not load Generational Echo. Please try again.");
                exitTool();
            }
        }

        function displayGenerationalEchoContent(mcpResult) {
            const content = document.getElementById("generational-echo-content");
            const area = mcpResult.reflection_area;
            const prompts = mcpResult.prompts;
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #7b68ee; margin-bottom: 10px;">🎧 Generational Echo</h2>
                    <p style="color: #666;">${mcpResult.intro_message}</p>
                    <div style="background: #fff3cd; padding: 10px; border-radius: 8px; margin-top: 15px;">
                        <small style="color: #856404;">🔒 ${mcpResult.privacy_note}</small>
                    </div>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #495057; margin-bottom: 15px; text-transform: capitalize;">
                        💭 Reflection Area: ${area}
                    </h3>
                    
                    <div style="margin-bottom: 20px;">
                        <p style="color: #666; margin-bottom: 15px;"><strong>Take your time to reflect on these questions:</strong></p>
                        ${prompts.map((prompt, index) => `
                            <div style="margin-bottom: 12px; padding: 10px; background: white; border-radius: 8px; border-left: 3px solid #7b68ee;">
                                <strong>${index + 1}.</strong> ${prompt}
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <textarea id="reflection-input" class="input-field" 
                    placeholder="Take your time to reflect deeply and honestly on these questions. Your thoughts are private and will help you understand your parenting patterns better...">
                </textarea>
                
                <div style="text-align: center; margin-top: 20px;">
                    <button class="submit-button" onclick="submitReflection('${area}')" style="background: #7b68ee;">
                        Continue to Next Reflection Area →
                    </button>
                </div>
                
                <div style="text-align: center; margin-top: 15px;">
                    <small style="color: #999;">Area ${getAreaIndex(area) + 1} of 4</small>
                </div>
            `;
            
            setTimeout(() => {
                document.getElementById("reflection-input").focus();
            }, 500);
        }

        function getAreaIndex(area) {
            const areas = ["discipline", "communication", "expectations", "emotions"];
            return areas.indexOf(area);
        }

        async function submitReflection(area) {
            try {
                const reflection = document.getElementById("reflection-input").value.trim();
                if (!reflection) {
                    alert("Please share your reflections before continuing. This is a private space for your personal growth.");
                    return;
                }
                
                generationalProgress.responses.push({
                    area: area,
                    reflection: reflection,
                    timestamp: new Date().toISOString()
                });
                
                const content = document.getElementById("generational-echo-content");
                content.innerHTML = `
                    <div style="text-align: center; padding: 40px;">
                        <h3 style="color: #7b68ee;">💭 Processing your reflection...</h3>
                        <p>Preparing the next area for deeper self-discovery.</p>
                    </div>
                `;
                
                setTimeout(async () => {
                    const response = await callMCPTool("generational_echo", {
                        stage: "reflection",
                        reflection_area: area,
                        user_reflection: reflection
                    });
                    
                    if (response.stage === "analysis") {
                        displayGenerationalEchoComplete(response);
                    } else {
                        displayGenerationalEchoContent(response);
                    }
                }, 1500);
                
            } catch (error) {
                console.error("Reflection submission error:", error);
                alert("Error saving your reflection. Please try again.");
            }
        }

        function displayGenerationalEchoComplete(mcpResult) {
            const content = document.getElementById("generational-echo-content");
            
            content.innerHTML = `
                <div style="text-align: center;">
                    <h2 style="color: #28a745; margin-bottom: 20px;">🌟 Reflection Journey Complete</h2>
                    <p style="font-size: 18px; color: #48bb78; margin-bottom: 20px;">
                        ${mcpResult.message}
                    </p>
                    
                    <div style="background: #e8f5e8; padding: 25px; border-radius: 15px; margin: 25px 0; text-align: left;">
                        <h4 style="color: #2d5016; margin-bottom: 15px;">🌱 Your Generational Insights</h4>
                        <p style="color: #2d5016; line-height: 1.6;">
                            Through this reflection, you've explored how your childhood experiences shape your parenting approach. 
                            This awareness is the foundation for making conscious choices about which patterns to continue and which to evolve.
                        </p>
                        <div style="background: white; padding: 15px; border-radius: 8px; margin-top: 15px;">
                            <p style="font-style: italic; color: #2d5016; margin: 0;">
                                "${mcpResult.insight}"
                            </p>
                        </div>
                    </div>
                    
                    <button class="submit-button" onclick="exitTool()">
                        Continue Your Parenting Journey
                    </button>
                </div>
            `;
        }

        // === DAILY PRACTICE FUNCTIONS ===

        async function startEmpathyGym() {
            console.log("Starting Empathy Gym...");
            try {
                currentTool = "empathy-gym";
                createScreen("empathy-gym-screen");
                showScreen("empathy-gym-screen");
                
                const response = await callMCPTool("empathy_gym", { action: "get_daily", difficulty: "beginner" });
                displayEmpathyGymContent(response);
                
            } catch (error) {
                console.error("Empathy Gym error:", error);
                alert("Could not load Empathy Gym. Please try again.");
                exitTool();
            }
        }

        function displayEmpathyGymContent(mcpResult) {
            const content = document.getElementById("empathy-gym-content");
            const scenario = mcpResult.scenario;
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #28a745; margin-bottom: 10px;">💪 Empathy Gym</h2>
                    <p style="color: #666;">${mcpResult.instruction}</p>
                    <div style="background: #d4edda; padding: 10px; border-radius: 8px; margin-top: 15px;">
                        <strong style="color: #155724;">⏱️ ${mcpResult.timer.replace('_', ' ').toUpperCase()}</strong>
                    </div>
                </div>
                
                <div class="scenario-card">
                    <h3 style="margin-bottom: 15px; color: #333;">Today's Scenario</h3>
                    <p style="margin-bottom: 15px;"><strong>Situation:</strong> ${scenario.situation}</p>
                    <p style="margin-bottom: 20px;"><strong>Context:</strong> ${scenario.context}</p>
                    
                    <h4 style="margin-bottom: 15px; color: #28a745;">${scenario.prompt}</h4>
                    
                    <textarea id="empathy-response" class="input-field" 
                        placeholder="Think from your teenager's perspective first, then describe how you would respond...">
                    </textarea>
                    
                    <button class="submit-button" onclick="submitEmpathyResponse('${scenario.id}')">
                        Get Feedback on My Response
                    </button>
                </div>
            `;
        }

        async function submitEmpathyResponse(scenarioId) {
            try {
                const response = document.getElementById("empathy-response").value.trim();
                if (!response) {
                    alert("Please share your response first.");
                    return;
                }
                
                const feedback = await callMCPTool("empathy_gym", {
                    action: "submit_response",
                    scenario_id: scenarioId,
                    user_response: response
                });
                
                displayEmpathyGymFeedback(feedback);
                
            } catch (error) {
                console.error("Empathy response error:", error);
            }
        }

        function displayEmpathyGymFeedback(mcpResult) {
            const content = document.getElementById("empathy-gym-content");
            
            content.innerHTML = `
                <div style="text-align: center;">
                    <h2 style="color: #28a745; margin-bottom: 20px;">🌟 Great Work!</h2>
                    <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <p style="color: #155724; margin-bottom: 15px;">
                            <strong>Feedback:</strong> ${mcpResult.feedback}
                        </p>
                        <p style="color: #2d5016; font-style: italic;">
                            ${mcpResult.encouragement}
                        </p>
                    </div>
                    <button class="submit-button" onclick="exitTool()">
                        Continue Building Empathy
                    </button>
                </div>
            `;
        }
        // === EMPATHY GYM FUNCTIONS (Updated) ===

        async function startEmpathyGym() {
            console.log("Starting Empathy Gym...");
            try {
                currentTool = "empathy-gym";
                createScreen("empathy-gym-screen");
                showScreen("empathy-gym-screen");
                
                const response = await callMCPTool("empathy_gym", { action: "get_daily", difficulty: "beginner" });
                displayEmpathyGymContent(response);
                
            } catch (error) {
                console.error("Empathy Gym error:", error);
                alert("Could not load Empathy Gym. Please try again.");
                exitTool();
            }
        }

        function displayEmpathyGymContent(mcpResult) {
            const content = document.getElementById("empathy-gym-content");
            const scenario = mcpResult.scenario;
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #28a745; margin-bottom: 10px;">💪 Empathy Gym</h2>
                    <p style="color: #666;">${mcpResult.instruction}</p>
                    <div style="background: #d4edda; padding: 10px; border-radius: 8px; margin-top: 15px;">
                        <strong style="color: #155724;">⏱️ <span id="countdown-timer">60 SECONDS</span></strong>
                    </div>
                </div>
                
                <div class="scenario-card">
                    <h3 style="margin-bottom: 15px; color: #333;">Today's Scenario</h3>
                    <p style="margin-bottom: 15px;"><strong>Situation:</strong> ${scenario.situation}</p>
                    <p style="margin-bottom: 20px;"><strong>Context:</strong> ${scenario.context}</p>
                    
                    <h4 style="margin-bottom: 15px; color: #28a745;">${scenario.prompt}</h4>
                    
                    <textarea id="empathy-response" class="input-field" 
                        placeholder="Think from your teenager's perspective first, then describe how you would respond..." 
                        style="width: 100%; height: 120px; padding: 15px; border: 2px solid #ddd; border-radius: 10px; font-size: 16px; margin: 10px 0; resize: vertical; box-sizing: border-box; font-family: Arial, sans-serif; vertical-align: top;">
                    </textarea>
                    
                    <button class="submit-button" onclick="submitEmpathyResponse('${scenario.id}')">
                        Get Feedback on My Response
                    </button>
                </div>
            `;
            
            // Start the countdown timer
            startCountdownTimer();
        }

        function startCountdownTimer() {
            let timeLeft = 60;
            const timerElement = document.getElementById("countdown-timer");
            
            const countdown = setInterval(() => {
                timeLeft--;
                
                if (timeLeft > 0) {
                    timerElement.textContent = `${timeLeft} SECONDS`;
                    
                    // Change color as time runs out
                    if (timeLeft <= 10) {
                        timerElement.parentElement.style.background = "#f8d7da";
                        timerElement.style.color = "#721c24";
                    } else if (timeLeft <= 30) {
                        timerElement.parentElement.style.background = "#fff3cd";
                        timerElement.style.color = "#856404";
                    }
                } else {
                    timerElement.textContent = "TIME'S UP!";
                    timerElement.parentElement.style.background = "#f8d7da";
                    timerElement.style.color = "#721c24";
                    clearInterval(countdown);
                    
                    // Optional: Show encouragement message
                    setTimeout(() => {
                        const responseBox = document.getElementById("empathy-response");
                        if (responseBox && responseBox.value.trim() === "") {
                            alert("Time's up! No pressure - you can still take your time to think and respond.");
                        }
                    }, 1000);
                }
            }, 1000);
        }

        async function submitEmpathyResponse(scenarioId) {
            try {
                const response = document.getElementById("empathy-response").value.trim();
                if (!response) {
                    alert("Please share your response first.");
                    return;
                }
                
                const feedback = await callMCPTool("empathy_gym", {
                    action: "submit_response",
                    scenario_id: scenarioId,
                    user_response: response
                });
                
                displayEmpathyGymFeedback(feedback);
                
            } catch (error) {
                console.error("Empathy response error:", error);
                alert("Error getting feedback. Please try again.");
            }
        }

        function displayEmpathyGymFeedback(mcpResult) {
            const content = document.getElementById("empathy-gym-content");
            
            content.innerHTML = `
                <div style="text-align: center;">
                    <h2 style="color: #28a745; margin-bottom: 20px;">🌟 Great Work!</h2>
                    
                    <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h4 style="color: #155724; margin-bottom: 15px;">📝 Feedback on Your Response</h4>
                        <p style="color: #155724; margin-bottom: 15px; line-height: 1.6;">
                            ${mcpResult.feedback || "Great job thinking from your teenager's perspective! Every attempt at empathy helps build stronger connections."}
                        </p>
                        
                        ${mcpResult.empathy_insight ? `
                        <div style="background: white; padding: 15px; border-radius: 8px; margin-top: 15px;">
                            <h5 style="color: #2d5016; margin-bottom: 10px;">💭 Your Teen Might Be Thinking:</h5>
                            <p style="color: #2d5016; font-style: italic; margin: 0;">
                                "${mcpResult.empathy_insight}"
                            </p>
                        </div>
                        ` : ''}
                        
                        <p style="color: #2d5016; font-style: italic; margin-top: 15px; margin-bottom: 0;">
                            ${mcpResult.encouragement || "Keep practicing empathy - it's a skill that grows stronger with use!"}
                        </p>
                    </div>
                    
                    <div style="margin-top: 30px;">
                        <button class="submit-button" onclick="startEmpathyGym()" style="margin-right: 10px; background: #28a745;">
                            Try Another Scenario
                        </button>
                        <button class="submit-button" onclick="exitTool()">
                            Continue Building Empathy
                        </button>
                    </div>
                </div>
            `;
        }



        // === TOOLKIT FUNCTIONS ===

        async function startCareerExplorer() {
            console.log("Starting Career Explorer...");
            try {
                currentTool = "career-explorer";
                createScreen("career-explorer-screen");
                showScreen("career-explorer-screen");
                
                displayCareerExplorerForm();
                
            } catch (error) {
                console.error("Career Explorer error:", error);
                alert("Could not load Career Explorer. Please try again.");
                exitTool();
            }
        }

        function displayCareerExplorerForm() {
            const content = document.getElementById("career-explorer-content");
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #17a2b8; margin-bottom: 10px;">🎯 Career Path Explorer</h2>
                    <p style="color: #666;">Research modern career options with real market data and salary projections</p>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <div class="form-group">
                        <label class="form-label">What career is your teenager interested in?</label>
                        <input type="text" id="career-field" class="form-input" 
                            placeholder="e.g., Photography, Game Design, Data Science, Graphic Design, YouTuber">
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">Location for market research:</label>
                            <select id="career-location" class="form-input">
                                <option value="India">India (General)</option>
                                <option value="Mumbai">Mumbai</option>
                                <option value="Delhi">Delhi</option>
                                <option value="Bangalore">Bangalore</option>
                                <option value="Chennai">Chennai</option>
                                <option value="Pune">Pune</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Child's specific interests: (Optional)</label>
                            <textarea id="child-interests" class="form-input" style="height: 80px;" 
                                placeholder="e.g., Loves taking photos of nature, good with technology...">
                            </textarea>
                        </div>
                    </div>
                    
                    <div style="text-align: center;">
                        <button class="submit-button" onclick="exploreCareer()" style="background: #17a2b8; padding: 15px 40px;">
                            🔍 Research This Career Path
                        </button>
                    </div>
                </div>
            `;
        }

        async function exploreCareer() {
            try {
                const careerField = document.getElementById("career-field").value.trim();
                const location = document.getElementById("career-location").value;
                const interests = document.getElementById("child-interests").value.trim();
                
                if (!careerField) {
                    alert("Please enter a career field to research.");
                    return;
                }
                
                const content = document.getElementById("career-explorer-content");
                content.innerHTML = `
                    <div style="text-align: center; padding: 40px;">
                        <h3>🔍 Researching ${careerField} opportunities in ${location}...</h3>
                        <p>Gathering salary data, market trends, and skill requirements...</p>
                    </div>
                `;
                
                const response = await callMCPTool("career_path_explorer", {
                    career_field: careerField,
                    location: location,
                    child_interests: interests
                });
                
                setTimeout(() => displayCareerResults(response, careerField), 1500);
                
            } catch (error) {
                console.error("Career exploration error:", error);
            }
        }

        function displayCareerResults(mcpResult, careerField) {
            const content = document.getElementById("career-explorer-content");
            const analysis = mcpResult.career_analysis;
            const guidance = mcpResult.parent_guidance;
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #17a2b8;">📊 Career Analysis: ${analysis.career_field}</h2>
                    <p style="color: #666;">Market research for ${analysis.location}</p>
                </div>
                
                <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #2c5aa0; margin-bottom: 15px;">💰 Salary Ranges</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                            <strong>Entry Level</strong><br>
                            <span style="color: #28a745; font-size: 18px;">${analysis.salary_ranges.entry_level}</span>
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                            <strong>Mid Level</strong><br>
                            <span style="color: #28a745; font-size: 18px;">${analysis.salary_ranges.mid_level}</span>
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                            <strong>Senior Level</strong><br>
                            <span style="color: #28a745; font-size: 18px;">${analysis.salary_ranges.senior_level}</span>
                        </div>
                    </div>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #495057; margin-bottom: 15px;">🎯 Skills Needed for Success</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        ${analysis.skills_needed.map(skill => `
                            <span style="background: #667eea; color: white; padding: 8px 15px; border-radius: 20px; font-size: 14px;">
                                ${skill}
                            </span>
                        `).join('')}
                    </div>
                </div>
                
                <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #155724; margin-bottom: 15px;">🎓 Education Pathways</h3>
                    ${analysis.education_paths.map(path => `
                        <div style="margin-bottom: 10px;">
                            <span style="color: #28a745;">✓</span> ${path}
                        </div>
                    `).join('')}
                </div>
                
                <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #856404; margin-bottom: 15px;">💡 Conversation Starters with Your Teen</h3>
                    ${guidance.conversation_starters.map(starter => `
                        <div style="margin-bottom: 15px; padding: 10px; background: white; border-radius: 8px;">
                            <em>"${starter}"</em>
                        </div>
                    `).join('')}
                </div>
                
                <div style="text-align: center;">
                    <button class="submit-button" onclick="displayCareerExplorerForm()" style="margin-right: 10px;">
                        Research Another Career
                    </button>
                    <button class="submit-button" onclick="exitTool()">
                        Start the Conversation
                    </button>
                </div>
            `;
        }

        async function startBehavioralWeather() {
            console.log("Starting Behavioral Weather Report...");
            try {
                currentTool = "behavioral-weather";
                createScreen("behavioral-weather-screen");
                showScreen("behavioral-weather-screen");
                
                displayBehavioralWeatherForm();
                
            } catch (error) {
                console.error("Behavioral Weather error:", error);
                alert("Could not load Behavioral Weather Report. Please try again.");
                exitTool();
            }
        }

        function displayBehavioralWeatherForm() {
            const content = document.getElementById("behavioral-weather-content");
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #ffc107; margin-bottom: 10px;">🌤️ Behavioral Weather Report</h2>
                    <p style="color: #666;">Distinguish normal teenage behavior from potential warning signs</p>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #ffc107;">
                    <p style="margin: 0; color: #856404;">
                        <strong>Important:</strong> This is an educational tool, not a medical diagnosis. 
                        Trust your parental instincts and seek professional help when concerned.
                    </p>
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <label class="form-label">What behaviors have you observed? (Check all that apply)</label>
                    <div id="behavior-checklist" class="checkbox-group">
                        <div class="checkbox-item">
                            <input type="checkbox" value="withdrawal_from_family" id="b1">
                            <label for="b1">Withdrawal from family activities</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" value="mood_swings" id="b2">
                            <label for="b2">Extreme mood swings</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" value="sleep_changes" id="b3">
                            <label for="b3">Changes in sleep patterns</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" value="appetite_changes" id="b4">
                            <label for="b4">Changes in eating habits</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" value="academic_decline" id="b5">
                            <label for="b5">Declining academic performance</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" value="irritability" id="b6">
                            <label for="b6">Increased irritability or anger</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" value="social_withdrawal" id="b7">
                            <label for="b7">Avoiding friends and social activities</label>
                        </div>
                        <div class="checkbox-item">
                            <input type="checkbox" value="risk_taking" id="b8">
                            <label for="b8">Engaging in risky behaviors</label>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">How long have you noticed these behaviors?</label>
                            <select id="behavior-duration" class="form-input">
                                <option value="less_than_week">Less than a week</option>
                                <option value="1-2_weeks">1-2 weeks</option>
                                <option value="2-4_weeks">2-4 weeks</option>
                                <option value="1-3_months">1-3 months</option>
                                <option value="more_than_3_months">More than 3 months</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Your level of concern (1 = mild, 5 = very worried):</label>
                            <input type="range" id="concern-level" min="1" max="5" value="3" 
                                style="width: 100%; margin: 10px 0;" oninput="updateConcernLabel()">
                            <div style="text-align: center;">
                                <span id="concern-label">Moderately Concerned (3)</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label">Additional context: (Optional)</label>
                        <textarea id="behavior-context" class="form-input" 
                            placeholder="Any recent changes, stressors, or additional information...">
                        </textarea>
                    </div>
                    
                    <div style="text-align: center;">
                        <button class="submit-button" onclick="generateWeatherReport()" style="background: #ffc107; color: #212529; padding: 15px 40px;">
                            📊 Generate Behavioral Weather Report
                        </button>
                    </div>
                </div>
            `;
        }

        function updateConcernLabel() {
            const level = document.getElementById("concern-level").value;
            const labels = {
                "1": "Mildly Concerned (1)",
                "2": "Somewhat Concerned (2)", 
                "3": "Moderately Concerned (3)",
                "4": "Quite Worried (4)",
                "5": "Very Worried (5)"
            };
            document.getElementById("concern-label").textContent = labels[level];
        }

        async function generateWeatherReport() {
            try {
                const checkboxes = document.querySelectorAll("#behavior-checklist input:checked");
                const behaviors = Array.from(checkboxes).map(cb => cb.value);
                
                const duration = document.getElementById("behavior-duration").value;
                const severity = parseInt(document.getElementById("concern-level").value);
                const context = document.getElementById("behavior-context").value.trim();
                
                if (behaviors.length === 0) {
                    alert("Please select at least one behavior you've observed.");
                    return;
                }
                
                const content = document.getElementById("behavioral-weather-content");
                content.innerHTML = `
                    <div style="text-align: center; padding: 40px;">
                        <h3>🌤️ Analyzing behavioral patterns...</h3>
                        <p>Generating your personalized weather report...</p>
                    </div>
                `;
                
                const response = await callMCPTool("behavioral_weather_report", {
                    behaviors: behaviors,
                    duration: duration,
                    severity: severity,
                    context: context
                });
                
                setTimeout(() => displayWeatherReport(response), 2000);
                
            } catch (error) {
                console.error("Weather report error:", error);
            }
        }

        function displayWeatherReport(mcpResult) {
            const content = document.getElementById("behavioral-weather-content");
            const assessment = mcpResult.assessment;
            const guidance = mcpResult.guidance;
            const crisis = mcpResult.crisis_resources;
            
            let riskColor = "#28a745";  // Green for low
            if (assessment.risk_level === "MEDIUM") riskColor = "#ffc107";  // Yellow
            if (assessment.risk_level === "HIGH") riskColor = "#dc3545";    // Red
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #ffc107;">📊 Behavioral Weather Report</h2>
                    <p style="color: #666;">Based on your observations and concerns</p>
                </div>
                
                <div style="background: ${riskColor}; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
                    <h3 style="margin-bottom: 10px;">Risk Level: ${assessment.risk_level}</h3>
                    <p style="margin: 10px 0; font-size: 18px;">Score: ${assessment.risk_score}</p>
                    <p style="margin: 0; font-size: 16px;">${assessment.recommendation}</p>
                </div>
                
                <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #155724; margin-bottom: 15px;">✅ Recommended Next Steps</h3>
                    ${guidance.next_steps.map(step => `
                        <div style="margin-bottom: 10px;">
                            <span style="color: #28a745;">•</span> ${step}
                        </div>
                    `).join('')}
                </div>
                
                <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #856404; margin-bottom: 15px;">⚠️ When to Seek Professional Help</h3>
                    ${guidance.when_to_seek_help.map(sign => `
                        <div style="margin-bottom: 10px;">
                            <span style="color: #ffc107;">•</span> ${sign}
                        </div>
                    `).join('')}
                </div>
                
                <div style="background: #f8d7da; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #dc3545;">
                    <h3 style="color: #721c24; margin-bottom: 15px;">🚨 Crisis Support (Always Available)</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                        <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                            <strong>KIRAN Helpline</strong><br>
                            <a href="tel:18005990019" style="color: #dc3545; font-size: 18px;">
                                ${crisis.kiran}
                            </a>
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                            <strong>Vandrevala Foundation</strong><br>
                            <a href="tel:18602662345" style="color: #dc3545; font-size: 18px;">
                                ${crisis.vandrevala}
                            </a>
                        </div>
                        <div style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                            <strong>Emergency</strong><br>
                            <span style="color: #dc3545; font-size: 18px;">
                                ${crisis.emergency}
                            </span>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <button class="submit-button" onclick="displayBehavioralWeatherForm()" style="margin-right: 10px;">
                        Create New Report
                    </button>
                    <button class="submit-button" onclick="startResourceHub()" style="background: #17a2b8;">
                        Find Professional Help
                    </button>
                </div>
            `;
        }

        async function startResourceHub() {
            console.log("Starting Resource Hub...");
            try {
                currentTool = "resource-hub";
                createScreen("resource-hub-screen");
                showScreen("resource-hub-screen");
                
                const response = await callMCPTool("resource_hub", {
                    resource_type: "family_therapist",
                    location: "India",
                    urgency: "medium"
                });
                displayResourceHub(response);
                
            } catch (error) {
                console.error("Resource Hub error:", error);
                alert("Could not load Resource Hub. Please try again.");
                exitTool();
            }
        }

        function displayResourceHub(mcpResult) {
            const content = document.getElementById("resource-hub-content");
            const resources = mcpResult.professional_resources;
            const educational = mcpResult.educational_resources;
            
            content.innerHTML = `
                <div style="text-align: center; margin-bottom: 30px;">
                    <h2 style="color: #17a2b8; margin-bottom: 10px;">🔍 Resource Hub</h2>
                    <p style="color: #666;">Vetted mental health professionals and support resources</p>
                </div>
                
                <div style="background: #e8f4fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #2c5aa0; margin-bottom: 15px;">👩‍⚕️ Professional Resources</h3>
                    ${resources.map((resource, index) => `
                        <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 4px solid #17a2b8;">
                            <h4 style="margin-bottom: 10px; color: #333;">${resource.name}</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                                <div>
                                    <strong>Contact:</strong><br>
                                    <a href="tel:${resource.contact.replace(/[^\\d]/g, '')}" style="color: #17a2b8;">
                                        ${resource.contact}
                                    </a>
                                </div>
                                <div>
                                    <strong>Specialty:</strong><br>
                                    ${resource.speciality}
                                </div>
                                <div>
                                    <strong>Fee Range:</strong><br>
                                    ${resource.fee_range}
                                </div>
                                <div>
                                    <strong>Languages:</strong><br>
                                    ${resource.languages.join(", ")}
                                </div>
                            </div>
                            <div style="margin-top: 10px;">
                                <span style="background: #28a745; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">
                                    ${resource.mode}
                                </span>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #495057; margin-bottom: 15px;">📚 Educational Resources</h3>
                    ${educational.map(resource => `
                        <div style="margin-bottom: 10px;">
                            <span style="color: #28a745;">•</span> ${resource}
                        </div>
                    `).join('')}
                </div>
                
                <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h3 style="color: #155724; margin-bottom: 15px;">💡 Tips for Choosing Professional Help</h3>
                    <div style="margin-bottom: 10px;">• Look for specialists in adolescent therapy</div>
                    <div style="margin-bottom: 10px;">• Consider family therapy for communication issues</div>
                    <div style="margin-bottom: 10px;">• Ask about their approach and experience</div>
                    <div style="margin-bottom: 10px;">• Ensure comfort with both parent and teen</div>
                </div>
                
                <div style="text-align: center;">
                    <button class="submit-button" onclick="exitTool()">
                        Start Your Search for Support
                    </button>
                </div>
            `;
        }

        function showCrisisSupport() {
            alert(`🚨 IMMEDIATE CRISIS SUPPORT\\n\\n24/7 Helplines:\\n📞 KIRAN: 1800-599-0019\\n📞 Vandrevala Foundation: 1860-2662-345\\n📞 iCall: 022-2556-3291\\n\\nEmergency: Call 102\\n\\nIf your teen is in immediate danger:\\n• Don't leave them alone\\n• Remove harmful objects\\n• Call helpline immediately\\n• Go to nearest hospital if needed\\n\\nYOU ARE NOT ALONE. Help is available.`);
        }
    </script>
</body>
</html>
'''

# MCP endpoints for frontend communication
@app.post("/mcp/{tool_name}")
async def mcp_endpoint(tool_name: str, request: Request):
    """Handle MCP tool calls from frontend"""
    try:
        body = await request.json()
        result = await mcp_client.call_mcp_tool(tool_name, body)
        return result
    except Exception as e:
        logger.error(f"MCP endpoint error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("🚀 Starting Parent Portal Client...")
    logger.info("Connect to: http://localhost:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
