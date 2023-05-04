from flask import Flask, request, render_template, redirect
import openai

openai.api_key = 'YOUR_API_KEY_HERE'

server = Flask(__name__)

def send_gpt(prompt):
    try:
        response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return e

@server.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if len(request.form['question']) < 1:
            return render_template(
                'home.html', question="NULL", res="Question can't be empty!")
        question = request.form['question']
        print("======================================")
        print("Receive the question:", question)
        res = send_gpt(question)
        print("Q：\n", question)
        print("A：\n", res)

        return redirect('/results?question={}&res={}'.format(question, res))
    return render_template('home.html', question=0)

@server.route('/results')
def results():
    question = request.args.get('question')
    res = request.args.get('res')
    return render_template('results.html', question=question, res=res)

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=80)
