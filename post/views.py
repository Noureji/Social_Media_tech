from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Board, Topic, Post
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models import Count, Q
from .models import Like
from django.db import models
from .models import Notification

def home(request):
    return render(request, 'index.html', {
        'bordes': Board.objects.all()
    })




@login_required
def show(request, bord_id):
    # Récupérer le board
    board = get_object_or_404(Board, id=bord_id)

    # Gestion du POST pour créer un topic et post directement depuis la page
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not subject or not message:
            messages.error(request, "Tous les champs sont obligatoires")
        else:
            topic = Topic.objects.create(
                subject=subject,
                bord=board,
                created_by=request.user
            )
            Post.objects.create(
                message=message,
                topic=topic,
                created_by=request.user
            )
            messages.success(request, "Post créé avec succès")
            return redirect('show', bord_id=bord_id)

    # ✅ Annotation pour total des vues des posts par topic
    topic_of_board = board.topics.annotate(
        total_views=Sum('posts__views')  # Somme des vues de tous les posts d'un topic
    )

    # Si aucun post n'a de vue, total_views sera None, donc on peut remplacer par 0 dans le template
    # {{ topic.total_views|default:0 }}

    return render(request, 'show.html', {
        'board': board,
        'topic_of_board': topic_of_board
    })


@login_required
def create(request, bord_id):
    board = get_object_or_404(Board, id=bord_id)

    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not subject or not message:
            messages.error(request, "Tous les champs sont obligatoires")
        else:
            topic = Topic.objects.create(
                subject=subject,
                bord=board,
                created_by=request.user
            )
            Post.objects.create(
                message=message,
                topic=topic,
                created_by=request.user
            )

            messages.success(request, "Post created successfully")
            return redirect('show', bord_id=bord_id)

    return render(request, 'NewTobic.html', {
        'board': board
    })

from django.db.models import Count, Q

@login_required
def tobishow(request, bord_id, tobic_id):
    board = get_object_or_404(Board, id=bord_id)
    topic = get_object_or_404(Topic, id=tobic_id)

    posts = Post.objects.filter(topic=topic).annotate(
        likes_count=Count('likes'),
        liked_by_user=Count('likes', filter=Q(likes__user=request.user))
    ).order_by('-created_at')

    # Incrémenter les vues pour chaque post seulement si pas déjà consulté en session
    for post in posts:
        session_key = f'viewed_post_{post.id}'
        if not request.session.get(session_key):
            post.views += 1
            post.save()
            request.session[session_key] = True

    return render(request, 'tobisow.html', {
        'board': board,
        'tobic': topic,
        'posts': posts
    })


@login_required
def create_post(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()

        if not message:
            messages.error(request, "Le message est obligatoire")
        else:
            Post.objects.create(
                message=message,
                topic=topic,
                created_by=request.user
            )

    return redirect('tobishow', topic.bord.id, topic.id)

# views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

            # 🔔 notification
            if post.created_by != request.user:
                Notification.objects.create(
                    to_user=post.created_by,
                    from_user=request.user,
                    post=post,
                    notification_type='comment'
                )

    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if created:
        if post.created_by != request.user:
            Notification.objects.create(
                to_user=post.created_by,
                from_user=request.user,
                post=post,
                notification_type='like'
            )
    else:
        like.delete()

    return redirect(request.META.get('HTTP_REFERER'))

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Board



@staff_member_required
def board_delete(request, id):
    board = get_object_or_404(Board, id=id)

    if request.method == "POST":
        board.delete()
        return redirect('index')

    return render(request, 'board_delete.html', {'board': board})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    views = models.PositiveIntegerField(default=0)
    session_key = f'viewed_post_{post_id}'
    if not request.session.get(session_key):
        post.views += 1
        post.save()
        request.session[session_key] = True

    return render(request, 'tobisow.html', {'post': post})

