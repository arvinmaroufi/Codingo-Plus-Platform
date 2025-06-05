from django.db import models
from Users.models import User


class Department(models.Model):
    """Represents a department where tickets can be categorized."""
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دپارتمان")  # Department name, must be unique
    description = models.TextField(blank=True, verbose_name="توضیحات")  # Optional description of the department

    def __str__(self):
        """Returns a human-readable representation of the department."""
        return self.name

    class Meta:
        """Meta options for the Department model."""
        verbose_name = "دپارتمان"
        verbose_name_plural = "دپارتمان ‌ها"
        

class Ticket(models.Model):
    """Represents a support ticket submitted by users."""
    class TicketPriorityChoices(models.TextChoices):
        """Defines priority levels for tickets."""
        LOW = "LW", "کم"
        MEDIUM = "ME", "متوسط"
        HIGH = "HG", "بالا"
        URGENT = "UR", "اضطراری"
        
    class TicketStatusChoices(models.TextChoices):
        """Defines possible statuses for tickets."""
        NEW = "NW", "جدید"
        ANSWERED = "AD", "پاسخ داده شده"
        IN_PROGRESS = "IN", "درحال بررسی"
        CLOSED = "CL", "بسته شده"
    
    subject = models.CharField(max_length=200, verbose_name="موضوع")  # The subject/title of the ticket
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets", verbose_name="کاربر")  # Links the ticket to a user; deleting user removes their tickets
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="دپارتمان")  # Links the ticket to a department
    priority = models.CharField(choices=TicketPriorityChoices.choices, max_length=10, default=TicketPriorityChoices.LOW, verbose_name="اولویت")  # Priority level of the ticket (fixed ForeignKey issue)
    status = models.CharField(choices=TicketStatusChoices.choices, max_length=10, default=TicketStatusChoices.NEW, verbose_name="وضعیت")  # Current status of the ticket
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")  # Timestamp when the ticket was created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")  # Timestamp when the ticket was last updated
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ بسته شدن")  # Timestamp when the ticket was closed

    def __str__(self):
        """Returns a human-readable representation of the ticket."""
        return f"{self.subject} - {self.user.username}"

    class Meta:
        """Meta options for the Ticket model."""
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت‌ ها"
        ordering = ["-created_at"]  # Orders tickets from newest to oldest
        

class TicketMessage(models.Model):
    """Represents messages exchanged within a ticket."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages", verbose_name="تیکت")  # Links the message to a specific ticket
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")  # User who sent the message
    message = models.TextField(verbose_name="پیام")  # Content of the message
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")  # Timestamp when the message was created

    def save(self, *args, **kwargs):
        """Ensures a user is assigned to a message before saving."""
        if not self.user_id:
            self.user = self.ticket.user
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns a human-readable representation of the message."""
        return f"پیام برای تیکت #{self.ticket.id}"

    class Meta:
        """Meta options for the TicketMessage model."""
        verbose_name = "پیام تیکت"
        verbose_name_plural = "پیام‌ های تیکت"
        ordering = ["created_at"]  # Orders messages from oldest to newest
        

class TicketAttachment(models.Model):
    """Represents file attachments associated with ticket messages."""
    message = models.ForeignKey(TicketMessage, on_delete=models.CASCADE, related_name="attachments", verbose_name="پیام")  # Links the attachment to a specific message
    file = models.FileField(upload_to="Tickets/ticket_attachments/", verbose_name="فایل")  # Stores the uploaded file
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")  # Timestamp when the file was uploaded

    def __str__(self):
        """Returns a human-readable representation of the attachment."""
        return f"پیوست برای پیام #{self.message.id}"

    class Meta:
        """Meta options for the TicketAttachment model."""
        verbose_name = "پیوست تیکت"
        verbose_name_plural = "پیوست‌ های تیکت"
        
