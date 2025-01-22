from django.shortcuts import render
from .models import Section
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Section, User
from .forms import SectionForm, UserForm
from django.shortcuts import get_object_or_404
from django.contrib import messages




def index(request):
    selected_section_id = request.GET.get('section')
    search_query = request.GET.get('search', '')

    all_sections = Section.objects.all()
    
    filtered_sections = {}

    if selected_section_id:
        sections = all_sections.filter(id=selected_section_id)
    else:
        sections = all_sections
    
    for section in sections:
        if search_query:
            users = section.members.filter(full_name__icontains=search_query)
        else:
            users = section.members.all()
        
        filtered_sections[section] = users
    
    return render(request, 'index.html', {
        'sections': filtered_sections,
        'all_sections': all_sections,
        'selected_section_id': selected_section_id,
        'search_query': search_query,
    })

class SectionListView(ListView):
    model = Section
    template_name = 'section_list.html'
    context_object_name = 'sections'

class SectionCreateView(CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'section_form.html'
    success_url = reverse_lazy('section_list')

class SectionUpdateView(UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'section_form.html'
    success_url = reverse_lazy('section_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(section=self.object)
        context['other_sections'] = Section.objects.exclude(id=self.object.id)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        action = self.request.POST.get('action')
        selected_user_ids = self.request.POST.getlist('selected_users')

        if action and selected_user_ids:
            if action == 'remove':
                User.objects.filter(id__in=selected_user_ids).update(section=None)
                messages.success(self.request, 'Selected users have been removed from the section.')
            elif action == 'move':
                target_section_id = self.request.POST.get('target_section')
                if target_section_id:
                    target_section = get_object_or_404(Section, id=target_section_id)
                    User.objects.filter(id__in=selected_user_ids).update(section=target_section)
                    messages.success(self.request, 'Selected users have been moved to the target section.')
                else:
                    messages.error(self.request, 'No target section selected.')

        return response

class SectionDeleteView(DeleteView):
    model = Section
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('section_list')

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')  
        if search_query:
            queryset = queryset.filter(
                full_name__icontains=search_query
            ) | queryset.filter(
                role__icontains=search_query
            )
        return queryset

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('user_list')
