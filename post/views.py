from django.shortcuts import render ,redirect ,get_object_or_404
from .models import Post,Topic
from .models import Board
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    bordes=Board.objects.all()
    return render(request,'index.html',{'bordes':bordes})
@login_required
def show(request,bord_id):
    if request.method == 'POST': 
        subject=request.POST['subject']
        message=request.POST['message']
        topic = Topic.objects.create(
            subject=subject,
            bord_id=bord_id,
            created_by=request.user

        )
        Post.objects.create(
            message=message,
            topic =topic,
            created_by=request.user

        )
    else :   
        topic_of_board=Topic.objects.filter(bord_id=bord_id)
        post = Board.objects.get(pk=int(bord_id))
   
    return render(request , 'show.html',{'post':post ,"topic_of_board":topic_of_board})
@login_required
def create (request,bord_id):
    post = Board.objects.get(id=bord_id)
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        
        if not subject or not message:
            messages.error(request, "Tous les champs sont obligatoires")
            return redirect(request.META.get('HTTP_REFERER'))
        topic = Topic.objects.create(
            subject=subject,
            bord_id=bord_id,
            created_by=request.user

        )
        Post.objects.create(
            message=message,
            topic =topic,
            created_by=request.user

        )
        
        return redirect('show',bord_id=bord_id)
    return render(request,'NewTobic.html',{"bord_id":post})

@login_required
def tobishow(request,bord_id,tobic_id):
    board = Board.objects.get(id=bord_id)
    
    tobic = Topic.objects.get(id=tobic_id)
    posts = tobic.posts.order_by('-created_at')

    return render(request , 'tobisow.html',{'tobic':tobic,'board':board,'posts':posts})




def create_post(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method == 'POST':

        message = request.POST.get('message', '').strip()
        
        
        if  not message:
            messages.error(request, "❌ Échec de l’enregistrement : tous les champs obligatoires doivent être renseignés.")
            return redirect(request.META.get('HTTP_REFERER'))
        Post.objects.create(
            message=message,
            topic=topic,
            created_by=request.user
        )

    return redirect('tobishow', topic.bord.id, topic.id)
