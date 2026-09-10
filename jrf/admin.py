from django.contrib import admin
from .models import Enquiry, Service, Post, GalleryImage


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'reason', 'submitted_at')
    list_filter = ('reason', 'property_type', 'submitted_at')
    readonly_fields = ('submitted_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'published_at')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_at',)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'is_historical', 'order', 'uploaded_at')
    list_filter = ('is_historical',)
    ordering = ('order', '-uploaded_at')
 