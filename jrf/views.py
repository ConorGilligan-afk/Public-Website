import random
 
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
 
from .forms import EnquiryForm
from .models import Post
from .services_data import SERVICES, get_service

def _new_captcha(request):
    a, b = random.randint(1, 9), random.randint(1, 9)
    request.session['captcha_a'] = a
    request.session['captcha_b'] = b
    return a, b


def home(request):
    a, b = _new_captcha(request)
    form = EnquiryForm()
    return render(request, 'dashboard/home.html', {
        'form': form,
        'captcha_a': a,
        'captcha_b': b,
        'services': SERVICES,
    })


def service_detail(request, slug):
    service = get_service(slug)
    if service is None:
        raise Http404("Service not found")
    other_services = [s for s in SERVICES if s['slug'] != slug]
    return render(request, 'dashboard/service_detail.html', {
        'service': service,
        'other_services': other_services,
    })


def enquiry_submit(request):
    if request.method != 'POST':
        return redirect('home')

    captcha_a = request.session.get('captcha_a')
    captcha_b = request.session.get('captcha_b')
    form = EnquiryForm(request.POST, request.FILES, captcha_a=captcha_a, captcha_b=captcha_b)

    if form.is_valid():
        enquiry = form.save(commit=False)
        enquiry.save()

        email = EmailMessage(
            subject=f"New Enquiry: {enquiry.get_reason_display()}",
            body=(
                f"Name: {enquiry.first_name} {enquiry.last_name}\n"
                f"Email: {enquiry.email}\n"
                f"Phone: {enquiry.phone}\n"
                f"Address: {enquiry.address_line1}, {enquiry.city}, {enquiry.state}\n"
                f"Property Type: {enquiry.get_property_type_display()}\n"
                f"Reason: {enquiry.get_reason_display()}\n\n"
                f"Description:\n{enquiry.description}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ENQUIRY_NOTIFY_EMAIL],
            reply_to=[enquiry.email],
        )
        if enquiry.attachment:
            email.attach_file(enquiry.attachment.path)
        email.send(fail_silently=False)

        messages.success(request, "Thanks, we've received your enquiry and will be in touch shortly.")
        return redirect('home')

    # invalid submission: refresh the captcha and re-render with errors
    a, b = _new_captcha(request)
    return render(request, 'dashboard/home.html', {
        'form': form,
        'captcha_a': a,
        'captcha_b': b,
        'services': SERVICES,
    })


def post_list(request):
    published = Post.objects.filter(is_published=True, published_at__lte=timezone.now())
    paginator = Paginator(published, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/post_list.html', {
        'page_obj': page_obj,
    })
 
 
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True, published_at__lte=timezone.now())
    recent_posts = Post.objects.filter(
        is_published=True, published_at__lte=timezone.now()
    ).exclude(slug=slug)[:4]
    return render(request, 'dashboard/post_detail.html', {
        'post': post,
        'recent_posts': recent_posts,
    })
 