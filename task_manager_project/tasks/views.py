from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import Task, Tag, TaskComment, TaskReminder
from .forms import TaskForm, TagForm, TaskCommentForm, TaskFilterForm


@login_required
def dashboard(request):
    # Get user's tasks with statistics
    user_tasks = Task.objects.filter(created_by=request.user)

    # Statistics
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='completed').count()
    pending_tasks = user_tasks.filter(status='pending').count()
    in_progress_tasks = user_tasks.filter(status='in_progress').count()
    overdue_tasks = user_tasks.filter(due_date__lt=timezone.now(), status__in=['pending', 'in_progress']).count()

    # Recent tasks
    recent_tasks = user_tasks.order_by('-created_at')[:5]

    # Upcoming tasks (next 7 days)
    upcoming_tasks = user_tasks.filter(
        due_date__gte=timezone.now(),
        due_date__lte=timezone.now() + timezone.timedelta(days=7),
        status__in=['pending', 'in_progress']
    ).order_by('due_date')[:5]

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_tasks': recent_tasks,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_list(request):
    tasks = Task.objects.filter(created_by=request.user)
    filter_form = TaskFilterForm(request.GET, user=request.user)

    if filter_form.is_valid():
        if filter_form.cleaned_data['search']:
            tasks = tasks.filter(
                Q(title__icontains=filter_form.cleaned_data['search']) |
                Q(description__icontains=filter_form.cleaned_data['search'])
            )
        if filter_form.cleaned_data['priority']:
            tasks = tasks.filter(priority=filter_form.cleaned_data['priority'])
        if filter_form.cleaned_data['status']:
            tasks = tasks.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data['tags']:
            tasks = tasks.filter(tags__in=filter_form.cleaned_data['tags']).distinct()
        if filter_form.cleaned_data['due_date_from']:
            tasks = tasks.filter(due_date__gte=filter_form.cleaned_data['due_date_from'])
        if filter_form.cleaned_data['due_date_to']:
            tasks = tasks.filter(due_date__lte=filter_form.cleaned_data['due_date_to'])

    # Pagination
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    comments = task.comments.all()

    if request.method == 'POST':
        comment_form = TaskCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        comment_form = TaskCommentForm()

    context = {
        'task': task,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task', 'task': task})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('tasks:task_list')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_toggle_status(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return JsonResponse({'success': True, 'status': task.get_status_display()})

    return JsonResponse({'success': False})


@login_required
def tag_list(request):
    tags = Tag.objects.filter(created_by=request.user).annotate(task_count=Count('task'))
    return render(request, 'tasks/tag_list.html', {'tags': tags})


@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.created_by = request.user
            tag.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('tasks:tag_list')
    else:
        form = TagForm()

    return render(request, 'tasks/tag_form.html', {'form': form, 'title': 'Create Tag'})


@login_required
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated successfully!')
            return redirect('tasks:tag_list')
    else:
        form = TagForm(instance=tag)

    return render(request, 'tasks/tag_form.html', {'form': form, 'title': 'Edit Tag', 'tag': tag})


@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk, created_by=request.user)

    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('tasks:tag_list')

    return render(request, 'tasks/tag_confirm_delete.html', {'tag': tag})
