from django.shortcuts import render


def emails_view(request, uid):
    context = {
        'uid': uid
    }
    return render(request, 'emails.html', context=context)
