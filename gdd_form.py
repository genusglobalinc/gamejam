from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import traceback

app = Flask(__name__)

# Configure Flask-Mail
# Configure Flask-Mail for Mailtrap
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'b512f8a7b89a8d'
app.config['MAIL_PASSWORD'] = '867b996a31c142'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

# Initialize Flask-Mail
mail = Mail(app)

# List of questions with unique variable names
questions = [
    ("game_name", "Game Name"),
    ("game_concept", "Game concept"),
    ("genre", "Genre"),
    ("target_audience", "Target audience"),
    ("game_flow_summary", "Game flow Summary"),
    ("look_and_feel", "Look and Feel"),
    ("game_progression", "Game Progression"),
    ("mission_challenge_structure", "Mission/Challenge structure"),
    ("puzzle_structure", "Puzzle structure"),
    ("objectives", "Objectives"),
    ("play_flow", "Play flow"),
    ("physical_world_work", "How does the physical world work?"),
    ("movement_in_game", "Movement in the game"),
    ("objects", "Objects"),
    ("actions", "Actions"),
    ("combat", "Combat"),
    ("economy", "Economy"),
    ("screen_flow", "Screen Flow"),
    ("game_options", "Game Options"),
    ("replaying_and_saving", "Replaying and Saving"),
    ("cheats_and_easter_eggs", "Cheats and Easter Eggs"),
    ("story_and_narrative", "Story and Narrative"),
    ("general_look_feel_game_world", "General Look and Feel of the Game World"),
    ("areas_in_game_world", "Areas in the Game World"),
    ("characters", "Characters"),
    ("level_synopsis", "Level synopsis"),
    ("level_given_materials", "Level Given Materials"),
    ("level_events", "What happens in this level?"),
    ("training_level", "Training level"),
    ("visual_system", "Visual System"),
    ("control_system", "Control System"),
    ("audio_music_sound_effects", "Audio, music, sound effects"),
    ("help_system", "Help System"),
    ("opponent_enemy_ai", "Opponent and Enemy AI"),
    ("non_combat_friendly_characters", "Non-combat and friendly characters"),
    ("support_ai", "Support AI"),
    ("target_hardware", "Target Hardware"),
    ("development_hardware_software_engine", "Development hardware and software and Game Engine"),
    ("network_requirements", "Network Requirements"),
    ("key_assets", "Key Assets"),
    ("development_process", "Development Process"),
    ("intended_style", "Intended Style")
]

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            # Collect form data into a dictionary
            answers = {q[0]: request.form[q[0]] for q in questions}
            email = request.form['email']
            
            # Print the collected data to the console for debugging
            print("Collected Answers:")
            for k, v in answers.items():
                print(f"{k}: {v}")
            print(f"Email: {email}")
            
            # Render the GDD as HTML using the collected answers
            try:
                gdd_html = render_template('index.html', answers=answers, questions=questions)
            except Exception as e:
                print(f"Error rendering template: {e}")
                print(traceback.format_exc())
                return "An error occurred while rendering the template.", 500
            
            # Create and send the email with the GDD
            try:
                msg = Message('Your Game Design Document', recipients=[email])
                msg.html = gdd_html
                mail.send(msg)
                print("Email sent successfully")
            except Exception as e:
                print(f"Error sending email: {e}")
                print(traceback.format_exc())
                return "An error occurred while sending the email.", 500
            
            # Redirect to a thank-you page after submission
            return redirect(url_for('thank_you'))
        
        # Render the form template with questions
        return render_template('index.html', questions=questions)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
        return "An internal error occurred. Please try again later.", 500

@app.route('/thank-you')
def thank_you():
    # Simple thank-you page after form submission
    return "Thank you! Your Game Design Document has been emailed to you."

if __name__ == '__main__':
    # Run the Flask app with debug mode enabled
    app.run(host='0.0.0.0', port=5000, debug=True)
