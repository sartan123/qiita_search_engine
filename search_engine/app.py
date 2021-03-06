from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Return index.html
    """
    if request.method == 'POST':
        keyword = request.form['keyword']
        if keyword:
            file = open('./templates/db/{}.json'.format(keyword), 'r')
            result = json.load(file)
            file.close()
            return render_template(
                'index.html',
                query=result[keyword],
                keyword=keyword)
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True  # デバッグモード有効化
    app.run(host='0.0.0.0')  # どこからでもアクセス可能に
