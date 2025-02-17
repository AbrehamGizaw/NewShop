from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from tinymce.models import HTMLField
from enum import Enum
import hashlib


class Status(Enum):
    SENT = 'sent'
    FAILED = 'failed'

    @classmethod
    def get_status_choices(cls):
        # Cache for dynamic choices
        return [(status.value, _(status.name.capitalize())) for status in cls]

# Utility function to calculate file checksum
def calculate_checksum(file):
    """
    Calculate the checksum of a file using MD5.

    :param file: A Django File or UploadedFile object.
    :return: The MD5 checksum as a hexadecimal string.
    """
    hasher = hashlib.md5()
    try:
        for chunk in file.chunks():
            hasher.update(chunk)
    except AttributeError:
        raise ValueError("Invalid file object. Ensure it has a 'chunks()' method.")
    finally:
        file.seek(0)  # Reset file pointer for further use.

    return hasher.hexdigest()


# Base Model for timestamp and soft deletion
class BaseModel(models.Model):
    # Fields to track creation, update, and soft deletion timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    removed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Removed At'))

    class Meta:
        abstract = True  # Ensures this model is only used as a base class

    def soft_delete(self):
        # Mark the record as soft-deleted by setting the removed_at timestamp
        self.removed_at = timezone.now()
        self.save()

class Image(BaseModel):
    # Model for storing image metadata
    file = models.ImageField(upload_to="uploads/images/", )  # Path where images are uploaded
    name = models.CharField(max_length=255, blank=True, null=True)
    checksum = models.CharField(max_length=64, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Automatically set the name if not provided
        if not self.name:
            self.name = self.file.name.split("/")[-1]
        # Calculate checksum for the file
        if not self.checksum:
            self.checksum = calculate_checksum(self.file)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or f"Image {self.id}"

class TagCategory(BaseModel):
    # Model for organizing tags into categories
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _('Tag Category')
        verbose_name_plural = _('Tag Categories')

    def __str__(self):
        return self.name

class NewsTag(BaseModel):
    # Tags to categorize newsletters
    name = models.CharField(max_length=125, unique=True, verbose_name=_('Tag Name'))
    slug = models.SlugField(max_length=150, unique=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    category = models.ForeignKey(TagCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Category'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('News Tags')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name


class Newsletter(BaseModel):
    # Core newsletter model
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # URL-friendly identifier
    content = HTMLField()  # Rich text content
    images = models.ManyToManyField(Image, related_name='newsletters', blank=True)  # Associated images
    tags = models.ManyToManyField(NewsTag, related_name='newsletters', blank=True)  # Associated tags
    is_published = models.BooleanField(default=False)  # Publication status
    publication_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Publication Date'))

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ['-publication_date','-created_at','title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        # Ensure that unpublished newsletters do not have a publication date
        from django.core.exceptions import ValidationError
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        if self.publication_date and not self.is_published:
            raise ValidationError("Unpublished newsletters should not have a publication date.")

    def send_to_all_subscribers(self):
        # Logic to send the newsletter to all active subscribers
        subscribers = self.subscribers.filter(is_active=True)
        for subscriber in subscribers:
            NewsletterSent.objects.create(subscriber=subscriber, newsletter=self, status=NewsletterSent.Status.SENT.value)

class Subscriber(BaseModel):
    # Model to manage newsletter subscribers
    email = models.EmailField(max_length=200, unique=True)
    last_news_sent_date = models.DateTimeField(null=True, blank=True)
    subscription_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Subscription Date'))
    email_verified_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Email Verified At'))
    is_active = models.BooleanField(default=False)  # Indicates if the subscriber is active

    class Meta:
        ordering = ['email', 'created_at', 'is_active']
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.email

    def toggle_subscription(self, is_active):
        # Activate or deactivate the subscription
        self.is_active = is_active
        if is_active:
            self.subscription_date = timezone.now()
        self.save()

    def validate_email_format(self):
        # Explicitly validate the email format
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError(f"The email {self.email} is not a valid email address.")

    def deactivate_unverified(self, timeframe_days):
        # Deactivate subscribers who have not verified their email within the given timeframe
        if not self.email_verified_at and (timezone.now() - self.subscription_date).days > timeframe_days:
            self.is_active = False
            self.save()

class NewsletterSent(BaseModel):
    # Enum for status choices

    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)  # When the newsletter was sent
    status = models.CharField(
        max_length=50,
        choices=Status.get_status_choices(),
        default=Status.SENT.value
    )

    class Meta:
        ordering = ['-sent_date']
        verbose_name = _('Newsletter Sent Log')
        verbose_name_plural = _('Newsletter Sent Logs')
        unique_together = ('subscriber', 'newsletter')

    def __str__(self):
        return f"{self.sent_date} - {self.status} - {self.newsletter.title} to {self.subscriber.email}"

    def retry_failed(self):
        # Retry sending a failed newsletter
        if self.status == self.Status.FAILED.value:
            self.status = self.Status.SENT.value  # Mark as successfully sent
            self.save()
            return True
        return False

    # @staticmethod
    # def log_failure(subscriber, newsletter, error_message):
    #     # Log a failed newsletter sending attempt
    #     NewsletterSent.objects.create(
    #         subscriber=subscriber,
    #         newsletter=newsletter,
    #         status=NewsletterSent.Status.FAILED.value
    #     )