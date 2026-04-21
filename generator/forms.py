"""Forms keep user input validation in one clear place."""
from django import forms


STYLE_CHOICES = [
    ("photorealistic", "Photorealistic"),
    ("cinematic", "Cinematic"),
    ("digital art", "Digital Art"),
    ("anime", "Anime"),
    ("watercolor", "Watercolor"),
    ("oil painting", "Oil Painting"),
    ("sketch", "Sketch"),
    ("low poly", "Low Poly"),
]

SIZE_CHOICES = [
    (512, "512 px"),
    (640, "640 px"),
    (768, "768 px"),
]


class TypeToImageForm(forms.Form):
    prompt = forms.CharField(
        label="Prompt",
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Example: A futuristic library floating above a quiet city",
            }
        ),
        min_length=3,
        max_length=800,
    )
    style = forms.ChoiceField(choices=STYLE_CHOICES, initial="cinematic")
    width = forms.TypedChoiceField(choices=SIZE_CHOICES, coerce=int, initial=512)
    height = forms.TypedChoiceField(choices=SIZE_CHOICES, coerce=int, initial=512)
    inference_steps = forms.IntegerField(min_value=1, max_value=80, initial=25)
    guidance_scale = forms.FloatField(min_value=1.0, max_value=20.0, initial=7.5)


class ScriptToImageForm(forms.Form):
    script = forms.CharField(
        label="Script or scene description",
        widget=forms.Textarea(
            attrs={
                "rows": 12,
                "placeholder": (
                    "Paste a scene description. Example: At sunrise, a young explorer "
                    "walks through an ancient forest with warm golden light..."
                ),
            }
        ),
        min_length=10,
        max_length=5000,
    )
    style = forms.ChoiceField(choices=STYLE_CHOICES, initial="cinematic")
    width = forms.TypedChoiceField(choices=SIZE_CHOICES, coerce=int, initial=512)
    height = forms.TypedChoiceField(choices=SIZE_CHOICES, coerce=int, initial=512)
    inference_steps = forms.IntegerField(min_value=1, max_value=80, initial=25)
    guidance_scale = forms.FloatField(min_value=1.0, max_value=20.0, initial=7.5)
