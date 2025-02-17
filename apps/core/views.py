from django.shortcuts import render
from django.views.generic import View
from vendor.models import Vendor, VendorCategory
from core.models import WhyUsItem
from notifications.models import Newsletter
from django.db.models import Q

class Index(View):
    def get(self, *args, **kwargs):
        vendors = Vendor.objects.filter(is_live = True)
        vendor_cats = VendorCategory.objects.all()
        whyus = WhyUsItem.objects.filter(is_published = True)
        news = Newsletter.objects.all()[:5] #Fetch top 5 only

        return render(self.request, "index.html", {"vendor_cats":vendor_cats,
                                                   "vendors":vendors, 
                                                   "whyus":whyus,
                                                   "news":news
                                                    }
                                                )

def SearchItem(request):
    queryString = request.GET.get('query',);
    categories = VendorCategory.objects.all();
    vendors = Vendor.objects.filter(Q(name__icontains = queryString) | Q(category__name__icontains = queryString))
    return render(request, "core/search.html",{'searchquery':queryString, 
                                               'vendors':vendors,
                                               'categories':categories})    

