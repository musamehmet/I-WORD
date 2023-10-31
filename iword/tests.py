from django.test import TestCase
from django.urls import reverse
from .models import User, Word, Sentence


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse("login"), {"username": "invaliduser", "password": "invalidpassword"}
        )
        self.assertEqual(response.status_code, 200)


class RegisterViewTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_with_valid_data(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmation": "testpassword",
                "email": "email@email.com",
                "location": "Test Universe",
                "birthday": "1989-11-22",
                "biography": "I am test user.",
                "profileURL": "https://randomuser.me/api/portraits/lego/1.jpg",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  

    def test_register_with_invalid_data(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password": "testpassword",
                "confirmation": "testpassword",
                "email": "email@email.com",
                "location": "Test Universe",
                "birthday": "1989-11-22",
                "biography": "I am test user.",
                "profileURL": "https://randomuser.me/api/portraits/lego/1.jpg",
            },
        )
        self.assertEqual(
            response.status_code, 302
        ) 


class WordTestCase(TestCase):
    def setUp(self):
        
        self.user_id = 1  

    def test_add_word_with_invalid_data(self):
        response = self.client.post(
            reverse("addword", args=[self.user_id]),
            {
                "word": "",
                "description": "an example word",
                "pronunciation": "example",
                "prontype": "example",
                "type": "example",
            },
        )      

    def test_add_word_with_valid_data(self):
        response = self.client.post(
            reverse("addword", args=[self.user_id]),
            {
                "word": "example",
                "description": "an example word",
                "pronunciation": "example",
                "prontype": "example",
                "type": "example",
            },
        )
        

    def test_word_detail(self):
        response = self.client.get(
            reverse("word_detail", args=[1])
        )  

  
class SentenceTestCase(TestCase):
    def setUp(self):
        # Test verilerini oluşturun
        self.user_id = 1
        self.word_id = 1
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.word = Word.objects.create(
            user=self.user,
            word="example",
            description="an example word",
            pronunciation="example",
            prontype="example",
            type="example",
        )

    def test_addsentence(self):
        
        self.client.force_login(self.user)

        
        url = reverse("addsentence", args=[1])
        
        sentence = "This is a valid test sentence."
        response = self.client.post(url, {"sentence": sentence, "sentenceword": self.word.id})
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse("sentence_detail", args=[1]))
        sentence_obj = Sentence.objects.get(sentence=sentence)
        self.assertEqual(sentence_obj.sentence, sentence) 


    def test_sentence_detail(self):

        sentence = Sentence.objects.create(
            user=self.user,
            sentence="This is a test sentence.",
            sentenceword=self.word,
        )

        url = reverse("sentence_detail", args=[sentence.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("This is a test sentence.", response.content.decode("utf-8"))

        related_sentences = Sentence.objects.filter(sentenceword=self.word).order_by("-id")[:10]
        for related_sentence in related_sentences:
            self.assertIn(related_sentence.sentence, response.content.decode("utf-8"))
