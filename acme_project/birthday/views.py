# birthday/views.py 
from django.shortcuts import render

from .forms import BirthdayForm
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# def birthday(request):
#     print(request.GET)
#     form = BirthdayForm()
#     # Добавляем его в словарь контекста под ключом form:
#     context = {'form': form}
#     # Указываем нужный шаблон и передаём в него словарь контекста.
#     return render(request, 'birthday/birthday.html', context)

# def birthday(request):
#     # Если есть параметры GET-запроса...
#     if request.GET:
#         # ...передаём параметры запроса в конструктор класса формы.
#         form = BirthdayForm(request.GET)
#         # Если данные валидны...
#         if form.is_valid():
#             # ...то считаем, сколько дней осталось до дня рождения.
#             # Пока функции для подсчёта дней нет — поставим pass:
#             pass
#     # Если нет параметров GET-запроса.
#     else:
#         # То просто создаём пустую форму.
#         form = BirthdayForm()
#     # Передаём форму в словарь контекста:
#     context = {'form': form}
#     return render(request, 'birthday/birthday.html', context)


def birthday(request):
    form = BirthdayForm(request.GET or None)
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)