# core/urls.py
from django.urls import path
from core.views import writer_views, judge_views, editor_views, public_views


urlpatterns = [

    #for landing page
    path('public/published/', public_views.public_list_published_submissions, name='public-published'),

    # Writer Routes
    path('writer/upload/', writer_views.writer_upload_submission, name='writer-upload'),
    path('writer/status/<int:submission_id>/', writer_views.writer_check_status, name='writer-status'),

    # Judge Routes
    path('judge/submissions/', judge_views.judge_list_submissions, name='judge-submissions'),
    path('judge/view/<int:submission_id>/', judge_views.judge_view_submission, name='judge-view'),
    path('judge/note/<int:submission_id>/', judge_views.judge_add_note, name='judge-add-note'),
    path("judge/panel/", judge_views.judge_list_submissions),


    # Editor Routes
    path('editor/submissions/', editor_views.editor_list_submissions, name='editor-submissions'),
    path('editor/assign/<int:submission_id>/', editor_views.editor_assign_judge, name='editor-assign'),
    path('editor/status/<int:submission_id>/', editor_views.editor_update_status, name='editor-update-status'),
    path('editor/judges/', editor_views.editor_add_judge, name='editor-add-judge'),
    path('editor/suggest-judges/', editor_views.editor_suggest_judges),
    path('editor/update-status/<int:submission_id>/', editor_views.editor_update_status, name='editor-update-status'),
    path("editor/judges/list/", editor_views.editor_list_judges, name="editor-list-judges"),
    path("editor/reviews/<int:submission_id>/", editor_views.editor_fetch_reviews),


]
