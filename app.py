from flask import Flask, render_template, request
import aiml

app = Flask(__name__)
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

conversation = []  # List to store chat history

@app.route("/", methods=["GET", "POST"])
def chatbot():
    global conversation
    ask_location = False
    
    if request.method == "POST":
        user_input = request.form.get("message")
        location = request.form.get("location")

        if user_input:
            response = kernel.respond(user_input)
            conversation.append({"user": True, "text": user_input})  # Store user message
            conversation.append({"user": False, "text": response})   # Store bot response

            # If bot asks for location
            if "your location" in response.lower():
                ask_location = True

        elif location:
            response = kernel.respond(location)
            conversation.append({"user": True, "text": location})
            conversation.append({"user": False, "text": response})
            ask_location = False

    return render_template("index.html", conversation=conversation, ask_location=ask_location)

if __name__ == "__main__":
    app.run(debug=True)

import time
if not hasattr(time, 'clock'):
    time.clock = time.perf_counter
