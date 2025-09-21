# main.py - Main Landing Page for Wellness Hub
import os
import sys
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mental Wellness Hub")

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mental Wellness Hub | AI-Powered Mental Health Support</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            width: 90%;
            text-align: center;
            padding: 40px 20px;
        }
        
        .hero-section {
            margin-bottom: 60px;
        }
        
        .logo {
            font-size: 3.5em;
            font-weight: 300;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tagline {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 15px;
            font-weight: 300;
        }
        
        .description {
            font-size: 1.1em;
            opacity: 0.8;
            max-width: 600px;
            margin: 0 auto 50px;
            line-height: 1.6;
        }
        
        .portals-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 40px;
            margin-bottom: 50px;
        }
        
        .portal-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px 30px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .portal-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .portal-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
        }
        
        .youth-card::before {
            background: linear-gradient(90deg, #4facfe, #00f2fe);
        }
        
        .parent-card::before {
            background: linear-gradient(90deg, #fa709a, #fee140);
        }
        
        .portal-icon {
            font-size: 4em;
            margin-bottom: 20px;
            display: block;
        }
        
        .portal-title {
            font-size: 2em;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .portal-subtitle {
            font-size: 1.1em;
            opacity: 0.8;
            margin-bottom: 25px;
        }
        
        .features-list {
            list-style: none;
            margin-bottom: 30px;
            text-align: left;
        }
        
        .features-list li {
            padding: 8px 0;
            opacity: 0.9;
            font-size: 0.95em;
        }
        
        .features-list li::before {
            content: '✨ ';
            margin-right: 8px;
        }
        
        .portal-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
        }
        
        .portal-button:hover {
            background: linear-gradient(45deg, #764ba2, #667eea);
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .youth-button {
            background: linear-gradient(45deg, #4facfe, #00f2fe);
        }
        
        .youth-button:hover {
            background: linear-gradient(45deg, #00f2fe, #4facfe);
        }
        
        .parent-button {
            background: linear-gradient(45deg, #fa709a, #fee140);
        }
        
        .parent-button:hover {
            background: linear-gradient(45deg, #fee140, #fa709a);
        }
        
        .powered-by {
            margin-top: 50px;
            opacity: 0.7;
            font-size: 0.9em;
        }
        
        .tech-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.1);
            padding: 5px 15px;
            border-radius: 15px;
            margin: 5px;
            font-size: 0.8em;
        }
        
        @media (max-width: 768px) {
            .logo {
                font-size: 2.5em;
            }
            
            .portals-section {
                grid-template-columns: 1fr;
                gap: 30px;
            }
            
            .portal-card {
                padding: 30px 20px;
            }
            
            .container {
                width: 95%;
                padding: 20px 10px;
            }
        }
        
        .floating-particles {
            position: absolute;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            animation: float 15s infinite linear;
        }
        
        @keyframes float {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(720deg);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="floating-particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
    </div>
    
    <div class="container">
        <div class="hero-section">
            <h1 class="logo">🧠 Mental Wellness Hub</h1>
            <p class="tagline">AI-Powered Mental Health Support Platform</p>
            <p class="description">
                Comprehensive mental wellness tools powered by advanced AI and designed for both youth and parents. 
                Get personalized support, crisis intervention, and evidence-based therapeutic interventions.
            </p>
        </div>
        
        <div class="portals-section">
            <div class="portal-card youth-card">
                <div class="portal-icon">🌟</div>
                <h2 class="portal-title">Youth Portal</h2>
                <p class="portal-subtitle">For teenagers and young adults seeking mental health support</p>
                
                <ul class="features-list">
                    <li>Crisis Detection & Real-time Intervention</li>
                    <li>AI-Powered S.O.S. Triage System</li>
                    <li>Interactive Calming Tools & Visual Focus</li>
                    <li>Values Discovery & Personal Growth</li>
                    <li>Empathy Mapping & Emotional Intelligence</li>
                    <li>Future Self Simulation & Goal Setting</li>
                    <li>Dialogue Practice with AI Personas</li>
                </ul>
                
                <a href="https://youth-wellness-mcp.el.r.appspot.com" 
                   class="portal-button youth-button">
                    Enter Youth Portal 🚀
                </a>
            </div>
            
            <div class="portal-card parent-card">
                <div class="portal-icon">👨‍👩‍👧‍👦</div>
                <h2 class="portal-title">Parent Portal</h2>
                <p class="portal-subtitle">For parents seeking to better understand and support their teens</p>
                
                <ul class="features-list">
                    <li>Walk a Mile - Teen Perspective Training</li>
                    <li>Generational Echo - Family Pattern Analysis</li>
                    <li>Empathy Gym - Daily Practice Scenarios</li>
                    <li>Career Path Explorer - Youth Guidance Tools</li>
                    <li>Behavioral Weather Report - Warning Signs</li>
                    <li>Resource Hub - Mental Health Directory</li>
                    <li>Communication Skills Development</li>
                </ul>
                
                <a href="https://parent-portal-dot-youth-wellness-mcp.el.r.appspot.com" 
                   class="portal-button parent-button">
                    Enter Parent Portal 💝
                </a>
            </div>
        </div>
        
        <div class="powered-by">
            <p><strong>Powered by Advanced AI Technology</strong></p>
            <div style="margin-top: 15px;">
                <span class="tech-badge">🤖 Google Vertex AI</span>
                <span class="tech-badge">⚡ Gemini 2.0 Flash</span>
                <span class="tech-badge">🔄 Model Context Protocol</span>
                <span class="tech-badge">☁️ Google Cloud Platform</span>

            </div>
        </div>
    </div>

    <script>
        // Add some interactive effects
        document.addEventListener('DOMContentLoaded', function() {
            // Animate portal cards on scroll
            const cards = document.querySelectorAll('.portal-card');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            });
            
            cards.forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(50px)';
                card.style.transition = 'all 0.8s ease';
                observer.observe(card);
            });
            
            // Track portal visits
            document.querySelectorAll('.portal-button').forEach(button => {
                button.addEventListener('click', function(e) {
                    const portal = this.textContent.includes('Youth') ? 'youth' : 'parent';
                    console.log(`Redirecting to ${portal} portal`);
                });
            });
        });
    </script>
</body>
</html>
    """

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "wellness-hub"}

@app.get("/_ah/warmup")
async def warmup():
    return {"status": "ok", "service": "wellness-hub"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Wellness Hub landing page on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
