from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm

"""
1) 처음에는 GET 으로 폼 인스턴스를 만들고
2) 폼 데이터가 정상적인 경우 Image 인스턴스를 생성시키고, 아직 데이터베이스에 쓰지 않는다(commit=False)
3) 현재 사용자를 Image 인스턴스에 레퍼런스를 준다.
4) 이제 데이터 베이스에 저장
5) 성공 메시지를 출력 하고 이미지가 저장된 URL으로 되돌린다.
"""
@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request,'이미지가 성공적으로 추가되었습니다.')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                  'form': form})


