import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase as BaseTestCase

from django.contrib.auth import get_user_model

from ..models import Thread, Message


class login(object):

    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success,
            "login with username=%r, password=%r failed" % (user, password)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class TestCaseMixin(object):
    def get(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs), data)

    def post(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", {})
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data)

    def login(self, user, password):
        return login(self, user, password)

    def reload(self, obj):
        return obj.__class__._default_manager.get(pk=obj.pk)

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context), value)


class TestCase(BaseTestCase, TestCaseMixin):
    pass


class BaseTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.brosner = User.objects.create_superuser(
            "brosner", "brosner@brosner.brosner", "abc123")
        self.jtauber = User.objects.create_superuser(
            "jtauber", "jtauber@jtauber.jtauber", "abc123")
        if hasattr(self, "template_dirs"):
            self._old_template_dirs = settings.TEMPLATE_DIRS
            settings.TEMPLATE_DIRS = self.template_dirs

    def tearDown(self):
        if hasattr(self, "_old_template_dirs"):
            settings.TEMPLATE_DIRS = self._old_template_dirs


class TestMessages(BaseTest):
    def test_messages(self):
        Message.new_message(
            self.brosner, [self.jtauber], "Really?", "You can't be serious")

        self.assertEqual(Thread.inbox(self.brosner).count(), 0)
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)

        thread = Thread.inbox(self.jtauber)[0]

        Message.new_reply(thread, self.jtauber, "Yes, I am.")

        self.assertEqual(Thread.inbox(self.brosner).count(), 1)
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)

        Message.new_reply(thread, self.brosner, "If you say so...")
        Message.new_reply(thread, self.jtauber, "Indeed I do")

        self.assertEqual(
            Thread.objects.get(pk=thread.pk).latest_message.content,
            "Indeed I do")
        self.assertEqual(
            Thread.objects.get(pk=thread.pk).first_message.content,
            "You can't be serious")

    def test_ordered(self):
        t1 = Message.new_message(
            self.brosner, [self.jtauber], "Subject",
            "A test message").thread
        t2 = Message.new_message(
            self.brosner, [self.jtauber], "Another",
            "Another message").thread
        t3 = Message.new_message(
            self.brosner, [self.jtauber], "Pwnt",
            "Haha I'm spamming your inbox").thread
        self.assertEqual(Thread.ordered([t2, t1, t3]), [t3, t2, t1])


class TestMessageViews(BaseTest):
    template_dirs = [
        os.path.join(os.path.dirname(__file__), "templates")
    ]

    def test_create_message(self):
        with self.login("brosner", "abc123"):
            response = self.get("messages_inbox")
            self.assertEqual(response.status_code, 200)

            response = self.get("message_create")
            self.assertEqual(response.status_code, 200)

            data = {
                "subject": "The internet is down.",
                "content": "Does this affect any of our sites?",
                "to_user": str(self.jtauber.id)
            }

            response = self.post("message_create", data=data)
            self.assertEqual(response.status_code, 302)

            self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
            self.assertEqual(Thread.inbox(self.brosner).count(), 0)

            response = self.get("message_create", user_id=self.jtauber.id)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "selected=\"selected\">jtauber</option>")

            thread_id = Thread.inbox(self.jtauber).get().id

            response = self.get("messages_thread_detail", thread_id=thread_id)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Does this affect any of our sites?")

        with self.login("jtauber", "abc123"):
            response = self.get("messages_inbox")
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Does this affect")

            response = self.get("messages_thread_detail", thread_id=thread_id)
            self.assertContains(response, "Does this affect")

            response = self.post("messages_thread_delete", thread_id=thread_id)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Thread.inbox(self.jtauber).count(), 0)

            data = {
                "content": "Nope, the internet being down doesn't affect us.",
            }

            response = self.post("messages_thread_detail", thread_id=thread_id, data=data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(Thread.inbox(self.brosner).count(), 1)
            self.assertEqual(
                Thread.inbox(self.brosner).get().messages.count(),
                2
            )
            self.assertEqual(Thread.unread(self.jtauber).count(), 0)

    def test_urls(self):
        self.assertEqual(reverse("message_create", args=[10]), "/create/10/")


class TestTemplateTags(BaseTest):
    def test_unread(self):
        thread = Message.new_message(self.brosner, [self.jtauber], "Why did you the internet?", "I demand to know.").thread
        tmpl = """{% load pinax_messages_tags %}{% if thread|unread:user %}UNREAD{% else %}READ{% endif %}"""
        self.assert_renders(
            tmpl,
            Context({"thread": thread, "user": self.jtauber}),
            "UNREAD"
        )
        self.assert_renders(
            tmpl,
            Context({"thread": thread, "user": self.brosner}),
            "READ",
        )
