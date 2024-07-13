from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.your-email-provider.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

mail = Mail(app)

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
    if request.method == 'POST':
        answers = {q[0]: request.form[q[0]] for q in questions}
        email = request.form['email']
        
        # Render the GDD as HTML
        gdd_html = render_template('gdd.html', answers=answers, questions=questions)

        # Send the email
        msg = Message('Your Game Design Document', recipients=[email])
        msg.html = gdd_html
        mail.send(msg)
        
        return redirect(url_for('thank_you'))
    return render_template('index.html', questions=questions)

@app.route('/thank-you')
def thank_you():
    return "Thank you! Your Game Design Document has been emailed to you."

if __name__ == '__main__':
    app.run(debug=True)
