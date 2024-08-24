from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q



# Create your models here.
class CustomUser(AbstractUser):
    full_name=models.CharField(max_length=100,blank=False, null=False)
    role = models.CharField(max_length=100, default='Fresher')
    sector = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    cv = models.FileField(upload_to='cv/',null=True,blank=True)
    skills_expertise = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', default='../static/theme-assets/images/avatar/05.jpg', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    
     
class Review(models.Model):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_reviews', null=True, blank=True)
    reviewed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reviews', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    rating = models.CharField(max_length=5, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.full_name} for {self.reviewed_user.full_name}" if self.reviewer and self.reviewed_user else "Anonymous Review"
    

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.thread is None:
            # Get or create the thread
            threads = Thread.objects.filter(
                Q(first_person=self.user) | Q(second_person=self.user)
            )

            if threads.exists():
                self.thread = threads.first()
            else:
                # You may want to define logic to set the second person
                # Example: self.thread.second_person = some_user
                self.thread = Thread.objects.create(first_person=self.user)
        
        super().save(*args, **kwargs)