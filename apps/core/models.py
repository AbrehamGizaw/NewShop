from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    removed_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Removed At'))

    class Meta:
        abstract = True
        get_latest_by = "created_at"

    def soft_delete(self):
        self.removed_at = timezone.now()
        self.save()

    @property
    def is_deleted(self):
        return self.removed_at is not None


class WhyUsItem(BaseModel):
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    content = HTMLField(
        null=False,
        max_length=150,
        help_text=_("Ensure the content does not exceed 150 characters for a smooth interface.")
    )
    icon = models.ImageField(upload_to="core/whyus", blank=False, null=False, default="default/icon.png")
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Why Us Item')
        verbose_name_plural = _('Why Us Items')
        ordering = ['is_published', 'created_at']
        app_label = 'core'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if len(self.content) > 150:
            raise ValueError(_("Content exceeds the maximum length of 150 characters."))


class TermsAndConditions(BaseModel):
    """The content of the terms and conditions page."""
    content = HTMLField(blank=False, null=False)

    class Meta:
        verbose_name = _('Terms and Conditions')
        verbose_name_plural = _('Terms and Conditions')
        ordering = ['created_at']
        app_label = 'core'

    def __str__(self):
        return _('Terms and Conditions')


class SocialMedia(BaseModel):
    """ Setting model for adding social medias! """

    name = models.CharField(max_length=255, null=False, verbose_name="Social Media Name" )
    icon = models.ImageField(upload_to="core/socialMediaIcons", blank=False,)
    link = models.URLField(verbose_name="Social Media Link (Optional)", blank=True)
   
    class Meta:
        verbose_name = _('Social Media')
        verbose_name_plural = _('Social Medias')
        ordering = ['name']
        app_label = 'core'

    def __str__(self):    
        return self.name
    

# class ContactUs(BaseModel):
    # name = models.CharField(max_length=255, default="", verbose_name=_("address name"))
    # country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Country"))
    # state = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("state"))
    # city = models.CharField(max_length=255, blank=True, verbose_name=_("city"))
    # location = models.CharField(max_length=500, blank=True, default="")
    # is_hq = models.BooleanField(default=False, verbose_name=_("is default"), help_text="If True it is Head Quarter office address, else it's branch office!")
