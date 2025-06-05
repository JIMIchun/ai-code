from flask import Flask, render_template, Blueprint

voice_input_bp = Blueprint("voice_input", __name__)

@voice_input_bp.route('/voice-input')
def voice_input():
    return render_template('index.html')
