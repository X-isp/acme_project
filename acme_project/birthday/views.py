from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
#  LoginRequiredMixin гарантирует, что только авторизованные пользователи 
# могут получить доступ к представлению. - UserPassesTestMixin проверяет, 
# что текущий пользователь является автором объекта, который пытается удалить. 


from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10 


class BirthdayMixin:
    model = Birthday


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user 


class BirthdayCreateView(OnlyAuthorMixin, LoginRequiredMixin, BirthdayMixin, CreateView):
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form) 

class BirthdayUpdateView(OnlyAuthorMixin, LoginRequiredMixin, BirthdayMixin, UpdateView):
    form_class = BirthdayForm


class BirthdayDeleteView(OnlyAuthorMixin, LoginRequiredMixin, BirthdayMixin, DeleteView):
    pass 


class BirthdayDetailView(BirthdayMixin, DetailView):

    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context 