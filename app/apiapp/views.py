from django.http.response import JsonResponse
from rest_framework import status
from .models import Ai_text
from rest_framework.decorators import api_view


@api_view(['POST'])
def ai_texts(request):
    if request.method == 'GET':
        return JsonResponse({}, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        # Ai_text.objects.filter(imae = request.image)
        x = Ai_text.objects.get_or_create(image=request.POST['image'])[0]
        print(x)
        print(x.ai_caption)
        print(x.ai_description)
        if request.POST['model_path'] == "soul11zz/image-caption-desc-only-large":   
            x.ai_caption = request.POST['caption']
            x.save()
        elif request.POST['model_path'] == "soul11zz/image-description-large-sl-web-feb":
            x.ai_description = request.POST['description']
            x.save()
        if 1:
            return JsonResponse({"data": request.POST['image']}, status=status.HTTP_201_CREATED) 
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)
