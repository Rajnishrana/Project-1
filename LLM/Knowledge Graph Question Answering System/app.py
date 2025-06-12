from flask import Flask, request, render_template_string
from ask_function import ask

app = Flask(__name__)

HTML = '''
<!doctype html>
<title>Knowledge Graph QA</title>
<h1>Ask a question:</h1>
<form method=post>
  <input type=text name=question size=50>
  <input type=submit value=Ask>
</form>
{% if answer %}
<h2>Answer: {{ answer }}</h2>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    answer = None
    if request.method == 'POST':
        question = request.form['question']
        answer = ask(question)
    return render_template_string(HTML, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
