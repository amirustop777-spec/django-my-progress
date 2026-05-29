from django import forms


class CartAddProductForm(forms.Form):
    """Форма для добавления/обновления количества товара в корзине.

    Используется в двух местах:
    1) На странице товара ("Добавить в корзину")
    2) На странице корзины ("Обновить" количество)

    Поле `override` — hidden флаг. Если True — перезаписываем quantity.
    Если False — увеличиваем текущий quantity.
    """

    # quantity — сколько штук добавить/установить.
    # min_value/max_value ограничивают разумный ввод.
    # initial=1 — значение по умолчанию.
    # widget=... задаёт HTML класс для Bootstrap.
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    # override — hidden checkbox/флаг, которым управляет сервер.
    # required=False — чтобы форма не требовала его при создании.
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput,
    )

