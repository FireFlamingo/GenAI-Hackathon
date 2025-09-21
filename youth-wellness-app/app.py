from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
from crisis_detector import CrisisDetector

app = FastAPI()
detector = CrisisDetector()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>S.O.S. Mental Wellness System</title>
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
                max-width: 600px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                border-radius: 20px; 
                text-align: center; 
            }
            
            .sos-button { 
                background: #ff4444; 
                color: white; 
                padding: 25px 50px; 
                font-size: 24px; 
                font-weight: bold;
                border: none; 
                border-radius: 50px; 
                cursor: pointer; 
                width: 100%;
                margin: 20px 0;
            }
            
            .sos-button:hover { 
                background: #cc3333; 
            }
            
            .send-button {
                background: #4299e1; 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer;
                font-size: 16px;
                margin-top: 15px;
            }
            
            .send-button:hover {
                background: #3182ce;
            }
            
            #user-input {
                width: 100%; 
                height: 100px; 
                padding: 15px; 
                border: 2px solid #ddd; 
                border-radius: 10px; 
                font-size: 16px;
                margin: 10px 0;
            }
            
            .triage-screen {
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
            
            .intervention-screen {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100vh;
                background: #1a202c;
                color: white;
                display: none;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
                z-index: 1001;
            }
            
            .triage-option {
                background: white;
                color: #333;
                padding: 20px;
                margin: 10px;
                border: none;
                border-radius: 15px;
                cursor: pointer;
                font-size: 18px;
                width: 90%;
                max-width: 500px;
                text-align: left;
            }
            
            .triage-option:hover {
                background: #f0f0f0;
            }
            
            .exit-button {
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(255,255,255,0.3);
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 18px;
            }
            
            .breathing-circle {
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: radial-gradient(circle, #4299e1, #2b6cb0);
                margin: 20px;
                transition: transform 4s ease-in-out;
            }
            
            .breathing-expanded { transform: scale(1.3); }
            .breathing-contracted { transform: scale(0.7); }
            
            .visual-focus {
                width: 300px;
                height: 300px;
                border-radius: 50%;
                background: conic-gradient(from 0deg, #805ad5, #d69e2e, #38b2ac, #805ad5);
                animation: rotate 20s linear infinite;
                margin: 20px;
            }
            
            @keyframes rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .intervention-content {
                text-align: center;
                max-width: 600px;
            }
            
            .step-container {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                margin: 20px;
            }
            
            .done-button {
                background: #48bb78;
                color: white;
                padding: 15px 25px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                margin: 15px;
            }
            
            .done-button:hover {
                background: #38a169;
            }
            
            #response {
                margin-top: 20px;
                padding: 15px;
                border-radius: 8px;
                display: none;
            }
            
            .success {
                background: #c6f6d5;
                color: #22543d;
            }
        </style>
    </head>
    <body>
        <!-- Main Interface - EXACT SAME AS WORKING VERSION -->
        <div id="main-interface" class="container">
            <h1>🤖 Your AI Mental Wellness Co-pilot</h1>
            <p style="color: #666; margin-bottom: 30px;">I'm here to support you through any moment</p>
            
            <button class="sos-button" onclick="testSOSButton()">
                🚨 S.O.S. - I Need Help Right Now
            </button>
            
            <div>
                <textarea id="user-input" placeholder="How are you feeling today? I'm here to listen..."></textarea>
                <button class="send-button" onclick="testSendButton()">Send Message</button>
                <div id="response"></div>
            </div>
        </div>
        
        <!-- S.O.S. Triage Screen -->
        <div id="triage-screen" class="triage-screen">
            <button class="exit-button" onclick="exitSOS()">✕ Exit</button>
            <h2 style="color: #2d3748; margin-bottom: 30px; text-align: center;">Right now, what do you feel the most?</h2>
            
            <button class="triage-option" onclick="selectOption('visual_focus')">
                💭 My thoughts are racing and I can't stop them.
            </button>
            <button class="triage-option" onclick="selectOption('box_breathing')">
                💓 My heart is pounding and I can't breathe.
            </button>
            <button class="triage-option" onclick="selectOption('grounding_543')">
                🌫️ Everything feels unreal, like I'm in a fog.
            </button>
            <button class="triage-option" onclick="selectOption('emergency_soundscape')">
                😔 I feel a sudden, heavy wave of sadness or emptiness.
            </button>
            <button class="triage-option" onclick="selectOption('muscle_relaxation')">
                ⚡ My body is tense, restless, and wants to escape.
            </button>
            <button class="triage-option" onclick="selectOption('emergency_soundscape')">
                🧊 I just feel numb and frozen.
            </button>
        </div>
        
        <!-- Intervention Screen -->
        <div id="intervention-screen" class="intervention-screen">
            <button class="exit-button" onclick="exitSOS()">✕ Exit</button>
            <div id="intervention-content" class="intervention-content"></div>
            <button class="done-button" onclick="exitSOS()" style="margin-top: 30px;">I'm Feeling Better</button>
        </div>

        <script>
            // EXACT SAME FUNCTION NAMES AS WORKING VERSION
            console.log('=== SCRIPT LOADED ===');
            
            function testSOSButton() {
                console.log('=== S.O.S. BUTTON CLICKED ===');
                document.getElementById('main-interface').style.display = 'none';
                document.getElementById('triage-screen').style.display = 'flex';
            }
            
            function testSendButton() {
                console.log('=== SEND BUTTON CLICKED ===');
                const input = document.getElementById('user-input').value.trim();
                
                if (!input) {
                    alert('Please share how you\\'re feeling first!');
                    return;
                }
                
                console.log('User input:', input);
                
                // Show immediate response
                const response = document.getElementById('response');
                response.innerHTML = '<strong>Your AI Co-pilot is listening.</strong><br>Thanks for sharing. Analyzing your message...';
                response.className = 'success';
                response.style.display = 'block';
                
                // Check for crisis
                fetch('/check-crisis', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: input})
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Crisis check result:', data);
                    if (data.is_crisis) {
                        response.innerHTML += '<br><strong>I detected you might need immediate support. Launching S.O.S. mode...</strong>';
                        setTimeout(testSOSButton, 2000);
                    } else {
                        response.innerHTML = '<strong>Your AI Co-pilot is listening.</strong><br>Thanks for sharing. I\\'m here whenever you need support. 💚';
                    }
                })
                .catch(error => {
                    console.error('API Error:', error);
                    response.innerHTML = 'I\\'m here for you. If you need immediate help, please click the S.O.S. button.';
                });
            }
            
            function exitSOS() {
                console.log('=== EXITING S.O.S. MODE ===');
                document.getElementById('triage-screen').style.display = 'none';
                document.getElementById('intervention-screen').style.display = 'none';
                document.getElementById('main-interface').style.display = 'block';
                
                // Clear any running timers
                clearInterval(window.breathingTimer);
                clearTimeout(window.stepTimer);
            }
            
            function selectOption(intervention) {
                console.log('=== SELECTED INTERVENTION:', intervention, '===');
                document.getElementById('triage-screen').style.display = 'none';
                document.getElementById('intervention-screen').style.display = 'flex';
                
                // Show intervention
                showIntervention(intervention);
            }
            
            function showIntervention(type) {
                const content = document.getElementById('intervention-content');
                
                if (type === 'box_breathing') {
                    content.innerHTML = `
                        <h2>Interactive Box Breathing</h2>
                        <p>Follow the circle to regulate your breathing and calm your heart rate</p>
                        <div class="breathing-circle" id="breathing-circle"></div>
                        <p id="breathing-text" style="font-size: 20px; margin-top: 20px;">Get ready to breathe...</p>
                    `;
                    setTimeout(startBreathing, 2000);
                    
                } else if (type === 'visual_focus') {
                    content.innerHTML = `
                        <h2>Calming Visual Focus</h2>
                        <p>Focus on the center of this animation to interrupt racing thoughts</p>
                        <div class="visual-focus"></div>
                        <p style="font-size: 18px; margin-top: 20px;">Let your thoughts follow the gentle movement</p>
                    `;
                    
                } else if (type === 'grounding_543') {
                    content.innerHTML = `
                        <h2>5-4-3-2-1 Grounding</h2>
                        <p>This will help bring you back to the present moment</p>
                        <div id="grounding-steps"></div>
                    `;
                    setTimeout(startGrounding, 1000);
                    
                } else if (type === 'muscle_relaxation') {
                    content.innerHTML = `
                        <h2>Guided Muscle Relaxation</h2>
                        <p>Release physical tension through guided exercises</p>
                        <div id="muscle-steps"></div>
                    `;
                    setTimeout(startMuscleRelaxation, 1000);
                    
                } else if (type === 'emergency_soundscape') {
                    content.innerHTML = `
                        <h2>Safe Space Soundscape</h2>
                        <div style="width: 100%; height: 200px; background: linear-gradient(45deg, #2d3748, #4a5568); border-radius: 15px; margin: 20px 0;"></div>
                        <h3 style="color: #48bb78; margin: 30px 0;">You are safe. This feeling will pass. You are not alone.</h3>
                        <p style="font-size: 18px;">Just breathe. You don't need to do anything else right now.</p>
                        <p style="font-size: 16px; margin-top: 20px; opacity: 0.8;">Take all the time you need here.</p>
                    `;
                }
            }
            
            function startBreathing() {
                const circle = document.getElementById('breathing-circle');
                const text = document.getElementById('breathing-text');
                let phase = 0;
                const phases = ['Breathe in slowly...', 'Hold your breath...', 'Breathe out slowly...', 'Hold empty...'];
                const classes = ['breathing-expanded', '', 'breathing-contracted', ''];
                
                function breathingCycle() {
                    text.textContent = phases[phase];
                    circle.className = 'breathing-circle ' + (classes[phase] || '');
                    phase = (phase + 1) % 4;
                }
                
                breathingCycle();
                window.breathingTimer = setInterval(breathingCycle, 4000);
                
                // Stop after 2 minutes
                setTimeout(() => {
                    clearInterval(window.breathingTimer);
                    text.textContent = 'Great work! Continue breathing naturally.';
                    circle.className = 'breathing-circle';
                }, 120000);
            }
            
            function startGrounding() {
                const steps = [
                    {count: 5, sense: 'see', examples: ['a wall', 'your hands', 'a door', 'the ceiling', 'a color']},
                    {count: 4, sense: 'touch', examples: ['your clothes', 'the chair', 'your hair', 'a surface']},
                    {count: 3, sense: 'hear', examples: ['your breathing', 'distant sounds', 'air conditioning']},
                    {count: 2, sense: 'smell', examples: ['the air', 'soap', 'food', 'fabric']},
                    {count: 1, sense: 'taste', examples: ['your mouth', 'toothpaste', 'coffee', 'neutral']}
                ];
                
                let currentStep = 0;
                const container = document.getElementById('grounding-steps');
                
                function showGroundingStep() {
                    if (currentStep >= steps.length) {
                        container.innerHTML = `
                            <div class="step-container">
                                <h2 style="color: #48bb78;">Perfect!</h2>
                                <h3>You are here. You are present. You are safe.</h3>
                                <p>You've successfully grounded yourself in this moment.</p>
                            </div>
                        `;
                        return;
                    }
                    
                    const step = steps[currentStep];
                    container.innerHTML = `
                        <div class="step-container">
                            <h3>Find ${step.count} things you can ${step.sense}</h3>
                            <p style="margin: 15px 0;">Examples: ${step.examples.join(', ')}</p>
                            <button class="done-button" onclick="nextGroundingStep()">Found them - Next</button>
                        </div>
                    `;
                }
                
                window.nextGroundingStep = function() {
                    currentStep++;
                    showGroundingStep();
                }
                
                showGroundingStep();
            }
            
            function startMuscleRelaxation() {
                const muscles = [
                    {name: 'hands', tense: 'Make tight fists', release: 'Let your hands fall loose'},
                    {name: 'arms', tense: 'Pull your arms tight to your chest', release: 'Let your arms drop heavy'},
                    {name: 'shoulders', tense: 'Lift shoulders to your ears', release: 'Drop shoulders down'},
                    {name: 'face', tense: 'Scrunch your face tight', release: 'Let your face go soft'},
                    {name: 'legs', tense: 'Straighten and tense your legs', release: 'Let your legs go heavy'}
                ];
                
                let currentMuscle = 0;
                const container = document.getElementById('muscle-steps');
                
                function showMuscleStep() {
                    if (currentMuscle >= muscles.length) {
                        container.innerHTML = `
                            <div class="step-container">
                                <h2 style="color: #48bb78;">Relaxation Complete</h2>
                                <p style="font-size: 18px;">Notice how much more relaxed your body feels now.</p>
                                <p style="margin-top: 15px;">Take a moment to appreciate this calm feeling.</p>
                            </div>
                        `;
                        return;
                    }
                    
                    const muscle = muscles[currentMuscle];
                    container.innerHTML = `
                        <div class="step-container">
                            <h3>${muscle.name.charAt(0).toUpperCase() + muscle.name.slice(1)}</h3>
                            <p><strong>Tense:</strong> ${muscle.tense}</p>
                            <p><strong>Now release:</strong> ${muscle.release}</p>
                            <p style="font-size: 14px; opacity: 0.8;">Hold tension for 5 seconds, then completely relax</p>
                            <button class="done-button" onclick="nextMuscleStep()">Done - Next Group</button>
                        </div>
                    `;
                }
                
                window.nextMuscleStep = function() {
                    currentMuscle++;
                    showMuscleStep();
                }
                
                showMuscleStep();
            }
            
            // Test elements when page loads
            window.addEventListener('load', function() {
                console.log('=== PAGE LOADED ===');
                console.log('S.O.S. button exists:', !!document.querySelector('.sos-button'));
                console.log('Send button exists:', !!document.querySelector('.send-button'));
            });
        </script>
    </body>
    </html>
    """

@app.post("/check-crisis")
async def check_crisis(request: Request):
    try:
        data = await request.json()
        result = detector.detect_crisis(data["text"])
        return result
    except Exception as e:
        print(f"Error in check_crisis: {e}")
        return {"is_crisis": False, "error": str(e)}

@app.get("/analytics")
async def get_analytics():
    try:
        return detector.get_crisis_analytics()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
