import random
 
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse
import base64
import requests
from django.conf import settings

 
from .forms import EnquiryForm
from .models import Post, GalleryImage
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

        payload = {
            "sender": {"name": "JRF Corp Website", "email": settings.DEFAULT_FROM_EMAIL},
            "to": [{"email": settings.ENQUIRY_NOTIFY_EMAIL}],
            "replyTo": {"email": enquiry.email},
            "subject": f"New Enquiry: {enquiry.get_reason_display()}",
            "htmlContent": (
                f"<p><strong>Name:</strong> {enquiry.first_name} {enquiry.last_name}</p>"
                f"<p><strong>Email:</strong> {enquiry.email}</p>"
                f"<p><strong>Phone:</strong> {enquiry.phone}</p>"
                f"<p><strong>Address:</strong> {enquiry.address_line1}, {enquiry.city}, {enquiry.state}</p>"
                f"<p><strong>Property Type:</strong> {enquiry.get_property_type_display()}</p>"
                f"<p><strong>Reason:</strong> {enquiry.get_reason_display()}</p>"
                f"<p><strong>Description:</strong><br>{enquiry.description}</p>"
            ),
        }

        if enquiry.attachment:
            with open(enquiry.attachment.path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            payload["attachment"] = [{
                "content": encoded,
                "name": enquiry.attachment.name.split('/')[-1],
            }]

        try:
            response = requests.post(
                "https://api.brevo.com/v3/smtp/email",
                headers={
                    "accept": "application/json",
                    "api-key": settings.BREVO_API_KEY,
                    "content-type": "application/json",
                },
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Enquiry email failed to send: {e}")

        messages.success(request, "Thanks, we've received your enquiry and will be in touch shortly.")
        return redirect(reverse('home') + '#contact')

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


def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'dashboard/gallery.html', {
        'images': images,
    })

def about(request):
    historical_photos = GalleryImage.objects.filter(is_historical=True)
    return render(request, 'dashboard/about.html', {
        'historical_photos': historical_photos,
    })