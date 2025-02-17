import os
import sys
import django
import shutil
from os.path import join, dirname

# Add run/ to  python path
sys.path.append(join(dirname(__file__), ".."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InternationalB2BVentures.settings")
django.setup()
from django.templatetags.static import static
from django.conf import settings
from core.models import WhyUsItem, SocialMedia
from vendor.models import VendorCategory, Vendor
from notifications.models import NewsTag, Newsletter, TagCategory, Image


def copy_static_to_media(model_field_name, icon_name, static_path="imgs/icons/"):
    try:
        # make sure that the media folder exists to store icons
        model_upload_dir = model_field_name.field.upload_to
        media_dir = (settings.MEDIA_ROOT) + "/" + model_upload_dir + "/"

        if not os.path.exists(media_dir):
            os.makedirs(os.path.dirname(media_dir), exist_ok=True)

        # get static icon
        static_icon = settings.PROJECT_ROOT + static(static_path + icon_name)
        media_dst = media_dir + icon_name  # add icon name to media dir
        shutil.copyfile(static_icon, media_dst)  # copy icon file

        media_url = model_upload_dir + "/" + icon_name
        return media_url

    except Exception as e:
        print(f"Exception occurred while creating link for :  ", e)


def populate_whyus():
    demo_items = [
        # Format is {icon_name, title, content, }
        ["voucher.svg", "Gift voucher", "Refer a friend"],
        ["support.svg", "Support 24/7", "Shop with an expert"],
        ["return.svg", "Return &amp; Refund", "Free return over $200"],
        ["delivery.svg", "Free Delivery better", "From all orders over $10 let's try"],
    ]

    print(f"{'-'*50}\nStarted populating Why Us Section Items!", end="\n")
    failed = 0
    for item in demo_items:
        try:
            media_url = copy_static_to_media(WhyUsItem.icon, item[0], "imgs/template/")
            obj, is_created = WhyUsItem.objects.get_or_create(
                title=item[1], content=item[2], icon=media_url, is_published=True
            )
            msg = "Item " + "created!" if is_created else "found!"
            failed = failed + 1 if not is_created else failed

        except Exception as e:
            print("Exception while creating why us item : ", e)
            failed += 1

    print(f"Populated {len(demo_items) - failed} why us items!", end="\n\n")


def populate_vendor_cats():
    print(f"{'-'*50}\nStarted populating Vendor Categories!", end="\n")
    cats = [
        "Tech",
        "Manufacturing",
        "Biology",
        "Beverage",
        "Advertising",
        "Software Development",
        "Car Manufacturing",
    ]
    failed = 0
    for cat in cats:
        try:
            obj, is_created = VendorCategory.objects.get_or_create(name=cat)
            msg = "Item " + "created!" if is_created else "found!"
            failed = failed + 1 if not is_created else failed

        except Exception as e:
            print("Exception while creating Vendor Category : ", e)
            failed += 1
    print(f"Populated {len(cats) - failed} Vendor Categories!", end="\n\n")


def populate_vendors():
    print(f"{'-'*50}\nStarted populating Vendors!", end="\n")
    vendors = [
        # logo, name, content
        ["alpha.jpg", "Alpha Inc"],
        ["sell.svg", "Seel and Buy"],
        ["eyes.png","Owl Company",],
        ["hyperlink.jpg", "Hyperlink"],
        ["dantos.png","Dantos Inc",],
        ["jordan.png","Jordan Shoes",],
        ["jordan.png", "Clutch Corporate"],
        ["vardot.png", "Vardot Corporation"],
        ["propeller.png", "Propeller Investment Group"],

    ]

    failed = 0
    vendor_cat_id = 1
    vendor_cat_count = VendorCategory.objects.all().count()
    repeat_count = 5

    for i in range(1, repeat_count+1):
        for item in vendors:
            try:
                # rotate b/n vendor categories
                cat_id = (
                    1 if (vendor_cat_id > 7 or vendor_cat_id % vendor_cat_count == 0) else vendor_cat_id
                )
                media_url = copy_static_to_media(Vendor.logo, item[0], "imgs/logos/")

                obj, is_created = Vendor.objects.get_or_create(
                    name=f"{item[1]}{'-'+str(i) if i > 1 else ''}",
                    logo=media_url,
                    category=VendorCategory.objects.get(id=cat_id),
                    content=f"{'Demo content for demo company. ' * 30} ",
                    is_live=True,
                    is_top=True,
                )

                msg = "Item created!" if is_created else " Item found!"
                print(msg)
                failed = failed + 1 if not is_created else failed
                vendor_cat_id += 1

            except Exception as e:
                print("Exception while creating Vendor Item : ", e)
                failed += 1

        print(f"Populated {len(vendors) - failed} Vendors!", end="\n\n")


def populate_newstag_categories():
    print(f"{'-'*50}\nStarted populating Tag categories!", end="\n")
    tags = [
        "Technology",
        "Engineering",
        "Cosmetics",
    ]
    failed = 0
    for item in tags:
        try:
            obj, is_created = TagCategory.objects.get_or_create(name=item)
            msg = (
                "Tag Category Item created!"
                if is_created
                else "Tag category Item found!"
            )
            print(msg)
            failed = failed + 1 if not is_created else failed

        except Exception as e:
            print("Exception while creating Tag : ", e)
            failed += 1

    print(f"Populated {len(tags) - failed} Tags!", end="\n\n")


def populate_newstags():

    print(f"{'-'*50}\nStarted populating News Tags!", end="\n")
    tags = [
        "Tech",
        "Manufacturing",
        "Biology",
        "Beverage",
        "Advertising",
        "Software Development",
        "Car Manufacturing",
    ]
    failed = 0
    for item in tags:
        try:
            obj, is_created = NewsTag.objects.get_or_create(
                name=item, slug=item, description=item
            )
            msg = "News tag Item created!" if is_created else "News tag Item found!"
            print(msg)
            failed = failed + 1 if not is_created else failed

        except Exception as e:
            print("Exception while creating News Tag : ", e)
            failed += 1

    print(f"Populated {len(tags) - failed} News Tags!", end="\n\n")


def populate_news():

    populate_newstag_categories()

    # Make sure to create news tags
    populate_newstags()

    print(f"{'-'*50}\nStarted populating News!", end="\n")

    failed = 0
    current_tag_id = 1
    news_tag_count = NewsTag.objects.all().count()
    demo_news = [
        #  img, title,
        ["blog1.jpg","NFL has a new halftime show sponsor",],
        ["blog-2.jpg", "Actress details sexual harassment on sitcom set"],
        ["blog-3.jpg", "Selma Blair stuns in Dancing with the Stars"],
        ["blog-4.jpg", "The Woman King surprises at the box office"],
        ["blog-5.jpg", "NFL has a new halftime show sponsor "],
        ["blog-6.jpg", "The fate of Elon Musks deal to buy Twitter"],
        ["blog-7.jpg", "Binance blockchain hit by $570 million crypto"],
    ]

    repeationCount = 3
    
    for i in range(1, repeationCount+1):
        for item in demo_news:
            try:
                # rotate news tag
                current_tag_id = (
                    1
                    if current_tag_id >= news_tag_count
                    else current_tag_id % news_tag_count
                )

                obj, is_created = Newsletter.objects.get_or_create(
                    title=f"{item[1]}{"-"+str(i) if i>1 else ''}",
                    slug=f"{item[1]}{"-"+str(i) if i>1 else ''}",
                    is_published=True,
                    content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
                )

                obj.tags.add(
                    NewsTag.objects.get(id=current_tag_id),
                )

                # Add new image
                media_url = copy_static_to_media(Image.file, item[0], "imgs/page/blog/")
                news_img = Image.objects.create(
                    file=media_url,
                    checksum =f"{media_url}{"-"+str(i) if i>1 else ''}",
                )
                obj.images.add(news_img)
                obj.save()

                msg = (
                    "News Letter Item created!" if is_created else "News Letter Item found!"
                )
                print(msg)
                failed = failed + 1 if not is_created else failed
                current_tag_id += 1

            except Exception as e:
                print("Exception while creating Newsletter Item : ", e)
                failed += 1

    print(f"Populated {len(demo_news)*repeationCount - failed} News Items!", end="\n\n")


def populate_socialmedias():
    print(f"{'-'*50}\nStarted populating social media types!", end="\n")
    social_medias = [
        # Name, link
        ["Facebook", "https://www.facebook.com", ],
        ["X", "https://www.x.com"],
        ["Instagram", "https://www.instagram.com"],
        ["LinkedIn", "https://www.linkedin.com"],
        ["YouTube", "https://www.youtube.com"],
        ["Snapchat", "https://www.snapchat.com"],
        ["WhatsApp", "https://www.whatsapp.com"],
        ["Telegram", "https://www.telegram.org"],
        ["Discord", "https://discord.com"],
        ["GitHub", "https://github.com"],
        ["WeChat", "https://www.wechat.com"],
    ]
    failed = 0
    for item in social_medias:
        try:
            media_url = copy_static_to_media(SocialMedia.icon, f"{item[0].lower()}.svg", "imgs/logos/")
            obj, is_created = SocialMedia.objects.get_or_create(name = item[0], icon=media_url, link=item[1] )
            msg = "Social Media Item created!" if is_created else f"Social Media Item {obj.name} is found!"
            failed = failed + 1 if not is_created else failed
            print(msg)
            
        except Exception as e:
            print("Exception while creating Social Media : ", e)
            failed += 1
    
    print(f"Populated {len(social_medias) - failed} Social media Items!", end="\n\n")

