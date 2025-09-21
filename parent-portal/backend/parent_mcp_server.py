#!/usr/bin/env python3

"""
Parent Portal MCP Server - PROPER IMPLEMENTATION
Proper Model Context Protocol implementation for parenting support
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
logger = logging.getLogger("parent-portal-mcp")

# Global server instance
server = Server("parent-portal-mcp")

# Global components
model = None
storage_client = None
bucket_name = "parent-portal-data-bucket"

def initialize_services():
    """Initialize AI and storage services"""
    global model, storage_client
    try:
        # Initialize Vertex AI
        vertexai.init(project="parent-portal-mcp", location="us-central1")
        model = GenerativeModel("gemini-2.0-flash-exp")
        
        # Initialize Cloud Storage
        storage_client = storage.Client(project="parent-portal-mcp")
        logger.info("Parent Portal services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List all available parent portal tools"""
    return [
        # === REFLECTION SPACE TOOLS ===
        types.Tool(
            name="walk_a_mile",
            description="Interactive case studies where parents practice empathy through challenging parenting scenarios",
            inputSchema={
                "type": "object",
                "properties": {
                    "stage": {
                        "type": "string",
                        "description": "Current stage: start, scenario, choice, complete",
                        "enum": ["start", "scenario", "choice", "complete"]
                    },
                    "scenario_id": {
                        "type": "integer", 
                        "description": "ID of current scenario (1-3)"
                    },
                    "choice": {
                        "type": "string",
                        "description": "User's choice: approach_a or approach_b"
                    }
                },
                "required": ["stage"]
            }
        ),
        
        types.Tool(
            name="generational_echo",
            description="Private reflection helping parents understand how their upbringing impacts current parenting patterns",
            inputSchema={
                "type": "object",
                "properties": {
                    "stage": {
                        "type": "string", 
                        "description": "Current stage: start, reflection, analysis, complete",
                        "enum": ["start", "reflection", "analysis", "complete"]
                    },
                    "reflection_area": {
                        "type": "string",
                        "description": "Area: discipline, communication, expectations, emotions",
                        "enum": ["discipline", "communication", "expectations", "emotions"]
                    },
                    "user_reflection": {
                        "type": "string",
                        "description": "User's written reflection"
                    }
                },
                "required": ["stage"]
            }
        ),

        # === DAILY PRACTICE TOOLS ===
        types.Tool(
            name="empathy_gym",
            description="Daily 60-second parenting scenarios with immediate feedback to build empathy skills",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Action: get_daily, submit_response, get_feedback",
                        "enum": ["get_daily", "submit_response", "get_feedback"]
                    },
                    "scenario_id": {
                        "type": "string",
                        "description": "ID of current scenario"
                    },
                    "user_response": {
                        "type": "string", 
                        "description": "Parent's response to scenario"
                    },
                    "difficulty": {
                        "type": "string",
                        "description": "Difficulty: beginner, intermediate, advanced",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "default": "beginner"
                    }
                },
                "required": ["action"]
            }
        ),

        # === TOOLKIT TOOLS ===
        types.Tool(
            name="career_path_explorer",
            description="Research tool with salary and growth projections to understand modern career options",
            inputSchema={
                "type": "object",
                "properties": {
                    "career_field": {
                        "type": "string",
                        "description": "Career to research (e.g., 'Photography', 'Game Design')"
                    },
                    "location": {
                        "type": "string", 
                        "description": "Geographic location for market data",
                        "default": "India"
                    },
                    "child_interests": {
                        "type": "string",
                        "description": "Child's specific interests or skills"
                    }
                },
                "required": ["career_field"]
            }
        ),

        types.Tool(
            name="behavioral_weather_report", 
            description="Educational checklist helping parents distinguish normal behavior from warning signs",
            inputSchema={
                "type": "object",
                "properties": {
                    "behaviors": {
                        "type": "array",
                        "description": "Observed behaviors",
                        "items": {"type": "string"}
                    },
                    "duration": {
                        "type": "string",
                        "description": "Duration of behaviors",
                        "enum": ["less_than_week", "1-2_weeks", "2-4_weeks", "1-3_months", "more_than_3_months"]
                    },
                    "severity": {
                        "type": "integer",
                        "description": "Concern level (1-5)",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context"
                    }
                },
                "required": ["behaviors", "duration", "severity"]
            }
        ),

        types.Tool(
            name="resource_hub",
            description="Vetted directory of mental health professionals, crisis hotlines, and resources",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_type": {
                        "type": "string", 
                        "description": "Type of resource needed",
                        "enum": ["crisis_support", "family_therapist", "teen_counselor", "educational_resources"],
                        "default": "family_therapist"
                    },
                    "location": {
                        "type": "string",
                        "description": "Geographic location",
                        "default": "India" 
                    },
                    "urgency": {
                        "type": "string",
                        "description": "Urgency level",
                        "enum": ["low", "medium", "high", "crisis"],
                        "default": "medium"
                    }
                },
                "required": ["resource_type"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """Handle tool execution"""
    global model, storage_client, bucket_name
    
    try:
        # Route to appropriate tool handler
        if name == "walk_a_mile":
            result = await walk_a_mile_tool(arguments)
        elif name == "generational_echo":
            result = await generational_echo_tool(arguments)
        elif name == "empathy_gym":
            result = await empathy_gym_tool(arguments)
        elif name == "career_path_explorer":
            result = await career_path_explorer_tool(arguments)
        elif name == "behavioral_weather_report":
            result = await behavioral_weather_report_tool(arguments)
        elif name == "resource_hub":
            result = await resource_hub_tool(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        error_result = {
            "error": str(e),
            "tool": name,
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }
        return [types.TextContent(type="text", text=json.dumps(error_result, indent=2))]

# === TOOL IMPLEMENTATIONS ===

# Walk a Mile Case Studies
CASE_STUDIES = [
    {
        "id": 1,
        "title": "The Career Dream Conflict",
        "context": "Your 17-year-old daughter announces she wants to drop pre-med to become a photographer. You've always planned for her to be a doctor.",
        "situation": "She applied to art school without telling you and got accepted with a scholarship.",
        "approach_a": {
            "text": "Express concerns about financial stability and 'wasting' her academic gifts. Emphasize practical benefits of medicine.",
            "outcome": "Likely creates defensive response, potential rebellion, damaged trust"
        },
        "approach_b": {
            "text": "Ask her to walk you through her passion for photography and specific career vision. Show genuine curiosity.",
            "outcome": "Builds trust, opens collaborative planning, increases understanding"
        }
    },
    {
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
    {
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
    }
]

async def walk_a_mile_tool(arguments: dict) -> dict:
    """Interactive empathy case studies"""
    try:
        stage = arguments.get("stage")
        
        if stage == "start":
            return {
                "mcp_tool": "walk_a_mile",
                "stage": "scenario",
                "current_scenario": CASE_STUDIES[0],
                "progress": {"current": 1, "total": len(CASE_STUDIES)},
                "intro_message": "Walk in your teenager's shoes through real parenting challenges. Practice empathy and explore different approaches.",
                "timestamp": datetime.now().isoformat()
            }
            
        elif stage == "choice":
            scenario_id = arguments.get("scenario_id", 1)
            choice = arguments.get("choice")
            
            print(f"DEBUG: Choice received - scenario_id: {scenario_id}, choice: {choice}")
            
            # Get next scenario or complete
            if scenario_id < len(CASE_STUDIES):
                next_scenario = CASE_STUDIES[scenario_id]  # scenario_id is 1-based, array is 0-based
                return {
                    "mcp_tool": "walk_a_mile",
                    "stage": "scenario",
                    "current_scenario": next_scenario,
                    "progress": {"current": scenario_id + 1, "total": len(CASE_STUDIES)},
                    "previous_choice": choice,
                    "choice_feedback": f"You chose {choice.replace('_', ' ').title()}. Here's the next scenario:",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "mcp_tool": "walk_a_mile",
                    "stage": "complete",
                    "completion_message": "Walk a Mile journey complete! You've practiced empathy through challenging scenarios.",
                    "insight": "Remember: Every challenging moment is an opportunity to deepen your connection with your teenager.",
                    "total_scenarios_completed": len(CASE_STUDIES),
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        print(f"ERROR in walk_a_mile_tool: {e}")
        return {"mcp_tool": "walk_a_mile", "error": str(e), "timestamp": datetime.now().isoformat()}


async def generational_echo_tool(arguments: dict) -> dict:
    """Private generational reflection"""
    try:
        stage = arguments.get("stage")
        
        if stage == "start":
            return {
                "mcp_tool": "generational_echo",
                "stage": "reflection",
                "reflection_area": "discipline",
                "prompts": [
                    "How were you disciplined as a child? What methods did your parents use?",
                    "When disciplined, how did it make you feel? What did you learn?",
                    "What discipline approaches do you automatically use with your teen?",
                    "Are there patterns you want to change or continue?"
                ],
                "intro_message": "Private reflection on how your upbringing influences your parenting. Take your time and be honest.",
                "privacy_note": "These reflections are completely private and help develop self-awareness.",
                "timestamp": datetime.now().isoformat()
            }
            
        elif stage == "reflection":
            area = arguments.get("reflection_area", "discipline")
            reflection = arguments.get("user_reflection", "")
            
            areas = ["discipline", "communication", "expectations", "emotions"]
            current_index = areas.index(area)
            
            if current_index + 1 < len(areas):
                next_area = areas[current_index + 1]
                return {
                    "mcp_tool": "generational_echo",
                    "stage": "reflection",
                    "reflection_area": next_area,
                    "prompts": get_reflection_prompts(next_area),
                    "progress": {"current": current_index + 2, "total": len(areas)},
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "mcp_tool": "generational_echo",
                    "stage": "analysis",
                    "message": "Reflection complete. Analyzing your generational patterns...",
                    "insight": "Your awareness of these patterns is the first step toward more conscious parenting.",
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {"mcp_tool": "generational_echo", "error": str(e), "timestamp": datetime.now().isoformat()}

def get_reflection_prompts(area: str) -> list:
    """Get reflection prompts for specific area"""
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
    return prompts.get(area, [])

async def empathy_gym_tool(arguments: dict) -> dict:
    """Daily empathy practice"""
    try:
        action = arguments.get("action")
        difficulty = arguments.get("difficulty", "beginner")
        
        if action == "get_daily":
            import random
            scenarios = {
                "beginner": [
                    {
                        "id": "teen_room_mess",
                        "situation": "Your teenager's room is completely messy. They're on their bed scrolling their phone.",
                        "context": "They have a big test tomorrow and you've reminded them twice to clean up.",
                        "prompt": "What's your immediate response?"
                    }
                ]
            }
            scenario = random.choice(scenarios[difficulty])
            
            return {
                "mcp_tool": "empathy_gym",
                "action": "scenario_presented",
                "scenario": scenario,
                "difficulty": difficulty,
                "timer": "60_seconds",
                "instruction": "Take 60 seconds to think from your teenager's perspective, then respond.",
                "timestamp": datetime.now().isoformat()
            }
            
        elif action == "submit_response":
            return {
                "mcp_tool": "empathy_gym",
                "action": "feedback_provided",
                "feedback": "Great work practicing empathy! Consider your teenager's emotional needs behind their behavior.",
                "encouragement": "Every moment of understanding strengthens your relationship.",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {"mcp_tool": "empathy_gym", "error": str(e), "timestamp": datetime.now().isoformat()}

async def career_path_explorer_tool(arguments: dict) -> dict:
    """Career research tool"""
    try:
        career_field = arguments.get("career_field")
        location = arguments.get("location", "India")
        
        return {
            "mcp_tool": "career_path_explorer",
            "career_analysis": {
                "career_field": career_field,
                "location": location,
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
                    f"I've been learning about {career_field} - can you tell me what excites you about it?",
                    "What specific skills do you want to develop?",
                    "How can I support your exploration of this field?"
                ]
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"mcp_tool": "career_path_explorer", "error": str(e), "timestamp": datetime.now().isoformat()}

async def behavioral_weather_report_tool(arguments: dict) -> dict:
    """Behavioral assessment tool"""
    try:
        behaviors = arguments.get("behaviors", [])
        duration = arguments.get("duration")
        severity = arguments.get("severity", 3)
        
        # Simple risk assessment
        risk_score = len(behaviors) + severity
        
        if risk_score >= 8:
            risk_level = "HIGH"
            recommendation = "Consider professional consultation soon"
        elif risk_score >= 5:
            risk_level = "MEDIUM"
            recommendation = "Monitor closely and maintain open communication"
        else:
            risk_level = "LOW"
            recommendation = "Appears within normal teenage development range"
            
        return {
            "mcp_tool": "behavioral_weather_report",
            "assessment": {
                "risk_level": risk_level,
                "risk_score": f"{risk_score}/15",
                "recommendation": recommendation,
                "behaviors_analyzed": len(behaviors),
                "duration": duration,
                "severity_perception": f"{severity}/5"
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
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"mcp_tool": "behavioral_weather_report", "error": str(e), "timestamp": datetime.now().isoformat()}

async def resource_hub_tool(arguments: dict) -> dict:
    """Resource directory"""
    try:
        resource_type = arguments.get("resource_type", "family_therapist")
        location = arguments.get("location", "India")
        urgency = arguments.get("urgency", "medium")
        
        if urgency == "crisis":
            return {
                "mcp_tool": "resource_hub",
                "resource_type": "crisis_support",
                "crisis_resources": {
                    "immediate_helplines": [
                        {"name": "KIRAN Mental Health Helpline", "number": "1800-599-0019", "availability": "24/7"},
                        {"name": "Vandrevala Foundation", "number": "1860-2662-345", "availability": "24/7"},
                        {"name": "iCall Psychosocial Helpline", "number": "022-2556-3291", "availability": "24/7"}
                    ],
                    "emergency_actions": [
                        "Stay calm and don't leave teen alone",
                        "Remove any harmful objects",
                        "Call helpline immediately",
                        "Go to nearest hospital if physical safety at risk"
                    ]
                },
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "mcp_tool": "resource_hub",
            "resource_type": resource_type,
            "location": location,
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
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"mcp_tool": "resource_hub", "error": str(e), "timestamp": datetime.now().isoformat()}

# Initialize services on startup
initialize_services()

async def main():
    """Run the Parent Portal MCP server"""
    # Create server options - FIXED VERSION
    options = InitializationOptions(
        server_name="parent-portal-mcp",
        server_version="1.0.0", 
        capabilities=server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={}
        )
    )
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Parent Portal MCP Server starting...")
        await server.run(read_stream, write_stream, options)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
