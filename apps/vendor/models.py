import hashlib
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import SocialMedia

from tinymce.models import HTMLField
from cities_light.models import Country, Region


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


class VendorCategory(BaseModel):
    name = models.CharField(max_length=125, unique=True, blank=False, null=False)
    
    class Meta:
        verbose_name = _('Vendor Category')
        verbose_name_plural = _('Vendor Categories')
        ordering = ['name', 'created_at', ]
        app_label = 'vendor'
      
    def __str__(self):
        return self.name


class Vendor(BaseModel):
    name = models.CharField(max_length=255, unique=True, blank=True, null=False, )
    content = HTMLField()
    logo = models.ImageField(upload_to="vendor/mainimages", blank=False,)
    category = models.ForeignKey(VendorCategory, on_delete=models.SET_NULL, blank=False, null=True, )
    is_live = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False, help_text="Marked as top vendor!")
    publication_date = models.DateTimeField(auto_now_add=True, null=False)
    # admin_user = models.ForeignKey
    # services 

    class Meta:
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')
        # ordering = ['is_top', 'name', 'is_live' ]
        ordering = ['-id']
        app_label = 'vendor'
      
    def __str__(self):
        return self.name

    def set_as_top_vendor(self):
        """ Set a vendor as Top Vendor! """
        # check if there are already 10 top vendors
        if Vendor.objects.filter(is_top = True).count() >= 10:
            raise ValueError("There are already 10 Top Vendors! ")
    
        self.is_top = True
        self.save() 
        

class VendorAddress(BaseModel):
    """ Physical address of the company """
    name = models.CharField(max_length=255, default="", verbose_name=_("address name"))
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Country"))
    state = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("state"))
    city = models.CharField(max_length=255, blank=True, verbose_name=_("city"))
    location = models.CharField(max_length=500, blank=True, default="")
    is_hq = models.BooleanField(default=False, 
                                verbose_name=_("is default"), 
                                help_text="If True it is Head Quarter office address, else it's branch office!")

    class Meta:
        verbose_name = _('Vendor address')
        verbose_name_plural = _('Vendor  Addresses')
        ordering = ['-is_hq', '-created_at']
        app_label = 'vendor'

    def __str__(self):
        address = "Head Quarter " if self.is_hq else ""
        address = f"{self.location} {self.city},{self.country}" if address == "" else address
        return address


class VendorSocialMedia(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=False )
    social_media = models.ForeignKey(SocialMedia, on_delete=models.PROTECT, blank=False)
    address = models.URLField(blank=False) 

    class Meta:
        verbose_name = _('Vendor Social Media')
        verbose_name_plural = _('Vendor Social Medias')
        ordering = ['-created_at']
        app_label = 'vendor'

    def __str__(self):    
        return f"{self.vendor.name}'s  {self.social_media.name} address"


class VendorContent(BaseModel):
    vendor = models.ForeignKey(to=Vendor, on_delete=models.CASCADE )
    header = models.CharField(max_length=255, null=False, )
    content = HTMLField()
    icon = models.ImageField(upload_to="vendor/contentIcons", blank=False,)

    class Meta:
        verbose_name = _('Vendor Content')
        verbose_name_plural = _('Vendor Contents')
        ordering = ['created_at']
        app_label = 'vendor'

    def __str__(self):    
        return f"{self.vendor.name}'s Why : {self.header}"
    

class VendorWhy(BaseModel):
    vendor:Vendor = models.ForeignKey(to=Vendor, on_delete=models.CASCADE )
    header = models.CharField(max_length=255, null=False, )
    content = HTMLField()
    icon = models.ImageField(upload_to="vendor/whyIcons", blank=False,)

    class Meta:
        verbose_name = _('Vendor Why Item')
        verbose_name_plural = _('Vendor Why Items')
        ordering = ['-created_at']
        app_label = 'vendor'

    def __str__(self):    
        return f"{self.vendor.name}'s Why : {self.header}"
    

class VendorLooking(BaseModel):
    vendor:Vendor = models.ForeignKey(to=Vendor, on_delete=models.CASCADE )
    header = models.CharField(max_length=255, null=False, )
    content = HTMLField()
    icon = models.ImageField(upload_to="vendor/lookingIcons", blank=False,)

    class Meta:
        verbose_name = _('Vendor Looking Item')
        verbose_name_plural = _('Vendor Looking Items')
        ordering = ['-created_at']
        app_label = 'vendor'

    def __str__(self):    
        return f"{self.vendor.name}'s Looking : {self.header}"
    

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


class Image(BaseModel):
    # Model for storing image metadata
    file = models.ImageField(upload_to="uploads/images/")  # Path where images are uploaded
    name = models.CharField(max_length=255, blank=True, null=True)
    checksum = models.CharField(max_length=64, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = _('Vendor Image')
        verbose_name_plural = _('Vendor Images')
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


