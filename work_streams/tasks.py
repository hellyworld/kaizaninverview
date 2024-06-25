from kaizaninterview.celery import app
from transcripts.models import WorkInteraction
from work_streams.models import WorkStream
from django.db.models.aggregates import Count


@app.task
def do_something_with_work_streams():
    WorkStream.objects.all().annotate(work_interaction_count=Count("work_interactions"))

    for work_stream in WorkStream.objects.all():
        work_interaction_count = WorkInteraction.objects.filter(work_streams=work_stream).count()
        work_stream.title = f"{work_stream.title} ({work_interaction_count})"
        work_stream.save()
