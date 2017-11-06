from flask import Flask, render_template, request, redirect, url_for
from utilities import get_url_info, build_link
from mongoengine.errors import ValidationError
from models import FakeNews

app = Flask(__name__)


@app.route('/')
def home():
    fake_stories = FakeNews.objects()
    return render_template('index.html', stories=fake_stories)


@app.route('/edit/<storyid>', methods=['GET', 'POST'])
def edit_story(storyid=None):
    story = FakeNews.objects.get(id=storyid)
    if request.method == 'POST':
        for field in request.form:
            if request.form[field] == '':
                story[field] = None
            else:
                story[field] = request.form[field]
        try:
            story.save()
            return redirect(url_for('home'))
        except ValidationError:
            return redirect(url_for('home'))
    else:
        return render_template('new_story.html', story=story)


@app.route('/new/', methods=['GET', 'POST'])
def new_story():
    if request.method == 'POST':
        story = FakeNews()
        for field in request.form:
            if request.form[field] == '':
                story[field] = None
            else:
                story[field] = request.form[field]
        metadata = get_url_info(request.form['fake_news_url'])
        print(metadata)
        story.title = metadata['title']
        story.thumbnail = metadata['thumbnail']
        story.facebook_shares = metadata['facebook_shares']
        story.source = metadata['source']
        story.shortened_url = build_link(request.form['correct_url'])
        try:
            story.save()
            return redirect(url_for('home'))
        except ValidationError:
            return 'There was an error in the form. Try again.'
    else:
        return render_template('new_story.html', story=FakeNews())
