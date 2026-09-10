from django.db import models
from django.urls import reverse
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Matches an icon key used in the template")
    short_description = models.CharField(max_length=200, help_text="Shown on the homepage service grid")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    description = models.TextField(help_text="Shown on the service's own page")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})


class Enquiry(models.Model):
    REASON_CHOICES = [
        ('water_leak', 'Water Leak (Outside Home)'),
        ('sewer_drain', 'Sewer/Drain Break or Back Up'),
        ('drainage', 'Drainage Issues'),
        ('excavation_quote', 'Excavation Quote'),
        ('other', 'Other'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('private', 'Private Property'),
        ('commercial', 'Commercial Property'),
        ('municipal', 'Municipal / Government'),
    ]

    STATE_CHOICES = [
        ('MA', 'Massachusetts'),
        ('RI', 'Rhode Island'),
        ('NH', 'New Hampshire'),
        ('CT', 'Connecticut'),
        ('ME', 'Maine'),
        ('VT', 'Vermont'),
        ('NY', 'New York'),
        ('OTHER', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='MA')
    phone = models.CharField(max_length=20)
    description = models.TextField()
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPE_CHOICES, default='private')
    attachment = models.FileField(upload_to='enquiries/%Y/%m/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f"{self.first_name} {self.last_name} \u2014 {self.get_reason_display()}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100, blank=True, help_text="Staff name to show as the author")
    excerpt = models.CharField(max_length=250, help_text="Short summary shown on the blog list page, works as meta description for Search Engine Optimisation. Make it a proper sentence but try to catch as many keywords as possible")
    content = models.TextField(help_text="Main body of the post. Line breaks are preserved.")
    image = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
 
    class Meta:
        ordering = ['-published_at']
 
    def __str__(self):
        return self.title
 
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
 
class GalleryImage(models.Model):
    caption = models.CharField(max_length=200, blank=True, help_text="Optional, shown under the photo")
    image = models.ImageField(upload_to='gallery/%Y/%m/')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['order', '-uploaded_at']
 
    def __str__(self):
        return self.caption or f"Gallery photo #{self.pk}"
 