from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput
from watson_developer_cloud import LanguageTranslatorV3


language_translator=LanguageTranslatorV3(
    version='2018-05-01',
    iam_apikey='Jo0I4-nXNuW9jOT_2oMMAoi4A2YFUoIp62XlNlLIFLUq',
    url='https://gateway.watsonplatform.net/language-translator/api'
    )



service = ToneAnalyzerV3(
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    # url='https://gateway.watsonplatform.net/tone-analyzer/api',
    username='b38255c6-41a5-4643-b9e7-1bf41be3872c',
    password='OJufNNKOLHMl',
    version='2017-09-26')

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    for post in posts:
        posting = post.text

        translation = language_translator.translate(
            text=post.text, model_id='en-es').get_result()
        obj = (json.dumps(translation, indent=2, ensure_ascii=False))
        print(obj)
        obj2 = json.loads(obj)
        post.obj2 = obj2['translations'][0]['translation']
        post.w_count = obj2['word_count']
        post.c_count = obj2['character_count']

        tone_input = ToneInput(post.text)
        tone = service.tone(tone_input=tone_input, content_type="application/json")
        tone2 = str(tone)
        tone_data = json.loads(tone2)
        print(tone_data)
        post.tone_score1 = tone_data['result']['document_tone']['tones'][0]['score']
        post.tone_score2 = tone_data['result']['document_tone']['tones'][1]['score']
        post.tone_name1 = tone_data['result']['document_tone']['tones'][0]['tone_name']
        post.tone_name2 = tone_data['result']['document_tone']['tones'][1]['tone_name']
        print(post.tone_score1)
        print(post.tone_score2)
        print(post.tone_name1)
        print(post.tone_name2)

        post.tone3 = (tone2[1:500])

        print(post.tone3)

    return render(request, 'blog/post_list.html', {'posts' : posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

