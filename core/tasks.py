from .models import Post
from datetime import timedelta
from django.utils import timezone

def clean_old_posts():
    # حذف المنشورات التي مضى عليها أكثر من أسبوعين
    expiry_threshold = timezone.now() - timedelta(weeks=2)
    Post.objects.filter(expires_at__lt=expiry_threshold).delete()
    
    # التأكد من عدم تجاوز الحجم الكلي 60 ميجا
    Post.enforce_storage_limit()
