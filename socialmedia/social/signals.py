from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Like, Comment, Follow

@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, **kwargs):
    send_mail(
        'Your post got a new like!',
        f'Your post "{instance.post.content}" got a new like from {instance.user.username}.',
        'from@example.com',
        [instance.post.user.email]
    )

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    send_mail(
        'Your post got a new comment!',
        f'Your post "{instance.post.content}" got a new comment from {instance.user.username}: "{instance.content}".',
        'from@example.com',
        [instance.post.user.email]
    )

@receiver(post_save, sender=Follow)
def send_follow_notification(sender, instance, **kwargs):
    send_mail(
        'You have a new follower!',
        f'{instance.follower.username} is now following you.',
        'from@example.com',
        [instance.following.email]
    )
